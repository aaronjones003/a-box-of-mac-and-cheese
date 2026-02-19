# Architecture Documentation

## System Overview

A Box of Mac and Cheese is a serverless application that generates AI-powered fantasy book covers. The system uses AWS managed services to create a scalable, cost-effective solution.

## Architecture Diagram

```
┌─────────────┐
│   Browser   │
│  (Frontend) │
└──────┬──────┘
       │ HTTPS
       ▼
┌─────────────────────────────────────────────────────────┐
│                    API Gateway                          │
│  ┌──────────────┐              ┌──────────────┐       │
│  │ GET /init    │              │ POST /status │       │
│  └──────┬───────┘              └──────┬───────┘       │
└─────────┼──────────────────────────────┼──────────────┘
          │                              │
          ▼                              ▼
┌─────────────────┐            ┌─────────────────┐
│ InvokeFunction  │            │ StatusFunction  │
│    (Lambda)     │            │    (Lambda)     │
└────────┬────────┘            └────────┬────────┘
         │                              │
         │ start_execution              │ describe_execution
         ▼                              │
┌────────────────────────────────────────┼──────────┐
│         Step Functions State Machine   │          │
│  ┌──────────────────────────────────────────┐    │
│  │ 1. GenerateTitleAndMetadata (Lambda)     │    │
│  │    ↓                                      │    │
│  │ 2. GenerateBackgroundImage (Bedrock)     │    │
│  │    ↓                                      │    │
│  │ 3. OverlayTextOnImage (Lambda)           │    │
│  └──────────────────────────────────────────┘    │
└───────────────────────────────────────────────────┘
         │                              │
         │ write images                 │ read images
         ▼                              ▼
┌─────────────────────────────────────────────────┐
│                    S3 Bucket                    │
│  /backgrounds/  |  /covers/                    │
└─────────────────────────────────────────────────┘
```

## Components

### Frontend

**Technology**: Vanilla JavaScript, HTML5, CSS3

**Responsibilities**:
- User interface for book cover generation
- API communication with backend
- Polling for generation status
- Image display and download

**Key Files**:
- `index.html` - Main UI
- `scripts.js` - Application logic
- `config.js` - API endpoint configuration
- `test.js` - Automated tests

### API Gateway

**Type**: AWS API Gateway REST API

**Endpoints**:
- `GET /init` - Initiate book cover generation
- `POST /status` - Check generation status

**Features**:
- CORS enabled for browser access
- Automatic request/response transformation
- CloudWatch logging

### Lambda Functions

#### 1. InvokeStepFunction (`src/invoke_step_function/`)

**Trigger**: API Gateway GET /init

**Purpose**: Start Step Functions execution

**Flow**:
1. Receive request from API Gateway
2. Call Step Functions `start_execution`
3. Return execution ARN to frontend

**Environment Variables**:
- `STATE_MACHINE_ARN` - Step Functions ARN

#### 2. Step1Function (`src/step_1/`)

**Trigger**: Step Functions

**Purpose**: Generate random book title and metadata

**Flow**:
1. Select random nouns and elements from predefined lists
2. Construct title: "A [Noun] of [Element] and [Element]"
3. Generate random author name
4. Prepare Bedrock API parameters
5. Return metadata for next step

**Output**:
```json
{
  "statusCode": 200,
  "body": {
    "title": "A Princess of Space and Power",
    "author": "Clara K. Blaas",
    "stable_image_params": {...},
    "model_id": "amazon.titan-image-generator-v2:0",
    "bucket": "a-box-of-mac-and-cheese-images",
    "background_key": "backgrounds/...",
    "cover_key": "covers/...",
    "output_url": "https://..."
  }
}
```

#### 3. Step2Function (`src/step_2/`)

**Trigger**: Step Functions (after Bedrock)

**Purpose**: Overlay title text on generated background

**Dependencies**:
- Pillow (PIL) - Image processing library
- Custom font (Lancelot Regular)

**Flow**:
1. Retrieve background image from S3
2. Load image with Pillow
3. Draw title text with custom font
4. Add stroke for readability
5. Save final cover to S3
6. Return output URL

**Memory**: 1024 MB (for image processing)

#### 4. GetStatusFunction (`src/get_status/`)

**Trigger**: API Gateway POST /status

**Purpose**: Check Step Functions execution status

**Flow**:
1. Receive execution ARN from frontend
2. Call Step Functions `describe_execution`
3. Return status and output

**Response**:
```json
{
  "status": "SUCCEEDED|RUNNING|FAILED",
  "output": "{...}"
}
```

### Step Functions State Machine

**Definition**: `statemachine/book-cover-generator.asl.json`

**States**:

1. **GenerateTitleAndMetadata**
   - Type: Task (Lambda)
   - Generates title and parameters
   - Retries on transient errors

2. **GenerateBackgroundImage**
   - Type: Task (Bedrock)
   - Invokes Titan Image Generator v2
   - Saves image to S3
   - Uses parameters from Step 1

3. **OverlayTextOnImage**
   - Type: Task (Lambda)
   - Overlays text on background
   - Saves final cover to S3
   - Returns output URL

**Error Handling**:
- Automatic retries with exponential backoff
- Detailed error messages in CloudWatch
- Failed executions can be inspected via console

### Amazon Bedrock

**Model**: `amazon.titan-image-generator-v2:0`

