# Emergency Access and First Time Setup for Serverless Deploys

This document describes the emergency access system for FastOpp, which allows you to recover access to the oppman route when you forget your admin password.

This can also be used to set up the admin user and database for serverless
systems where you do not have shell or ssh command access.

## Overview

The emergency access system provides a secure way to regain access to your admin functions using your `SECRET_KEY` environment variable. This is particularly useful when:

- You forget your admin password
- All admin accounts are locked or inaccessible
- You need to reset user passwords but can't log in normally
- The database hasn't been initialized yet (first-time setup) and you do not have shell access
- You need to create the first superuser account

## Where Emergency Access is Needed for Setup

| service | emergency access needed |
| -- | -- |
| Fly | no. provides shell and ssh |
| Railway | no |
| Leapcell | yes |

## Security Features

- **Disabled by default**: Emergency access is only available when explicitly enabled
- **SECRET_KEY authentication**: Uses your existing SECRET_KEY for authentication
- **Session-based**: Temporary access that can be disabled after use
- **Audit trail**: All emergency access is logged and can be tracked

## How It Works

1. **Token Generation**: Creates a secure token from your SECRET_KEY using SHA-256 hashing
2. **Environment Control**: Only works when `EMERGENCY_ACCESS_ENABLED=true`
3. **Session Management**: Grants temporary access via session cookies
4. **Database Initialization**: Automatically creates database tables if they don't exist
5. **Password Reset**: Allows you to reset any user's password
6. **Superuser Creation**: Allows you to create new superuser accounts
7. **Auto-disable**: Can and should be disabled immediately after use

## Usage Instructions

### Step 1: Enable Emergency Access

Set the environment variable to enable emergency access:

```bash
export EMERGENCY_ACCESS_ENABLED=true
```

Or add it to your `.env` file:

```env
EMERGENCY_ACCESS_ENABLED=true
```

### Step 2: Generate Emergency Token (Optional)

You can generate the emergency token to verify it works:

```bash
uv run python oppman.py emergency
```

This will show you:

- Your current SECRET_KEY
- The generated emergency token
- Instructions for using the system

### Step 3: Access Emergency Interface

1. Visit: `http://localhost:8000/oppman/emergency`
2. Enter your **SECRET_KEY** (not the token) in the form
3. Click "Grant Emergency Access"

### Step 4: Create Superuser or Reset Password

1. You'll be redirected to the emergency dashboard
2. **Database Initialization**: The system will automatically create database tables if they don't exist
3. **Create Superuser** (if no superuser exists):
   - Enter email address and password
   - Click "Create Superuser"
4. **Reset Password** (if superuser exists):
   - Select the user whose password you want to reset
   - Enter a new password (minimum 6 characters)
   - Click "Reset Password"

### Step 5: Logout from Emergency Access

1. Click "Logout from Emergency Access" button
2. Or set `EMERGENCY_ACCESS_ENABLED=false`:
   ```bash
   export EMERGENCY_ACCESS_ENABLED=false
   ```
3. Restart your application

## API Endpoints

### GET `/oppman/emergency`
- **Purpose**: Emergency access login page
- **Requirements**: `EMERGENCY_ACCESS_ENABLED=true`
- **Returns**: HTML form for SECRET_KEY input

### POST `/oppman/emergency/verify`
- **Purpose**: Verify SECRET_KEY and grant emergency access
- **Body**: `token` (your SECRET_KEY)
- **Returns**: JSON response with success status

### GET `/oppman/emergency/dashboard`
- **Purpose**: Emergency dashboard with password reset functionality
- **Requirements**: Valid emergency session
- **Returns**: HTML dashboard with user list and password reset form

### POST `/oppman/emergency/create-superuser`
- **Purpose**: Create superuser via emergency access
- **Body**: `email`, `password`
- **Returns**: JSON response with success status

### POST `/oppman/emergency/reset-password`
- **Purpose**: Reset user password via emergency access
- **Body**: `email`, `new_password`
- **Returns**: JSON response with success status

### POST `/oppman/emergency/logout`
- **Purpose**: Logout from emergency access and clear session
- **Returns**: JSON response confirming logout

## Security Considerations

### When to Use

- ✅ **Forgot admin password**: Use to reset your own password
- ✅ **Account locked**: When admin accounts are inaccessible
- ✅ **Emergency maintenance**: Critical system maintenance needs
- ❌ **Regular access**: Don't use for normal admin tasks
- ❌ **Shared access**: Don't share emergency access with others

### Best Practices

1. **Enable only when needed**: Keep `EMERGENCY_ACCESS_ENABLED=false` by default
2. **Disable immediately**: Turn off emergency access after use
3. **Secure SECRET_KEY**: Keep your SECRET_KEY secure and private
4. **Monitor usage**: Check logs for emergency access usage
5. **Regular rotation**: Consider rotating your SECRET_KEY periodically

### Environment Variables

```env
# Enable/disable emergency access (default: false)
EMERGENCY_ACCESS_ENABLED=true

# Your application secret key (required)
SECRET_KEY=your_secure_secret_key_here
```

## Troubleshooting

### Emergency Access Not Working

1. **Check environment variable**:
   ```bash
   echo $EMERGENCY_ACCESS_ENABLED
   ```

2. **Verify SECRET_KEY**:
   ```bash
   uv run python oppman.py emergency
   ```

3. **Check application logs** for error messages

4. **Restart application** after setting environment variables

### Common Issues

- **404 Error**: Emergency access is disabled (`EMERGENCY_ACCESS_ENABLED=false`)
- **Invalid Token**: Wrong SECRET_KEY entered
- **Session Expired**: Refresh the page and try again
- **Permission Denied**: Check that the user account exists and is active

## Implementation Details

### Token Generation

The emergency access token is generated using:

```python
import hashlib

def generate_emergency_token(secret_key: str) -> str:
    return hashlib.sha256(f"emergency_access_{secret_key}".encode()).hexdigest()
```

### Session Management

Emergency access uses FastAPI sessions with:

- `emergency_access`: Boolean flag for emergency access
- `emergency_granted_at`: Timestamp of when access was granted

### Password Hashing

User passwords are hashed using FastAPI Users' `PasswordHelper`:

```python
from fastapi_users.password import PasswordHelper

password_helper = PasswordHelper()
hashed_password = password_helper.hash(new_password)
```

## Integration with Oppman

The emergency access system integrates seamlessly with the existing oppman route:

- **Same authentication**: Uses the same SECRET_KEY as your application
- **Same database**: Accesses the same user database
- **Same templates**: Uses consistent UI with DaisyUI and TailwindCSS
- **Same security**: Follows the same security practices

## Support

If you encounter issues with the emergency access system:

1. Check the application logs
2. Verify your environment variables
3. Ensure your SECRET_KEY is correct
4. Try restarting the application
5. Contact your system administrator

Remember: Emergency access is a powerful feature that should be used responsibly and disabled when not needed.
