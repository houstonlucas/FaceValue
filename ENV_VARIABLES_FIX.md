# Environment Variables Fix for Elastic Beanstalk

## Problem
The Django application was running in a Docker container on Elastic Beanstalk, but environment variables weren't being passed from the host `.env` file into the container. This caused the application to use default/fallback values instead of the production database and configuration settings.

## Root Cause
1. The `docker-compose.yml` file didn't specify environment variables to pass to the container
2. The `.env` file on the host was not being loaded into the Docker container
3. Elastic Beanstalk environment variables weren't configured

## Solution

### 1. Updated docker-compose.yml
Added environment variable mapping to ensure all Django settings are passed to the container:

```yaml
environment:
  - POSTGRES_USER=${POSTGRES_USER:-postgres}
  - DJANGO_SETTINGS_MODULE=${DJANGO_SETTINGS_MODULE:-facevalue.settings}
  - PYTHONPATH=${PYTHONPATH:-/app}
  - DJANGO_ALLOWED_HOSTS=${DJANGO_ALLOWED_HOSTS:-*}
  - POSTGRES_HOST=${POSTGRES_HOST:-localhost}
  - DJANGO_SECRET_KEY=${DJANGO_SECRET_KEY:-django-insecure-change-this-in-production}
  - ALLOWED_HOSTS=${ALLOWED_HOSTS:-*}
  - POSTGRES_PASSWORD=${POSTGRES_PASSWORD}
  - POSTGRES_PORT=${POSTGRES_PORT:-5432}
  - DJANGO_DEBUG=${DJANGO_DEBUG:-False}
  - POSTGRES_DB=${POSTGRES_DB:-facevalue}
  - DEBUG=${DEBUG:-False}
```

### 2. Updated .env file
Updated with production values for the RDS database and Elastic Beanstalk configuration.

### 3. Set Environment Variables on Elastic Beanstalk

Run the provided script to set environment variables:
```bash
./set-env.sh
```

Or set them manually via EB CLI:
```bash
eb setenv POSTGRES_USER=postgres \
          POSTGRES_PASSWORD=your-postgres-password \
          POSTGRES_HOST=facevalue.c3uww8i4qmkv.us-west-1.rds.amazonaws.com \
          # ... (see set-env.sh for complete list)
```

### 4. Deploy the Updated Application
```bash
./deploy.sh
```

## Verification

After deployment, SSH into the EC2 instance and verify:

1. **Check environment variables in container:**
```bash
sudo docker exec $(sudo docker ps -q) env | grep -E '(DJANGO|POSTGRES|DEBUG)'
```

2. **Test Django settings:**
```bash
sudo docker exec $(sudo docker ps -q) python -c "
import os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'facevalue.settings')
django.setup()
from django.conf import settings
print('SECRET_KEY set:', bool(settings.SECRET_KEY))
print('DEBUG:', settings.DEBUG)
print('DATABASES:', settings.DATABASES['default']['ENGINE'])
print('HOST:', settings.DATABASES['default']['HOST'])
"
```

3. **Check health endpoint:**
```bash
curl -f http://localhost:8000/healthz/
```

## Files Modified
- `docker-compose.yml` - Added environment variable mapping
- `.env` - Updated with production values
- `deploy.sh` - Created deployment script
- `set-env.sh` - Created environment variable setup script

## Next Steps
- Update the `DJANGO_SECRET_KEY` with a proper production secret
- Consider using AWS Systems Manager Parameter Store for sensitive environment variables
- Set up proper logging and monitoring for the production environment
