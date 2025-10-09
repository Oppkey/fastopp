# Leapcell Deployment Guide

This guide covers deploying FastOpp to Leapcell, a platform that provides free hosting with PostgreSQL and object storage.

## Prerequisites

- Leapcell account
- Your FastOpp application code
- SECRET_KEY for your application

## Deployment Steps

### 1. Prepare Your Application

Ensure your application is ready for production:

```bash
# Install dependencies
uv sync

# Generate a secure SECRET_KEY
uv run python oppman.py secrets
```

### 2. Deploy to Leapcell

Follow the standard Leapcell deployment process for your FastOpp application.

### 3. Initial Admin Setup (No Shell Access)

Since Leapcell doesn't provide shell access, use the emergency access system to create your admin account:

#### Step 1: Enable Emergency Access

Set the environment variable in your Leapcell dashboard:
```
EMERGENCY_ACCESS_ENABLED=true
```

#### Step 2: Access Emergency Dashboard

1. Visit: `https://your-app.leapcell.com/oppman/emergency`
2. Enter your **SECRET_KEY** (the same one you used in deployment)
3. Click "Grant Emergency Access"

#### Step 3: Create Superuser

1. You'll be redirected to the emergency dashboard
2. In the "Create Superuser" section:
   - Enter your admin email address
   - Enter a secure password (minimum 6 characters)
   - Click "Create Superuser"

#### Step 4: Verify Access

1. Visit: `https://your-app.leapcell.com/admin/`
2. Login with your new superuser credentials
3. Verify you have full admin access

#### Step 5: Disable Emergency Access

1. In the emergency dashboard, click "Logout from Emergency Access"
2. Set `EMERGENCY_ACCESS_ENABLED=false` in your Leapcell environment variables
3. Restart your application

## Emergency Access Recovery

If you ever lose access to your admin account:

### 1. Enable Emergency Access

Set in Leapcell environment variables:
```
EMERGENCY_ACCESS_ENABLED=true
```

### 2. Access Emergency Dashboard

1. Visit: `https://your-app.leapcell.com/oppman/emergency`
2. Enter your SECRET_KEY
3. Click "Grant Emergency Access"

### 3. Reset Password or Create New Superuser

- **Reset Password**: Select existing user and set new password
- **Create Superuser**: If no superuser exists, create a new one

### 4. Disable Emergency Access

1. Click "Logout from Emergency Access"
2. Set `EMERGENCY_ACCESS_ENABLED=false`
3. Restart application

## Security Notes

- **Emergency access is disabled by default** - only enable when needed
- **SECRET_KEY authentication** - uses your application's SECRET_KEY
- **Session-based access** - temporary and can be cleared
- **Disable immediately after use** - don't leave emergency access enabled

## Environment Variables

Required for Leapcell deployment:

```env
# Database (provided by Leapcell)
DATABASE_URL=postgresql://...

# Security (generate with: uv run python oppman.py secrets)
SECRET_KEY=your_secure_secret_key_here

# Environment
ENVIRONMENT=production

# Emergency access (set to true only when needed)
EMERGENCY_ACCESS_ENABLED=false

# Optional: File uploads
UPLOAD_DIR=/app/uploads
```

## Troubleshooting

### Can't Access Emergency Dashboard

1. **Check environment variable**: Ensure `EMERGENCY_ACCESS_ENABLED=true`
2. **Verify SECRET_KEY**: Make sure you're using the correct SECRET_KEY
3. **Check application logs**: Look for any error messages
4. **Restart application**: After changing environment variables

### Emergency Access Not Working

1. **Verify SECRET_KEY**: Use `uv run python oppman.py emergency` locally to check
2. **Check application status**: Ensure your app is running properly
3. **Environment variables**: Confirm `EMERGENCY_ACCESS_ENABLED=true` is set
4. **Application restart**: Restart after changing environment variables

### Can't Create Superuser

1. **Check email format**: Ensure valid email address
2. **Password requirements**: Minimum 6 characters
3. **User already exists**: Check if email is already in use
4. **Database connection**: Verify database is accessible

## Best Practices

1. **Keep SECRET_KEY secure**: Never commit it to version control
2. **Use strong passwords**: For both SECRET_KEY and admin accounts
3. **Disable emergency access**: Only enable when needed
4. **Regular backups**: Use Leapcell's backup features
5. **Monitor logs**: Check application logs regularly

## Support

If you encounter issues:

1. Check the [Emergency Access Documentation](../EMERGENCY_ACCESS.md)
2. Review Leapcell's documentation
3. Check your application logs
4. Verify environment variables are set correctly
