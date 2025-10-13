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
# Generate a secure SECRET_KEY
uv run python oppman.py secrets
```

#### Creating requirements.txt for Leapcell

Since Leapcell uses `pip install -r requirements.txt` instead of `uv sync`, you need to export your dependencies:

```bash
# Export dependencies to requirements.txt (use this when you add new packages)
uv export --format requirements.txt --no-hashes > requirements.txt
```

**When to run this command:**
- After adding new packages with `uv add package_name`
- Before deploying to Leapcell
- When updating dependencies

**Note:** The `--no-hashes` option is recommended for Leapcell compatibility, and `--format requirements.txt` ensures the correct format for pip.

### 2. Configure Leapcell Build Settings

Set the following in your Leapcell deployment configuration:

- **Runtime**: Python 3.12 (debian)
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `uvicorn main:app --host 0.0.0.0 --port 8080`
- **Serving Port**: `8080`

### 3. Deploy to Leapcell

Follow the standard Leapcell deployment process for your FastOpp application.

### 4. Initial Admin Setup (No Shell Access)

Since Leapcell doesn't provide shell access, use the emergency access system to create your admin account. The emergency access system provides a secure way to regain access to your admin functions using your `SECRET_KEY` environment variable.

#### How Emergency Access Works

- **Disabled by default**: Emergency access is only available when explicitly enabled
- **SECRET_KEY authentication**: Uses your existing SECRET_KEY for authentication
- **Session-based**: Temporary access that can be disabled after use
- **Database initialization**: Automatically creates database tables if they don't exist
- **Auto-disable**: Should be disabled immediately after use

#### Step 1: Enable Emergency Access

Set the environment variable in your Leapcell dashboard:

```env
EMERGENCY_ACCESS_ENABLED=true
```

#### Step 2: Access Emergency Dashboard

1. Visit: `https://your-app.leapcell.com/oppman/emergency`
2. Enter your **SECRET_KEY** (the same one you used in deployment)
3. Click "Grant Emergency Access"

#### Step 3: Create Superuser

1. You'll be redirected to the emergency dashboard
2. **Database Initialization**: The system will automatically create database tables if they don't exist
3. In the "Create Superuser" section:
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

#### Emergency Access API Endpoints

- **GET `/oppman/emergency`**: Emergency access login page
- **POST `/oppman/emergency/verify`**: Verify SECRET_KEY and grant emergency access
- **GET `/oppman/emergency/dashboard`**: Emergency dashboard with password reset functionality
- **POST `/oppman/emergency/create-superuser`**: Create superuser via emergency access
- **POST `/oppman/emergency/reset-password`**: Reset user password via emergency access
- **POST `/oppman/emergency/logout`**: Logout from emergency access and clear session

## Emergency Access Recovery

If you ever lose access to your admin account:

### 1. Enable Emergency Access

Set in Leapcell environment variables:

```env
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

### Emergency Access Security

- **Emergency access is disabled by default** - only enable when needed
- **SECRET_KEY authentication** - uses your application's SECRET_KEY
- **Session-based access** - temporary and can be cleared
- **Disable immediately after use** - don't leave emergency access enabled

### Security Features

- **Token Generation**: Creates a secure token from your SECRET_KEY using SHA-256 hashing
- **Environment Control**: Only works when `EMERGENCY_ACCESS_ENABLED=true`
- **Session Management**: Grants temporary access via session cookies
- **Database Initialization**: Automatically creates database tables if they don't exist
- **Password Reset**: Allows you to reset any user's password
- **Superuser Creation**: Allows you to create new superuser accounts
- **Auto-disable**: Can and should be disabled immediately after use

### When to Use Emergency Access

- ✅ **Forgot admin password**: Use to reset your own password
- ✅ **Account locked**: When admin accounts are inaccessible
- ✅ **Emergency maintenance**: Critical system maintenance needs
- ✅ **First-time setup**: Creating initial admin account on serverless platforms
- ❌ **Regular access**: Don't use for normal admin tasks
- ❌ **Shared access**: Don't share emergency access with others

### Emergency Access Security Best Practices

1. **Enable only when needed**: Keep `EMERGENCY_ACCESS_ENABLED=false` by default
2. **Disable immediately**: Turn off emergency access after use
3. **Secure SECRET_KEY**: Keep your SECRET_KEY secure and private
4. **Monitor usage**: Check logs for emergency access usage
5. **Regular rotation**: Consider rotating your SECRET_KEY periodically

## Environment Variables

Required for Leapcell deployment:

```env
# Database (provided by Leapcell - uses psycopg driver)
DATABASE_URL=postgresql+psycopg://...

# Security (generate with: uv run python oppman.py secrets)
SECRET_KEY=your_secure_secret_key_here

# Environment
ENVIRONMENT=production

# Emergency access (set to true only when needed)
EMERGENCY_ACCESS_ENABLED=false

# File uploads (Leapcell uses /tmp for temporary storage)
UPLOAD_DIR=/tmp/uploads

# Object Storage (Leapcell S3-compatible storage)
STORAGE_TYPE=s3
S3_ACCESS_KEY=your_leapcell_access_key
S3_SECRET_KEY=your_leapcell_secret_key
S3_BUCKET=your_bucket_name
S3_ENDPOINT_URL=https://objstorage.leapcell.io
S3_CDN_URL=https://your-account.leapcellobj.com/your-bucket
```

## Troubleshooting

### Can't Access Emergency Dashboard

1. **Check environment variable**: Ensure `EMERGENCY_ACCESS_ENABLED=true`
2. **Verify SECRET_KEY**: Make sure you're using the correct SECRET_KEY
3. **Check application logs**: Look for any error messages
4. **Restart application**: After changing environment variables

### Emergency Access Not Working

1. **Check environment variable**:

   ```bash
   echo $EMERGENCY_ACCESS_ENABLED
   ```

2. **Verify SECRET_KEY**: Use `uv run python oppman.py emergency` locally to check

3. **Check application status**: Ensure your app is running properly

4. **Environment variables**: Confirm `EMERGENCY_ACCESS_ENABLED=true` is set

5. **Application restart**: Restart after changing environment variables

### Common Emergency Access Issues

- **404 Error**: Emergency access is disabled (`EMERGENCY_ACCESS_ENABLED=false`)
- **Invalid Token**: Wrong SECRET_KEY entered
- **Session Expired**: Refresh the page and try again
- **Permission Denied**: Check that the user account exists and is active

### Can't Create Superuser

1. **Check email format**: Ensure valid email address
2. **Password requirements**: Minimum 6 characters
3. **User already exists**: Check if email is already in use
4. **Database connection**: Verify database is accessible

## Best Practices

### General Security

1. **Keep SECRET_KEY secure**: Never commit it to version control
2. **Use strong passwords**: For both SECRET_KEY and admin accounts
3. **Regular backups**: Use Leapcell's backup features
4. **Monitor logs**: Check application logs regularly

### Emergency Access Best Practices

1. **Disable emergency access**: Only enable when needed
2. **Disable immediately after use**: Turn off emergency access after completing setup
3. **Never share emergency access**: Don't share emergency access with others
4. **Use for emergencies only**: Don't use for regular admin tasks

## Support

If you encounter issues:

1. Check the [Emergency Access Documentation](../EMERGENCY_ACCESS.md)
2. Review Leapcell's documentation
3. Check your application logs
4. Verify environment variables are set correctly
