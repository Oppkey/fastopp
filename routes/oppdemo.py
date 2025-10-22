"""
Oppdemo web interface routes
Provides web interface for oppdemo.py functionality
"""
from pathlib import Path

from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from sqlmodel import select

from core.services.auth import get_current_superuser
from dependencies.config import get_settings, Settings
from models import User
from db import AsyncSessionLocal

# Import oppdemo functions
from scripts.init_db import init_db
from scripts.create_superuser import create_superuser
from scripts.check_users import check_users
from scripts.test_auth import test_auth
from demo_scripts.add_test_users import add_test_users
from demo_scripts.add_sample_products import add_sample_products
from demo_scripts.add_sample_webinars import add_sample_webinars
from demo_scripts.add_sample_webinar_registrants import add_sample_registrants
from demo_scripts.clear_and_add_registrants import clear_and_add_registrants
from demo_scripts.download_sample_photos import download_sample_photos

router = APIRouter()
templates = Jinja2Templates(directory="templates")


def ensure_upload_dirs(settings: Settings):
    """Ensure upload directories exist using environment configuration."""
    uploads_root = Path(settings.upload_dir)
    photos_dir = uploads_root / "photos"
    sample_photos_dir = uploads_root / "sample_photos"
    uploads_root.mkdir(parents=True, exist_ok=True)
    photos_dir.mkdir(parents=True, exist_ok=True)
    sample_photos_dir.mkdir(parents=True, exist_ok=True)


@router.get("/oppdemo/", response_class=HTMLResponse)
async def oppdemo_dashboard(
    request: Request,
    current_user: User = Depends(get_current_superuser)
):
    """Oppdemo dashboard - admin only access"""
    return templates.TemplateResponse("oppdemo.html", {
        "request": request,
        "title": "Oppdemo Dashboard",
        "current_page": "oppdemo",
        "user": current_user
    })


@router.post("/oppdemo/init")
async def oppdemo_init(
    request: Request,
    current_user: User = Depends(get_current_superuser),
    settings: Settings = Depends(get_settings)
):
    """Run full oppdemo initialization"""
    try:
        # Ensure upload directories exist
        ensure_upload_dirs(settings)

        # Run initialization steps
        results = []

        # Step 1: Initialize database
        try:
            await init_db()
            results.append({
                "step": "Database Initialization",
                "status": "success",
                "message": "Database initialized successfully"
            })
        except Exception as e:
            results.append({
                "step": "Database Initialization",
                "status": "error",
                "message": f"Failed to initialize database: {str(e)}"
            })
            return JSONResponse({
                "success": False,
                "message": "Database initialization failed",
                "results": results
            })

        # Step 2: Create superuser (if not exists)
        try:
            # Check if superuser already exists
            async with AsyncSessionLocal() as session:
                result = await session.execute(
                    select(User).where(User.is_superuser)
                )
                existing_superusers = result.scalars().all()

                if not existing_superusers:
                    await create_superuser()
                    results.append({
                        "step": "Superuser Creation",
                        "status": "success",
                        "message": "Superuser created successfully"
                    })
                else:
                    results.append({
                        "step": "Superuser Creation",
                        "status": "skipped",
                        "message": f"Superuser(s) already exist: {', '.join([u.email for u in existing_superusers])}"
                    })
        except Exception as e:
            results.append({
                "step": "Superuser Creation",
                "status": "error",
                "message": f"Failed to create superuser: {str(e)}"
            })

        # Step 3: Add test users
        try:
            await add_test_users()
            results.append({
                "step": "Test Users",
                "status": "success",
                "message": "Test users added successfully"
            })
        except Exception as e:
            results.append({
                "step": "Test Users",
                "status": "error",
                "message": f"Failed to add test users: {str(e)}"
            })

        # Step 4: Add sample products
        try:
            await add_sample_products()
            results.append({
                "step": "Sample Products",
                "status": "success",
                "message": "Sample products added successfully"
            })
        except Exception as e:
            results.append({
                "step": "Sample Products",
                "status": "error",
                "message": f"Failed to add sample products: {str(e)}"
            })

        # Step 5: Add sample webinars
        try:
            await add_sample_webinars()
            results.append({
                "step": "Sample Webinars",
                "status": "success",
                "message": "Sample webinars added successfully"
            })
        except Exception as e:
            results.append({
                "step": "Sample Webinars",
                "status": "error",
                "message": f"Failed to add sample webinars: {str(e)}"
            })

        # Step 6: Download sample photos
        try:
            download_sample_photos()
            results.append({
                "step": "Sample Photos",
                "status": "success",
                "message": "Sample photos downloaded successfully"
            })
        except Exception as e:
            results.append({
                "step": "Sample Photos",
                "status": "error",
                "message": f"Failed to download sample photos: {str(e)}"
            })

        # Step 7: Add sample registrants
        try:
            await add_sample_registrants()
            results.append({
                "step": "Sample Registrants",
                "status": "success",
                "message": "Sample registrants added successfully"
            })
        except Exception as e:
            results.append({
                "step": "Sample Registrants",
                "status": "error",
                "message": f"Failed to add sample registrants: {str(e)}"
            })

        # Step 8: Clear and add fresh registrants
        try:
            await clear_and_add_registrants()
            results.append({
                "step": "Fresh Registrants",
                "status": "success",
                "message": "Fresh registrants added successfully"
            })
        except Exception as e:
            results.append({
                "step": "Fresh Registrants",
                "status": "error",
                "message": f"Failed to add fresh registrants: {str(e)}"
            })

        # Check if any steps failed
        failed_steps = [r for r in results if r["status"] == "error"]

        if failed_steps:
            return JSONResponse({
                "success": False,
                "message": f"Initialization completed with {len(failed_steps)} errors",
                "results": results
            })
        else:
            return JSONResponse({
                "success": True,
                "message": "Demo initialization completed successfully!",
                "results": results
            })

    except Exception as e:
        return JSONResponse({
            "success": False,
            "message": f"Initialization failed: {str(e)}",
            "results": results if 'results' in locals() else []
        })


