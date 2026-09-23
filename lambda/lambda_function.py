import json
import boto3
import urllib.parse
import os
from datetime import datetime, timezone
from PIL import Image

s3 = boto3.client('s3')
dynamodb = boto3.client('dynamodb')

UPLOAD_BUCKET = "project2-image-uploads-tanishq-84721"
PROCESSED_BUCKET = "project2-image-processed-tanishq-84721"
TABLE_NAME = "project2-image-processing"


def lambda_handler(event, context):

    print("Lambda started processing SQS event")

    for record in event['Records']:

        message_body = json.loads(record['body'])

        s3_record = message_body['Records'][0]['s3']

        bucket = s3_record['bucket']['name']

        key = urllib.parse.unquote_plus(
            s3_record['object']['key']
        )

        print(f"Input bucket: {bucket}")
        print(f"Input image: {key}")

        filename = os.path.basename(key)

        # Download original image
        local_path = f"/tmp/{filename}"

        s3.download_file(
            bucket,
            key,
            local_path
        )

        print(f"Downloaded image to {local_path}")

        # Open image using Pillow
        image = Image.open(local_path)

        print(f"Original image size: {image.size}")

        # Resize image while maintaining aspect ratio
        image.thumbnail((800, 800))

        print(f"Processed image size: {image.size}")

        # Create processed file
        processed_path = f"/tmp/processed-{filename}"

        # JPEG cannot store transparency
        if image.mode in ("RGBA", "P"):
            image = image.convert("RGB")

        image.save(processed_path)

        print(f"Processed image saved to {processed_path}")

        # Upload processed image
        processed_key = f"processed-{filename}"

        s3.upload_file(
            processed_path,
            PROCESSED_BUCKET,
            processed_key
        )

        print(
            f"Processed image uploaded to "
            f"s3://{PROCESSED_BUCKET}/{processed_key}"
        )

        # Store processing information in DynamoDB
        dynamodb.put_item(
            TableName=TABLE_NAME,
            Item={
                'image_id': {'S': filename},
                'status': {'S': 'PROCESSED'},
                'original_bucket': {'S': bucket},
                'original_key': {'S': key},
                'processed_bucket': {'S': PROCESSED_BUCKET},
                'processed_key': {'S': processed_key},
                'processed_at': {
                    'S': datetime.now(timezone.utc).isoformat()
                },
                'original_size': {
                    'S': str(image.size)
                }
            }
        )

        print("DynamoDB record created successfully")

    return {
        'statusCode': 200,
        'body': json.dumps(
            'Image processing completed successfully'
        )
    }
