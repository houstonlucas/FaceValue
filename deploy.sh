#!/bin/bash

# Deployment script for FaceValue to Elastic Beanstalk
# This script helps ensure environment variables are properly configured

echo "🚀 Deploying FaceValue to Elastic Beanstalk..."

# Check if EB CLI is available
if ! command -v eb &> /dev/null; then
    echo "❌ EB CLI is not installed. Please install it first:"
    echo "   pip install awsebcli"
    exit 1
fi

# Check if we're in the right directory
if [ ! -f "docker-compose.yml" ]; then
    echo "❌ docker-compose.yml not found. Are you in the FaceValue directory?"
    exit 1
fi

echo "📦 Deploying application..."
eb deploy

echo "✅ Deployment initiated!"
echo ""
echo "🔧 Important: Make sure to set the following environment variables in EB Console:"
echo "   - POSTGRES_USER=postgres"
echo "   - POSTGRES_PASSWORD=your-postgres-password"
echo "   - POSTGRES_HOST=facevalue.c3uww8i4qmkv.us-west-1.rds.amazonaws.com"
echo "   - POSTGRES_PORT=5432"
echo "   - POSTGRES_DB=facevalue"
echo "   - DJANGO_SECRET_KEY=django-insecure-change-this-in-production"
echo "   - DJANGO_DEBUG=False"
echo "   - DEBUG=False"
echo "   - DJANGO_ALLOWED_HOSTS=*"
echo "   - ALLOWED_HOSTS=facevalue-api-env.eba-rih4z2ep.us-west-1.elasticbeanstalk.com,*"
echo ""
echo "💡 You can set these via:"
echo "   1. EB CLI: eb setenv KEY=VALUE"
echo "   2. AWS Console: Go to your EB environment > Configuration > Software"
echo ""
echo "🔍 After deployment, check the logs with: eb logs"
