#!/bin/bash
set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}🚀 A Box of Mac and Cheese - Deployment Script${NC}\n"

# Check if AWS CLI is installed
if ! command -v aws &> /dev/null; then
    echo -e "${RED}❌ AWS CLI is not installed. Please install it first.${NC}"
    exit 1
fi

# Check if SAM CLI is installed
if ! command -v sam &> /dev/null; then
    echo -e "${RED}❌ AWS SAM CLI is not installed. Please install it first.${NC}"
    echo "Install with: brew install aws-sam-cli"
    exit 1
fi

# Parse arguments
ENVIRONMENT=${1:-dev}
GUIDED=${2:-false}

echo -e "${YELLOW}Environment: ${ENVIRONMENT}${NC}"
echo -e "${YELLOW}Guided mode: ${GUIDED}${NC}\n"

# Validate environment
if [[ ! "$ENVIRONMENT" =~ ^(dev|prod)$ ]]; then
    echo -e "${RED}❌ Invalid environment. Use 'dev' or 'prod'${NC}"
    exit 1
fi

# Build the application
echo -e "${GREEN}📦 Building SAM application...${NC}"
sam build

# Deploy the application
echo -e "${GREEN}🚀 Deploying to AWS...${NC}"
if [ "$GUIDED" = "true" ]; then
    sam deploy --guided --config-env $ENVIRONMENT
else
    sam deploy --config-env $ENVIRONMENT
fi

# Get outputs
echo -e "\n${GREEN}✅ Deployment complete!${NC}\n"
echo -e "${YELLOW}📋 Stack Outputs:${NC}"
aws cloudformation describe-stacks \
    --stack-name "a-box-of-mac-and-cheese${ENVIRONMENT:+-$ENVIRONMENT}" \
    --query 'Stacks[0].Outputs[*].[OutputKey,OutputValue]' \
    --output table

echo -e "\n${GREEN}🎉 Deployment successful!${NC}"
echo -e "${YELLOW}Next steps:${NC}"
echo "1. Update config.js with the API endpoints"
echo "2. Deploy the frontend to your hosting service (or use GitHub Pages)"
echo "3. Test the application"
