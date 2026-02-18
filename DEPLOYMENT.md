# Deployment Guide

## First-Time Deployment

### Step 1: Prerequisites Check

```bash
# Verify AWS CLI
aws --version

# Verify SAM CLI
sam --version

# Verify Python
python3 --version

# Check AWS credentials
aws sts get-caller-identity
```

### Step 2: Enable Bedrock Model

1. Navigate to [AWS Bedrock Console](https://console.aws.amazon.com/bedrock/)
2. Go to **Model access** in the left sidebar
3. Click **Manage model access**
4. Find **Amazon Titan Image Generator v2**
5. Click **Request model access** or **Enable**
6. Wait for approval (usually instant for Titan models)

### Step 3: Run Setup Script

```bash
./scripts/setup.sh
```

This script will:
- Verify all prerequisites are installed
- Check AWS credentials
- Prompt you to confirm Bedrock model access
- Create the Pillow Lambda layer
- Install frontend dependencies

### Step 4: Deploy Infrastructure

```bash
# First deployment with guided setup
./scripts/deploy.sh dev true
```

You'll be prompted for:
- Stack name (default: `a-box-of-mac-and-cheese`)
- AWS Region (default: `us-east-1`)
- Confirm changes before deploy
- Allow SAM CLI IAM role creation
- Save arguments to configuration file

Answer `Y` to all prompts for first deployment.

### Step 5: Configure Frontend

After deployment completes, you'll see output like:

```
Stack Outputs:
---------------------------------------------------------
| InitEndpoint    | https://abc123.execute-api.us-east-1.amazonaws.com/default/init   |
| StatusEndpoint  | https://abc123.execute-api.us-east-1.amazonaws.com/default/status |
---------------------------------------------------------
```

Update `frontend/config.js`:

```javascript
const CONFIG = {
  API_INIT_ENDPOINT: 'https://abc123.execute-api.us-east-1.amazonaws.com/default/init',
  API_STATUS_ENDPOINT: 'https://abc123.execute-api.us-east-1.amazonaws.com/default/status',
  POLL_INTERVAL_MS: 3000,
  MAX_POLLS: 60,
  ENVIRONMENT: 'dev'
};
```

### Step 6: Test

```bash
cd frontend
npm test
```

Or open `frontend/index.html` in a browser.

## Subsequent Deployments

After the first deployment, updates are simpler:

```bash
# Deploy changes
./scripts/deploy.sh dev

# Or for production
./scripts/deploy.sh prod
```

## Manual Deployment (Alternative)

If you prefer not to use the scripts:

```bash
# Build
sam build

# Validate
sam validate --lint

# Deploy
sam deploy --guided --config-env dev
```

## Updating Specific Components

### Update Lambda Functions Only

```bash
sam build
sam deploy --config-env dev
```

### Update State Machine Only

Edit `statemachine/book-cover-generator.asl.json`, then:

```bash
sam deploy --config-env dev
```

### Update Frontend Only

No deployment needed - just update files and refresh browser.
For production, upload `frontend/` to your hosting service.

## Environment Management

### Development Environment

```bash
./scripts/deploy.sh dev
```

Creates stack: `a-box-of-mac-and-cheese-dev`

### Production Environment

```bash
./scripts/deploy.sh prod
```

Creates stack: `a-box-of-mac-and-cheese-prod`

## Rollback

If deployment fails or you need to rollback:

```bash
# View stack events
aws cloudformation describe-stack-events \
  --stack-name a-box-of-mac-and-cheese \
  --max-items 20

# Rollback to previous version
aws cloudformation rollback-stack \
  --stack-name a-box-of-mac-and-cheese
```

## Monitoring

### View Logs

```bash
# Step Functions execution logs
aws stepfunctions describe-execution \
  --execution-arn <execution-arn>

# Lambda logs
sam logs -n Step1Function --stack-name a-box-of-mac-and-cheese --tail

# API Gateway logs
aws logs tail /aws/apigateway/a-box-of-mac-and-cheese --follow
```

### CloudWatch Metrics

Navigate to CloudWatch Console to view:
- Lambda invocations and errors
- Step Functions execution metrics
- API Gateway request counts
- Bedrock API usage

## Cleanup

To completely remove all resources:

```bash
# Delete CloudFormation stack
aws cloudformation delete-stack --stack-name a-box-of-mac-and-cheese

# Wait for deletion
aws cloudformation wait stack-delete-complete \
  --stack-name a-box-of-mac-and-cheese

# Empty and delete S3 bucket
aws s3 rm s3://a-box-of-mac-and-cheese-images --recursive
aws s3 rb s3://a-box-of-mac-and-cheese-images
```

## Troubleshooting

### "Model not found" Error

- Ensure Titan Image Generator v2 is enabled in Bedrock
- Check you're deploying to the correct region
- Verify IAM permissions include `bedrock:InvokeModel`

### "Stack already exists" Error

```bash
# Update existing stack instead
sam deploy --config-env dev
```

### "Insufficient permissions" Error

Ensure your AWS user/role has:
- CloudFormation full access
- Lambda full access
- S3 full access
- API Gateway full access
- Step Functions full access
- Bedrock invoke model permissions
- IAM role creation permissions

### Frontend Not Loading Images

- Check S3 bucket CORS configuration
- Verify bucket policy allows public read
- Check browser console for CORS errors
- Ensure API endpoints in `config.js` are correct

## Cost Optimization

### Development

- Use smaller Lambda memory sizes
- Reduce Step Functions retention period
- Enable S3 lifecycle policies to delete old images

### Production

- Enable CloudWatch Logs retention policies
- Use Reserved Concurrency for predictable workloads
- Monitor and set billing alerts