**Input**:
```json
{
  "taskType": "TEXT_IMAGE",
  "textToImageParams": {
    "text": "A fantasy background image..."
  },
  "imageGenerationConfig": {
    "numberOfImages": 1,
    "quality": "standard",
    "cfgScale": 8.0,
    "height": 640,
    "width": 384,
    "seed": 0
  }
}
```

**Output**: Base64-encoded PNG image

**Cost**: ~$0.008 per image

### S3 Bucket

**Name**: `a-box-of-mac-and-cheese-images`

**Structure**:
```
/backgrounds/
  - [title].png (Bedrock-generated images)
/covers/
  - [title].png (Final covers with text)
```

**Configuration**:
- Public read access for generated images
- CORS enabled for browser access
- Lifecycle policies (optional) for cleanup

## Data Flow

### Generation Request Flow

1. **User Action**: Click "Generate" button
2. **Frontend**: Call `GET /init`
3. **API Gateway**: Route to InvokeStepFunction
4. **Lambda**: Start Step Functions execution
5. **Response**: Return execution ARN
6. **Frontend**: Begin polling `/status`

### Step Functions Execution Flow

1. **Step 1 (Lambda)**:
   - Generate title: "A Crown of Fire and Ice"
   - Generate author: "Mara J. Graas"
   - Prepare Bedrock parameters
   - Output metadata

2. **Bedrock Invocation**:
   - Receive prompt from Step 1
   - Generate 384x640 background image
   - Save to S3: `s3://bucket/backgrounds/A Crown of Fire and Ice.png`

3. **Step 2 (Lambda)**:
   - Read background from S3
   - Load with Pillow
   - Draw title text in sections:
     - "A Crown" (top)
     - "of" (middle)
     - "Fire" (middle)
     - "and" (middle)
     - "Ice" (bottom)
   - Save to S3: `s3://bucket/covers/A Crown of Fire and Ice.png`
   - Return URL

### Status Polling Flow

1. **Frontend**: Poll every 3 seconds
2. **API Gateway**: Route to GetStatusFunction
3. **Lambda**: Check execution status
4. **Response**: Return status + output
5. **Frontend**: 
   - If RUNNING: Continue polling
   - If SUCCEEDED: Display image
   - If FAILED: Show error

## Security

### IAM Roles

**Lambda Execution Role**:
- CloudWatch Logs write
- S3 read/write on specific bucket
- Bedrock InvokeModel (Step Functions only)
- Step Functions execution (InvokeFunction only)

**Step Functions Role**:
- Lambda invoke permissions
- Bedrock InvokeModel permissions
- S3 write permissions

### API Security

- CORS configured for specific origins (currently `*`)
- No authentication (public demo)
- Rate limiting via API Gateway (optional)

### Data Security

- S3 bucket allows public read (required for image display)
- No sensitive data stored
- Temporary execution data in Step Functions (90 days retention)

## Scalability

### Current Limits

- **Lambda**: 1000 concurrent executions (default)
- **Step Functions**: 1M executions per account per region
- **Bedrock**: Varies by model (check quotas)
- **API Gateway**: 10,000 requests per second

### Scaling Considerations

- Lambda auto-scales automatically
- Step Functions handles queuing
- S3 scales infinitely
- Bedrock may require quota increase for high volume

### Cost at Scale

| Requests/Month | Estimated Cost |
|----------------|----------------|
| 1,000          | $10            |
| 10,000         | $100           |
| 100,000        | $1,000         |

## Monitoring

### CloudWatch Metrics

- Lambda invocations, duration, errors
- Step Functions execution count, success rate
- API Gateway requests, latency, 4xx/5xx errors
- Bedrock API calls, throttles

### CloudWatch Logs

- Lambda function logs (per function)
- Step Functions execution history
- API Gateway access logs

### Alarms (Recommended)

- Lambda error rate > 5%
- Step Functions failed executions
- API Gateway 5xx errors
- Bedrock throttling

## Deployment

### Infrastructure as Code

**Tool**: AWS SAM (Serverless Application Model)

**Template**: `template.yaml`

**Benefits**:
- Version controlled infrastructure
- Reproducible deployments
- Automatic resource creation
- Built-in best practices

### CI/CD (Optional)

Can be integrated with:
- GitHub Actions (frontend auto-deploys via GitHub Pages)
- AWS CodePipeline
- GitLab CI

### Environments

- **Dev**: Testing and development
- **Prod**: Production deployment

Managed via SAM configuration profiles.

## Future Enhancements

### Potential Improvements

1. **Authentication**: Add Cognito for user accounts
2. **Caching**: Cache generated covers to reduce costs
3. **Customization**: Allow users to input custom titles
4. **Gallery**: Store and display user-generated covers
5. **Social Sharing**: Add share to social media
6. **Analytics**: Track popular title combinations
7. **A/B Testing**: Test different AI models
8. **CDN**: Add CloudFront for faster image delivery

### Alternative Architectures

1. **Serverless Framework**: Alternative to SAM
2. **AWS CDK**: TypeScript-based IaC
3. **Terraform**: Multi-cloud IaC
4. **ECS/Fargate**: Container-based deployment
5. **Lambda@Edge**: Edge computing for global users

## Frontend Deployment

The frontend files (index.html, scripts.js, config.js, test.js, test.html) are kept at the root level for GitHub Pages compatibility. This allows the live demo to work without redirects or subdirectory configuration.