@router.post("/oppdemo/db")
async def oppdemo_db(
    request: Request,
    current_user: User = Depends(get_current_superuser)
):
    """Initialize database only"""
    try:
        await init_db()
        return JSONResponse({
            "success": True,
            "message": "Database initialized successfully"
        })
    except Exception as e:
        return JSONResponse({
            "success": False,
            "message": f"Database initialization failed: {str(e)}"
        })


@router.post("/oppdemo/superuser")
async def oppdemo_superuser(
    request: Request,
    current_user: User = Depends(get_current_superuser)
):
    """Create superuser only"""
    try:
        await create_superuser()
        return JSONResponse({
            "success": True,
            "message": "Superuser created successfully"
        })
    except Exception as e:
        return JSONResponse({
            "success": False,
            "message": f"Superuser creation failed: {str(e)}"
        })


@router.post("/oppdemo/debug-storage")
async def oppdemo_debug_storage(
    request: Request,
    current_user: User = Depends(get_current_superuser)
):
    """Debug storage system"""
    try:
        import os
        from services.storage import get_storage
        
        debug_info = {
            "environment": {
                "STORAGE_TYPE": os.getenv('STORAGE_TYPE', 'NOT SET'),
                "S3_ACCESS_KEY": 'SET' if os.getenv('S3_ACCESS_KEY') else 'NOT SET',
                "S3_SECRET_KEY": 'SET' if os.getenv('S3_SECRET_KEY') else 'NOT SET',
                "S3_BUCKET": os.getenv('S3_BUCKET', 'NOT SET'),
                "S3_CDN_URL": os.getenv('S3_CDN_URL', 'NOT SET'),
            },
            "storage_type": None,
            "sample_photos": {},
            "test_operations": {}
        }
        
        storage = get_storage()
        debug_info["storage_type"] = type(storage).__name__
        
        # Check sample photos
        sample_photos = [
            "sample_photos/john_smith.jpg",
            "sample_photos/sarah_johnson.jpg", 
            "sample_photos/michael_chen.jpg",
            "sample_photos/emily_davis.jpg",
            "sample_photos/david_wilson.jpg"
        ]
        
        for photo_path in sample_photos:
            try:
                exists = storage.file_exists(photo_path)
                debug_info["sample_photos"][photo_path] = {
                    "exists": exists,
                    "error": None
                }
                if exists:
                    try:
                        content = storage.get_file(photo_path)
                        debug_info["sample_photos"][photo_path]["size"] = len(content)
                    except Exception as e:
                        debug_info["sample_photos"][photo_path]["error"] = str(e)
            except Exception as e:
                debug_info["sample_photos"][photo_path] = {
                    "exists": False,
                    "error": str(e)
                }
        
        # Test file operations
        try:
            test_content = b"test content"
            test_path = "sample_photos/debug_test.txt"
            
            # Save test file
            url = storage.save_file(test_content, test_path, "text/plain")
            debug_info["test_operations"]["save"] = {"success": True, "url": url}
            
            # Check if it exists
            exists = storage.file_exists(test_path)
            debug_info["test_operations"]["exists"] = {"success": True, "exists": exists}
            
            # Read it back
            if exists:
                content = storage.get_file(test_path)
                debug_info["test_operations"]["read"] = {"success": True, "size": len(content)}
            
            # Clean up
            storage.delete_file(test_path)
            debug_info["test_operations"]["cleanup"] = {"success": True}
            
        except Exception as e:
            debug_info["test_operations"]["error"] = str(e)
        
        return JSONResponse({
            "success": True,
            "message": "Storage debug completed",
            "debug_info": debug_info
        })
        
    except Exception as e:
        return JSONResponse({
            "success": False,
            "message": f"Storage debug failed: {str(e)}"
        })


