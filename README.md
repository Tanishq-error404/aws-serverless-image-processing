# AWS Serverless Image Processing Pipeline

An event-driven serverless image processing pipeline built using AWS. The system automatically processes uploaded images, stores the processed output, and records processing metadata.

## Architecture



AWS Services Used
Service	Purpose
-Amazon S3	Stores original and processed images
-Amazon SQS	Provides asynchronous message queuing
-AWS Lambda	Processes images without managing servers
-Pillow	Resizes and processes images
-Amazon DynamoDB	Stores processing metadata
-AWS IAM	Controls permissions between services
-Amazon CloudWatch	Monitors Lambda execution and logs

How It Works
-A user uploads an image to the S3 upload bucket.
-Amazon S3 generates an ObjectCreated event.
-The event is sent to an Amazon SQS queue.
-AWS Lambda receives the SQS message.
-Lambda downloads the image from S3.
-Pillow opens and processes the image.
-The image is resized while maintaining its aspect ratio.
-The processed image is uploaded to a separate S3 bucket.
-Processing metadata is stored in DynamoDB.
-CloudWatch Logs provide execution and debugging information.

Image Processing

Pillow is used inside the Lambda function to resize uploaded images.

Example test:

Original image:
736 × 1074

Processed image:
548 × 800

The aspect ratio is maintained during resizing.

Example Workflow
bankai.jpg
     │
     ▼
S3 Upload Bucket
     │
     ▼
SQS Queue
     │
     ▼
Lambda + Pillow
     │
     ├──► processed-bankai.jpg
     │
     └──► DynamoDB record

Testing

-The complete pipeline was tested using a real image upload.

-The CloudWatch execution logs confirmed:

-SQS successfully triggered Lambda
-Image was downloaded from S3
-Pillow processed the image
-Image dimensions changed from 736 × 1074 to 548 × 800
-Processed image was uploaded successfully
-DynamoDB record was created successfully
-Project Structure
aws-serverless-image-processing/
│
├── lambda/
│   └── lambda_function.py
│
├── policies/
│   ├── lambda-s3-policy.json
│   ├── lambda-dynamodb-policy.json
│   └── s3-sqs-policy.json
│
├── screenshots/
│
└── README.md

Key Concepts Demonstrated

-Event-driven architecture
-Serverless computing
-Asynchronous processing
-S3 event notifications
-SQS → Lambda integration
-AWS IAM permissions
-Image processing with Python and Pillow
-DynamoDB data persistence
-CloudWatch monitoring
-AWS Lambda Layers

Future Improvements
-Add a Dead Letter Queue (DLQ) for failed messages
-Improve Lambda error handling
-Add idempotent processing
-Move configuration values to Lambda environment variables
-Add automated deployment using AWS SAM or Terraform
-Add automated testing
