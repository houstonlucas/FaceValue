#!/bin/bash

# Script to set environment variables for FaceValue on Elastic Beanstalk
# This ensures all required environment variables are set correctly

echo "🔧 Setting environment variables for FaceValue on Elastic Beanstalk..."

# Check if EB CLI is available
if ! command -v eb &> /dev/null; then
    echo "❌ EB CLI is not installed. Please install it first:"
    echo "   pip install awsebcli"
    exit 1
fi

echo "📝 Setting environment variables..."

# Set all environment variables
eb setenv \
    POSTGRES_USER=postgres \
    POSTGRES_PASSWORD=1WK4hXOKfdnMufeqjZvU \
    POSTGRES_HOST=facevalue.c3uww8i4qmkv.us-west-1.rds.amazonaws.com \
    POSTGRES_PORT=5432 \
    POSTGRES_DB=facevalue \
    DJANGO_SECRET_KEY=yC2ecPbkGxZqmeBu6BaPGJGL7J2zjI-t0zeHu0FjuQFq8daYsK \
    DJANGO_DEBUG=False \
    DEBUG=False \
    DJANGO_ALLOWED_HOSTS=* \
    "ALLOWED_HOSTS=facevalue-api-env.eba-rih4z2ep.us-west-1.elasticbeanstalk.com,*" \
    DJANGO_SETTINGS_MODULE=facevalue.settings \
    PYTHONPATH=/app

echo "✅ Environment variables set successfully!"
echo ""
echo "🔍 You can verify the environment variables with:"
echo "   eb printenv"
echo ""
echo "🚀 Now deploy the application with:"
echo "   ./deploy.sh"