@router.post("/oppdemo/users")
async def oppdemo_users(
    request: Request,
    current_user: User = Depends(get_current_superuser)
):
    """Add test users only"""
    try:
        await add_test_users()
        return JSONResponse({
            "success": True,
            "message": "Test users added successfully"
        })
    except Exception as e:
        return JSONResponse({
            "success": False,
            "message": f"Failed to add test users: {str(e)}"
        })


@router.post("/oppdemo/products")
async def oppdemo_products(
    request: Request,
    current_user: User = Depends(get_current_superuser)
):
    """Add sample products only"""
    try:
        await add_sample_products()
        return JSONResponse({
            "success": True,
            "message": "Sample products added successfully"
        })
    except Exception as e:
        return JSONResponse({
            "success": False,
            "message": f"Failed to add sample products: {str(e)}"
        })


@router.post("/oppdemo/webinars")
async def oppdemo_webinars(
    request: Request,
    current_user: User = Depends(get_current_superuser)
):
    """Add sample webinars only"""
    try:
        await add_sample_webinars()
        return JSONResponse({
            "success": True,
            "message": "Sample webinars added successfully"
        })
    except Exception as e:
        return JSONResponse({
            "success": False,
            "message": f"Failed to add sample webinars: {str(e)}"
        })


@router.post("/oppdemo/download-photos")
async def oppdemo_download_photos(
    request: Request,
    current_user: User = Depends(get_current_superuser),
    settings: Settings = Depends(get_settings)
):
    """Download sample photos only"""
    try:
        ensure_upload_dirs(settings)
        download_sample_photos()
        return JSONResponse({
            "success": True,
            "message": "Sample photos downloaded successfully"
        })
    except Exception as e:
        return JSONResponse({
            "success": False,
            "message": f"Failed to download sample photos: {str(e)}"
        })


@router.post("/oppdemo/registrants")
async def oppdemo_registrants(
    request: Request,
    current_user: User = Depends(get_current_superuser)
):
    """Add sample registrants only"""
    try:
        await add_sample_registrants()
        return JSONResponse({
            "success": True,
            "message": "Sample registrants added successfully"
        })
    except Exception as e:
        return JSONResponse({
            "success": False,
            "message": f"Failed to add sample registrants: {str(e)}"
        })


@router.post("/oppdemo/clear-registrants")
async def oppdemo_clear_registrants(
    request: Request,
    current_user: User = Depends(get_current_superuser)
):
    """Clear and add fresh registrants"""
    try:
        await clear_and_add_registrants()
        return JSONResponse({
            "success": True,
            "message": "Fresh registrants added successfully"
        })
    except Exception as e:
        return JSONResponse({
            "success": False,
            "message": f"Failed to add fresh registrants: {str(e)}"
        })


@router.get("/oppdemo/check-users")
async def oppdemo_check_users(
    request: Request,
    current_user: User = Depends(get_current_superuser)
):
    """Check existing users"""
    try:
        await check_users()
        return JSONResponse({
            "success": True,
            "message": "User check completed successfully"
        })
    except Exception as e:
        return JSONResponse({
            "success": False,
            "message": f"User check failed: {str(e)}"
        })


@router.get("/oppdemo/test-auth")
async def oppdemo_test_auth(
    request: Request,
    current_user: User = Depends(get_current_superuser)
):
    """Test authentication system"""
    try:
        await test_auth()
        return JSONResponse({
            "success": True,
            "message": "Authentication test completed successfully"
        })
    except Exception as e:
        return JSONResponse({
            "success": False,
            "message": f"Authentication test failed: {str(e)}"
        })
