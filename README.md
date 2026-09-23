# AWS Serverless Image Processing Pipeline

An event-driven serverless image processing pipeline built using AWS.

## Architecture

S3 → SQS → Lambda → Pillow → S3 + DynamoDB

## AWS Services Used

- Amazon S3
- Amazon SQS
- AWS Lambda
- Amazon DynamoDB
- AWS IAM
- Amazon CloudWatch

## How It Works

1. A user uploads an image to an Amazon S3 upload bucket.
2. Amazon S3 generates an ObjectCreated event.
3. The event is sent to an Amazon SQS queue.
4. AWS Lambda consumes the SQS message.
5. Lambda downloads the image from S3.
6. Pillow processes and resizes the image.
7. The processed image is uploaded to a separate S3 bucket.
8. Processing metadata is stored in DynamoDB.
9. CloudWatch Logs provide execution and debugging information.

## Image Processing

The Lambda function uses Pillow to resize images while maintaining their aspect ratio.

Example:

Original image:

736 × 1074

Processed image:

548 × 800

## Project Status

Working successfully.

The complete event-driven pipeline has been tested with a real image upload.
