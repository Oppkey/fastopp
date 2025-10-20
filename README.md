# FastOpp - Easier AI Web Apps for Students

![FastOpp Logo](https://raw.githubusercontent.com/Oppkey/fastopp/refs/heads/main/docs/images/fastopp_logo.webp)

## Quick Install

### with uv (recommended)

If you don't have uv installed:

`curl -LsSf https://astral.sh/uv/install.sh | less`

```bash
mkdir my-project && cd my-project
uv init
uv add fastopp
uv run fastopp-startproject
uv run python oppman.py runserver
```

### with pip



## What

FastAPI starter package for students prototyping AI web applications. Pre-built admin
components give FastAPI functionality comparable to Django
for AI-first applications.

## Problem Solved

Django and Flask are not designed for optimized async LLM applications.

## Overview

Although both Django and Flask can absolutely be used for complex AI
applications and are great in many, many ways, there are often rough patches during
development of asynchronous AI applications that communicate with backend LLMs available
at OpenAI, Anthropic, and OpenRouter.

FastAPI has advantages in future-proof architecture, but can
have a steep learning curve for people, especially for
developers familiar with Django.

FastOpp provides an opinionated framework for FastAPI with the following features:

* admin panel similar to Django with role-based authentication
* SQL database with Django-inspired models and migrations
* Django-style HTML templates with modern UI components
  * Replaceable style templates to get started
* API endpoints to connect to other frontend frameworks
  * auto-generated documentation for API endpoints
  * designed to connect to Flutter and React in the future, but we do not have examples
* **oppman.py** core management tool for database, users, and application setup
* **oppdemo.py** demo file management tool for switching between demo and minimal modes

## Target Audience

This stack is opinionated and may not be for you. It is intended for students and novice developers who
know Python, but are not strong in or do not like JavaScript.

**FastOpp is not intended for production use or for experienced developers.**

* You strongly prefer Python over JavaScript on the backend
* You prefer to handle logic on the Python backend instead of using JavaScript code on the frontend
* You prefer inline styling instead of separation of concerns with CSS in separate files
* You prefer typed languages and want to use Python optional type hints instead of relying only on dynamic typing
* You prefer HTML files with Python code and variables embedded in the HTML instead of embedding HTML in the Python code on the server
* You are using Django or Flask and are having problems with async LLM communication
* You started with [Streamlit](https://streamlit.io/) or [Gradio](https://www.gradio.app/). Your code became more complex and is now difficult to manage

## Example Use Cases

* **University student** looking to build resume - Show potential employers that you can
  build an AI application. You want to host it cheaply and use cheap or free
  LLMs with the option
  to use a higher-quality LLM before you showoff your project.
  You have an idea on how to use AI and want to show it to people.
* **Hobbyist** looking to vibe code simple AI utility - Provide Cursor or equivalent
  access to demos and start with an opinionated structure for files and UI.
  Enforce vibe-code behavior with rules so that you can go back and edit your
  code. Deploy cheaply for less than $1 and month and scale up if your idea take off.
* **Small business entrepreneur** - You have
  great business ideas, but you are not a great programmer.
  You want to put AI into a business workflow that you are familiar with and show other
  people to get more help.

## FAQ and Concerns

### I'm concerned that this project is new and I don't want to waste time if it dies

The project is intended to teach use of FastAPI with LLMs.  The knowledge you gain will be
highly relevant to employers as long as Python and LLMs continue to be used together.
We intend that you eventually move off of Jinja2 templates and use the built-in API
for interfaces with React-variants or something like Flutter for mobile or web apps.
The project is intended to get you started on your path.  Even if it dies, your
knowledge will live on.

### I'm concerned about security

To be honest, we are not confident in the security architecture and model.  It is
sufficient for learning purposes, but you need to look into security yourself
and use another model if your project takes off.  FastOpp will get you started
quickly, but it is not intended for long-term production use.

### Should I use PostgreSQL instead of SQLite?

Yes. We use SQLite to get you started because there are less installation dependencies.
If you use the database in production,
we recommend switching to PostgreSQL.

### Should I use NGINX instead of serving the HTML templates from FastAPI?

Yes. We use FastAPI in deployment tutorials to get you started. NGINX is better.
FastAPI is very usable without NGINX if you do not have many simultaneous users.

### Should I change the LLM from LLama3.3-70b-instruct:free?

Yes. The free LLM is set for easy setup. We do not use it in production.  
At a minimum, you should
change this to the paid version of LLama3.3-70b-instruct or your
app will have very limited functionality.  If you password-protect your
app, you can control costs.  If only a few people use the app, the
free version will work.  LLama3.3-70b is pretty good, not great. It's primary
quality is that it is much cheaper than top-tier great LLMs like [GPT-5](https://openrouter.ai/openai/gpt-5).

### Can I use FastOpp in my own business?

Yes.  FastOpp itself is under the MIT license. You can modify FastOpp and close it off if that helps
your business or personal goals.  Refer to pyproject.toml for a list of FastOpp dependencies and confirm compliance for your use.

## Screenshots of Included Design Examples and Functionality Demos

FastOpp can be viewed as an opinionated design framework that adds an UI to an SQL
database (or vector db with extensions) and a UI to the input and
output of an LLM.

### Clickable Cards with Mouseover

![home](https://raw.githubusercontent.com/Oppkey/fastopp/refs/heads/main/docs/images/readme/home.webp)

### Change Images Without Page Reload

![interactive](https://raw.githubusercontent.com/Oppkey/fastopp/refs/heads/main/docs/images/interactive.webp)

### Hero

![hero](https://raw.githubusercontent.com/Oppkey/fastopp/main/docs/images/readme/hero.webp)

### Database Admin List

![admin list](https://raw.githubusercontent.com/Oppkey/fastopp/main/docs/images/admin.webp)

### Database Entry Edit

![edit](https://raw.githubusercontent.com/Oppkey/fastopp/main/docs/images/edit.webp)

### User Management

![user management](https://raw.githubusercontent.com/Oppkey/fastopp/main/docs/images/user_management.webp)

### User Authentication

Admin panel is restricted to logged-in users.

![authentication](https://raw.githubusercontent.com/Oppkey/fastopp/main/docs/images/login.webp)

### Statistics Hero Card

![webinar top](https://raw.githubusercontent.com/Oppkey/fastopp/main/docs/images/webinar_top.webp)

### People Hero Card

![webinar people](https://raw.githubusercontent.com/Oppkey/fastopp/main/docs/images/webinar_people.webp)

### AI Chat with Cloud-Based LLM

![AI Chat](https://raw.githubusercontent.com/Oppkey/fastopp/main/docs/images/ai_chat_indents.webp)

![AI Chat](https://raw.githubusercontent.com/Oppkey/fastopp/main/docs/images/ai_chat.webp)

### Emergency Access From Web Browser

* create admin if you forgot password or have no shell or database access
* ability to disable access with environment variable

![emergency login](https://raw.githubusercontent.com/Oppkey/fastopp/main/docs/images/readme/emergency_login.webp)

### Admin Dashhboards to Change Password and Manage Database

![oppman web admin](https://raw.githubusercontent.com/Oppkey/fastopp/main/docs/images/readme/password_migration.webp)

### Manage Reference Demos From WebUI

Create fake data for testing

* fake users
* fake webinar registrants
* fake products for sales and marketing tests

![oppdemo dashboard](https://raw.githubusercontent.com/Oppkey/fastopp/main/docs/images/readme/oppdemo.webp)

## Basic Design System and Reference Template

FastOpp comes with an optional basic UI design system to accelerate AI application development.

* based on Tailwind CSS, DaisyUI, AlpineJS and HTMX

## 🚀 Quick Start (For Students)

### Prerequisites

* Python 3.12+
  If Python 3.12+ is not on your Mac, consider [installing pyenv](https://youtu.be/1F2IK7CU76U?feature=shared)
  and install the newest 3.12.x with pyenv. Although the latest stable Python is 3.13.7, we're using 3.12.x
  right now for maximum package compatibility.
* [uv](https://docs.astral.sh/uv/) package manager

### 1. Fork, Clone, Add Upstream, Sync

Fork it!

Go to https://github.com/Oppkey/fastopp  
Click Fork in GitHub UI    
You'll get github.com/yourusername/fastopp  

Clone your fork down to your local machine

`git clone https://github.com/yourusername/fastopp.git`  
`cd fastopp`

Add upstream remote

`git remote add upstream https://github.com/Oppkey/fastopp.git`

Sync your fork with upstream before new work

`git fetch upstream`  
`git checkout main`  
`git merge upstream/main`  

### 2. Environment Configuration

Create a `.env` file in your project root:

**Required Environment Variables:**

* `DATABASE_URL`: Database connection string
* `SECRET_KEY`: Secret key for JWT tokens and session management
* `ENVIRONMENT`: Set to "development" for development mode
* `OPENROUTER_API_KEY`: API key for OpenRouter (required for AI demo features)

**Optional Environment Variables:**

* `UPLOAD_DIR`: Directory for storing uploaded files (defaults to `static/uploads` if not set)
  * **Local Development**: Not set (uses default `static/uploads`)
  * **Production Deployments**: Set to persistent storage path (e.g., `/data/uploads`, `/app/uploads`)
  * **URL Compatibility**: Files are always served from `/static/uploads/photos/` regardless of storage location

#### Generate Secure SECRET_KEY

**Recommended**: Use the built-in secret generator for maximum security:

```bash
# Generate a cryptographically secure SECRET_KEY
uv run python oppman.py secrets
```

This will output a line like `SECRET_KEY=...` that you can copy directly into your `.env` file.

**Alternative methods:**

```bash
# Create environment file with secure defaults
cat > .env << EOF
DATABASE_URL=sqlite+aiosqlite:///./test.db
SECRET_KEY=$(uv run python oppman.py secrets | grep SECRET_KEY | cut -d'=' -f2)
ENVIRONMENT=development
OPENROUTER_API_KEY=your_openrouter_api_key_here
EOF
```

**Using the example configuration:**

```bash
# Copy the example environment file
cp example.env .env

# Edit the .env file with your values
nano .env  # or use your preferred editor
```

The `example.env` file contains all available configuration options with detailed comments and examples.

**Or manually create `.env`:**

```bash
# .env
DATABASE_URL=sqlite+aiosqlite:///./test.db
SECRET_KEY=your_generated_secret_key_here
ENVIRONMENT=development
OPENROUTER_API_KEY=your_openrouter_api_key_here
```

**⚠️ Security Important:**

* Never commit `.env` files to version control
* Add `.env` to your `.gitignore` file
* Keep your SECRET_KEY secure and private
* Use different SECRET_KEYs for different environments

### 3. One-Command Setup

```bash
# Complete setup with one command
uv run python oppdemo.py init
```

This single command will:

* Initialize migrations
* Create initial migration
* Apply migrations
* Initialize database with sample data
* Create superuser and test data

#### Alternative: Step-by-Step Setup

If you prefer to understand each step:

```bash
# Initialize migrations (first time only)
uv run python oppman.py migrate init

# Create initial migration
uv run python oppman.py migrate create "Initial migration"

# Apply migrations
uv run python oppman.py migrate upgrade

# Initialize database with sample data
uv run python oppdemo.py init
```

**Note**: Demo data initialization commands have been moved from `oppman.py` to `oppdemo.py` for better separation of concerns.

### 4. Start Development Server

```bash
# Start the server
uv run python oppman.py runserver
```

### 5. Access the Application

Visit these URLs in your browser:

* **Homepage**: `http://localhost:8000/`
* **Admin Panel**: `http://localhost:8000/admin/`
* **API Docs**: `http://localhost:8000/docs`

#### Admin Panel Login

Use these credentials to access the admin panel:

* **Email**: `admin@example.com`
* **Password**: `admin123`

## 🛠️ Management Commands

FastOpp now uses two separate management tools for better organization and separation of concerns:

### Core Application Management (oppman.py)

**oppman.py** is similar to Django's manage.py and focuses on core application management:

```bash
# Server management
uv run python oppman.py runserver       # Start development server
uv run python oppman.py stopserver      # Stop development server
uv run python oppman.py production      # Start production server

# Database management
uv run python oppman.py backup          # Backup database
uv run python oppman.py delete          # Delete database (with backup)

# Migration management
uv run python oppman.py migrate init    # Initialize migrations
uv run python oppman.py migrate create "Add new table"  # Create migration
uv run python oppman.py migrate upgrade # Apply migrations
uv run python oppman.py migrate current # Check migration status

# Environment and utilities
uv run python oppman.py env             # Check environment configuration
uv run python oppman.py secrets         # Generate SECRET_KEY for .env file
uv run python oppman.py demo            # Show demo command help
uv run python oppman.py help            # Show comprehensive help
```

### Demo Management (oppdemo.py)

**oppdemo.py** handles all demo-related functionality:

```bash
# Demo file management
uv run python oppdemo.py save           # Save demo files to demo_assets
uv run python oppdemo.py restore        # Restore demo files from backup
uv run python oppdemo.py destroy        # Switch to minimal application
uv run python oppdemo.py diff           # Show differences between current and backup
uv run python oppdemo.py backups        # List all available backups

# Demo data initialization (moved from oppman.py)
uv run python oppdemo.py init           # Complete initialization (database + superuser + users + products + webinars + registrants)
uv run python oppdemo.py db             # Initialize database only
uv run python oppdemo.py superuser      # Create superuser only
uv run python oppdemo.py users          # Add test users only
uv run python oppdemo.py products       # Add sample products only
uv run python oppdemo.py webinars       # Add sample webinars only
uv run python oppdemo.py download_photos # Download sample photos
uv run python oppdemo.py registrants    # Add sample registrants
uv run python oppdemo.py clear_registrants # Clear and add fresh registrants
uv run python oppdemo.py check_users    # Check existing users
uv run python oppdemo.py test_auth      # Test authentication
uv run python oppdemo.py change_password # Change user password
uv run python oppdemo.py list_users     # List all users

# Help
uv run python oppdemo.py help           # Show comprehensive help
```

### Server Management

```bash
# Development server
uv run python oppman.py runserver       # Start development server
uv run python oppman.py stopserver      # Stop development server

# Production server (optional)
uv run python oppman.py production      # Start production server
```

### Migration Management

```bash
# Initialize migrations (first time only)
uv run python oppman.py migrate init

# Create new migration
uv run python oppman.py migrate create "Add new table"

# Apply migrations
uv run python oppman.py migrate upgrade

# Check migration status
uv run python oppman.py migrate current

# View migration history
uv run python oppman.py migrate history
```

### Environment Management

```bash
# Check environment configuration
uv run python oppman.py env

# Generate secure SECRET_KEY for .env file
uv run python oppman.py secrets

# Show all available commands
uv run python oppman.py help
```

### Backup Management

Backup files are automatically organized in the `backups/` directory:

* **`backups/destroy/`** - Files backed up before switching to minimal mode
* **`backups/restore/`** - Files backed up before restoring demo mode

Each backup includes a timestamp for easy identification. Use `uv run python oppdemo.py backups` to list all available backups.

## 📊 Test Data

The application comes with pre-loaded test data:

### Users

* **Superuser**: `admin@example.com` / `admin123`
* **Test Users**: `john@example.com`, `jane@example.com`, `bob@example.com` / `test123`

### Products

Sample products with various categories and prices for testing the admin interface.

## 🛠️ Tool Separation

FastOpp now uses two separate management tools for better organization and separation of concerns:

### oppman.py - Core Application Management

**oppman.py** is similar to Django's manage.py and focuses on core application management:

* **Server Management**: Start/stop development and production servers
* **Database Management**: Backup, delete, and migration operations
* **Environment Management**: Configuration checks and utilities
* **Core Operations**: Essential application lifecycle management

### oppdemo.py - Demo Management

**oppdemo.py** handles all demo-related functionality:

* **Demo File Management**: Save/restore demo state, switch between demo and minimal modes
* **Demo Data Initialization**: All sample data creation (users, products, webinars, registrants)
* **Demo State Control**: Comprehensive demo application management

## 🔄 Database Migrations

### Migration Workflow

1. **Add/Modify Models**: Edit `models.py` with your changes
2. **Create Migration**: `uv run python oppman.py migrate create "Description"`
3. **Review Migration**: Check the generated file in `alembic/versions/`
4. **Apply Migration**: `uv run python oppman.py migrate upgrade`
5. **Verify**: `uv run python oppman.py migrate current`

### Making a Pull Request

Create a feature branch

`git checkout -b feature/your-change`

Make changes → commit

`git add .`  
`git commit -m "Your change description"`

Push feature branch to your fork

`git push origin feature/your-change`

Open a Pull Request (PR)

In GitHub, go to your fork yourusername/fastopp.  
Click “Compare & pull request”.  

Base: Oppkey/fastopp:main  
Head: yourusername/fastopp:feature/your-change  

Fill title, description, link issues. Submit.  

If upstream changes during review, sync your branch  

`git fetch upstream`  
`git checkout feature/your-change`  
`git merge upstream/main`  
`git push origin feature/your-change`  

After PR is merged  

`git checkout main`  
`git fetch upstream`  
`git merge upstream/main`  
`git branch -d feature/your-change`  
`git push origin --delete feature/your-change`  

## 🚨 Troubleshooting

### Common Issues

1. **"Alembic not found"**

   ```bash
   uv add alembic
   ```

2. **"Alembic not initialized"**

   ```bash
   uv run python oppman.py migrate init
   ```

3. **Environment issues**

     ```bash
     # Check environment configuration
     uv run python oppman.py env
     ```

4. **Database issues**

     ```bash
     # Backup and reset
     uv run python oppman.py backup
     uv run python oppman.py delete
     uv run python oppman.py init
     ```

5. **"Module not found" errors**

   ```bash
   # Reinstall dependencies
   uv sync
   ```

6. **Port already in use**

    ```bash
    # Stop any running servers
    uv run python oppman.py stopserver
    
    or
    
    # Kill uvicorn processes manually
    pkill -f uvicorn

    or
     
    # use a different port
    uv run uvicorn main:app --reload --port 8001
    ```

### Quick Reset

FastOpp is a learning tool designed for tinkering, you can play around
with the demo and then restore the entire demo or just the database to a working state:

```bash
# Backup current database
uv run python oppman.py backup

# Delete database and reinitialize
uv run python oppman.py delete # delete SQL database

# initialize blank database
uv run python oppdemo.py db

or

# initializes and puts in fake data
uv run python oppdemo.py init 

# Verify setup
uv run python oppman.py env
```

## 📁 File Uploads and Storage

FastOpp includes a flexible file upload system that works across different deployment environments:

### How It Works

* **Local Development**: Files stored in `static/uploads/` directory (default behavior)
* **Production Deployments**: Files stored in configurable directory via `UPLOAD_DIR` environment variable
* **URL Consistency**: All uploads served from `/static/uploads/photos/` regardless of storage location

### Configuration Examples

```bash
# Local development (no environment variable needed)
# Files stored in: static/uploads/photos/
# URLs served from: /static/uploads/photos/

# Docker deployment
UPLOAD_DIR=/app/uploads
# Files stored in: /app/uploads/photos/
# URLs served from: /static/uploads/photos/

# Fly.io deployment with persistent Fly Volume mounted at /data
UPLOAD_DIR=/data/uploads
# Files stored in: /data/uploads/photos/
# URLs served from: /static/uploads/photos/

# Kubernetes deployment
UPLOAD_DIR=/persistent/uploads
# Files stored in: /persistent/uploads/photos/
# URLs served from: /static/uploads/photos/
```

### Benefits

* **Environment-agnostic**: Works in any deployment environment
* **Backward compatible**: Local development unchanged
* **Persistent storage**: Production deployments can use persistent volumes
* **URL consistency**: Frontend code doesn't need to change

## 🔄 Demo vs Minimal Mode

FastOpp supports two application modes:

### Demo Mode (Default)

* Full-featured application with AI chat, dashboard, design examples
* Sample data and comprehensive UI components
* Ideal for learning and showcasing features

### Minimal Mode

* Basic FastAPI application with authentication
* Clean slate for building your own application
* Includes admin panel and basic structure with password-protected pages

### Switching Between Modes

```bash
# Save current demo state
uv run python oppdemo.py save

# Switch to minimal mode
uv run python oppdemo.py destroy

# Restore demo mode
uv run python oppdemo.py restore

# Check what's different
uv run python oppdemo.py diff
```

## 📚 Documentation

### Courseware - YouTube Video Tutorials

* [FastAPI for AI LLM Apps with SQLAdmin, SQLModel - Quickstart Template for Frontend](https://youtu.be/_P9p0BGO64Q) - published August 15, 2025
* [FastAPI with LLM and Database Beginner Tutorial](https://youtu.be/_NlY0zlcC6Q) - published August 18, 2025
* [Deploy FastAPI and SQLite to Fly for Cheap Hosting](https://youtu.be/k-6xxE6k7Fs) - published August 26, 2025
* [Permanent Photo Uploads on Fly with FastAPI Static Files on Fly Volume](https://youtu.be/YKC3ZSA2Eh8) - published August 29, 2025
* [Free FastAPI Deployment - No Credit Card - Railway](https://youtu.be/7vxroD-tyo8) - published Sept 3, 2025
* [FastAPI Deploy to Leapcell - free hosting tier](https://youtu.be/xhOALd640tA)
* [Free  Deploy to Leapcell with FastAPI, PostgreSQL and Object Storage](https://youtu.be/GoKpQTHE-1A)

### Tutorials

* [Add new page](docs/tutorials/add_new_page.md)
* [Change LLM](docs/tutorials/change_llm.md)

### Deployment

* [Deploy to fly.io](docs/deployment/FLY_DEPLOYMENT.md)
* [fly deployment costs discussion](https://github.com/Oppkey/fastopp/discussions/25)

### Architecture and Overview

* [Architecture Overview](docs/ARCHITECTURE.md) - MVS Architecture and code organization
* [Database](docs/DATABASE.md)
* [Authentication](docs/AUTHENTICATION.md)
* [Emergency Access](docs/EMERGENCY_ACCESS.md) - Password recovery system for admin access
* [Features](docs/FEATURES.md)

## Guidelines

* beautiful
* cheap
* easy
* opinionated
