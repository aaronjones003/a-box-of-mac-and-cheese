#!/bin/bash
set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}🎨 A Box of Mac and Cheese - Initial Setup${NC}\n"

# Check prerequisites
echo -e "${YELLOW}Checking prerequisites...${NC}"

if ! command -v aws &> /dev/null; then
    echo -e "${RED}❌ AWS CLI not found${NC}"
    echo "Install: https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html"
    exit 1
fi

if ! command -v sam &> /dev/null; then
    echo -e "${RED}❌ AWS SAM CLI not found${NC}"
    echo "Install: brew install aws-sam-cli"
    exit 1
fi

if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python 3 not found${NC}"
    exit 1
fi

echo -e "${GREEN}✅ All prerequisites installed${NC}\n"

# Check AWS credentials
echo -e "${YELLOW}Checking AWS credentials...${NC}"
if ! aws sts get-caller-identity &> /dev/null; then
    echo -e "${RED}❌ AWS credentials not configured${NC}"
    echo "Run: aws configure"
    echo "Or: aws sso login"
    exit 1
fi

ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
REGION=$(aws configure get region || echo "us-east-1")

echo -e "${GREEN}✅ AWS Account: ${ACCOUNT_ID}${NC}"
echo -e "${GREEN}✅ Region: ${REGION}${NC}\n"

# Check Bedrock model access
echo -e "${YELLOW}Checking Bedrock model access...${NC}"
echo "Please ensure you have enabled the following model in AWS Bedrock:"
echo "  - amazon.titan-image-generator-v2:0"
echo ""
read -p "Have you enabled this model? (y/n) " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo -e "${YELLOW}⚠️  Please enable the model in AWS Bedrock Console:${NC}"
    echo "https://console.aws.amazon.com/bedrock/home?region=${REGION}#/modelaccess"
    exit 1
fi

# Create Pillow layer
echo -e "\n${YELLOW}Creating Pillow layer...${NC}"
mkdir -p layers/pillow/python
pip3 install --target layers/pillow/python Pillow
echo -e "${GREEN}✅ Pillow layer created${NC}\n"

# Install frontend dependencies
echo -e "${YELLOW}Installing frontend dependencies...${NC}"
npm install
echo -e "${GREEN}✅ Frontend dependencies installed${NC}\n"

echo -e "${GREEN}🎉 Setup complete!${NC}\n"
echo -e "${YELLOW}Next steps:${NC}"
echo "1. Run: ./scripts/deploy.sh dev true    # Deploy with guided setup"
echo "2. Update config.js with API endpoints from deployment output"
echo "3. Open index.html in a browser or deploy to hosting"
