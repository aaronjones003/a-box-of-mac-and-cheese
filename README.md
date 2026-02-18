# A Box of Mac and Cheese 📚✨

> AI-powered fantasy book cover generator using AWS Bedrock, Step Functions, and Lambda

## Overview

A serverless web application that generates random fantasy book covers in the style of "A Box of Mac and Cheese". The app creates unique titles like "A Princess of Space and Power" and generates beautiful AI-powered background images, then overlays the title text to create a complete book cover.

## Architecture

### Backend (AWS)
- **AWS Step Functions**: Orchestrates the cover generation workflow
- **AWS Lambda**: Three functions for title generation, image processing, and workflow management
- **Amazon Bedrock**: AI image generation using Titan Image Generator v2
- **Amazon S3**: Storage for generated cover images
- **API Gateway**: REST API endpoints for frontend communication

### Frontend
- **Vanilla JavaScript**: No framework dependencies
- **HTML5/CSS3**: Modern, responsive design
- **Playwright**: Automated testing

## Project Structure

```
.
├── template.yaml              # AWS SAM Infrastructure as Code
├── samconfig.toml             # SAM deployment configuration
├── src/                       # Lambda function source code
│   ├── step_1/               # Generate title and metadata
│   ├── step_2/               # Overlay text on image
│   ├── invoke_step_function/ # Initiate workflow
│   └── get_status/           # Check workflow status
├── statemachine/             # Step Functions definitions
│   └── book-cover-generator.asl.json
├── layers/                   # Lambda layers (Pillow)
├── scripts/                  # Deployment and setup scripts
│   ├── setup.sh             # Initial setup
│   └── deploy.sh            # Deploy to AWS
├── frontend/                # Web application
│   ├── index.html
│   ├── scripts.js
│   ├── config.js            # API endpoint configuration
│   └── test.js              # Automated tests
└── README.md
```

## Prerequisites

- **AWS Account** with appropriate permissions
- **AWS CLI** configured with credentials
- **AWS SAM CLI** installed
- **Python 3.11+**
- **Node.js 18+** (for frontend testing)
- **Bedrock Model Access**: `amazon.titan-image-generator-v2:0` enabled

## Quick Start

### 1. Initial Setup

```bash
# Clone the repository
cd a-box-of-mac-and-cheese

# Run setup script
./scripts/setup.sh
```

This will:
- Check all prerequisites
- Verify AWS credentials
- Create the Pillow Lambda layer
- Install frontend dependencies

### 2. Enable Bedrock Model

1. Go to [AWS Bedrock Console](https://console.aws.amazon.com/bedrock/)
2. Navigate to **Model access**
3. Enable **Amazon Titan Image Generator v2**
4. Wait for approval (usually instant)

### 3. Deploy Infrastructure

```bash
# First deployment (guided)
./scripts/deploy.sh dev true

# Subsequent deployments
./scripts/deploy.sh dev

# Production deployment
./scripts/deploy.sh prod
```

### 4. Configure Frontend

1. After deployment, note the API endpoints from the output
2. Update `frontend/config.js`:

```javascript
const CONFIG = {
  API_INIT_ENDPOINT: 'https://YOUR_API_ID.execute-api.us-east-1.amazonaws.com/default/init',
  API_STATUS_ENDPOINT: 'https://YOUR_API_ID.execute-api.us-east-1.amazonaws.com/default/status',
  // ...
};
```

### 5. Test Locally

```bash
cd frontend
npm test
```

Or open `frontend/index.html` in a browser.

## Deployment Details

### Manual Deployment Steps

If you prefer manual deployment:

```bash
# Build the application
sam build

# Validate the template
sam validate --lint

# Deploy with guided setup
sam deploy --guided

# Or deploy with existing config
sam deploy --config-env dev
```

### Environment Variables

The SAM template uses these parameters:
- `Environment`: `dev` or `prod`
- `S3BucketName`: Bucket for storing images (default: `a-box-of-mac-and-cheese-images`)

### Stack Outputs

After deployment, the stack provides:
- `ApiEndpoint`: Base API Gateway URL
- `InitEndpoint`: Endpoint to start generation
- `StatusEndpoint`: Endpoint to check status
- `S3BucketName`: Image storage bucket
- `StateMachineArn`: Step Functions ARN

## Development

### Local Testing

```bash
# Run frontend tests
cd frontend
npm test

# Start local API (requires SAM)
sam local start-api
```

### Updating Lambda Functions

1. Edit code in `src/*/lambda_function.py`
2. Run `sam build`
3. Deploy with `./scripts/deploy.sh dev`

### Updating State Machine

1. Edit `statemachine/book-cover-generator.asl.json`
2. Deploy with `./scripts/deploy.sh dev`

## Workflow

1. **User clicks Generate**
2. Frontend calls `/init` endpoint
3. Lambda invokes Step Functions
4. **Step 1**: Generate random title and author
5. **Bedrock**: Create AI background image (saved to S3)
6. **Step 2**: Overlay title text on image
7. Frontend polls `/status` endpoint
8. Display final cover image

## Cost Estimation

- **Lambda**: ~$0.20 per 1M requests
- **Step Functions**: ~$0.025 per 1K transitions
- **Bedrock Titan v2**: ~$0.008 per image
- **S3**: ~$0.023 per GB storage
- **API Gateway**: ~$3.50 per 1M requests

**Estimated cost per cover**: ~$0.01

## Troubleshooting

### Deployment Fails

```bash
# Check AWS credentials
aws sts get-caller-identity

# Validate template
sam validate --lint

# Check CloudFormation events
aws cloudformation describe-stack-events --stack-name a-box-of-mac-and-cheese
```

### Bedrock Model Not Available

- Ensure model is enabled in Bedrock console
- Check region (Titan v2 may not be available in all regions)
- Verify IAM permissions for `bedrock:InvokeModel`

### Frontend Not Connecting

- Verify API endpoints in `frontend/config.js`
- Check CORS configuration in API Gateway
- Inspect browser console for errors

## Testing

The project includes automated tests:

```bash
cd frontend
npm test
```

Tests verify:
- DOM elements exist
- Button states are correct
- Image visibility behavior
- Status div hiding when image displays
- No JavaScript errors

## Cleanup

To delete all AWS resources:

```bash
# Delete the CloudFormation stack
aws cloudformation delete-stack --stack-name a-box-of-mac-and-cheese

# Empty and delete S3 bucket
aws s3 rm s3://a-box-of-mac-and-cheese-images --recursive
aws s3 rb s3://a-box-of-mac-and-cheese-images
```

## Contributing

This project uses Infrastructure as Code for reproducibility. When making changes:

1. Update `template.yaml` for infrastructure changes
2. Update Lambda code in `src/`
3. Test locally with `sam local`
4. Deploy to dev environment first
5. Run automated tests
6. Deploy to production

## License

MIT License - see LICENSE file

## Live Demo

https://onigiri.zone/a-box-of-mac-and-cheese/
