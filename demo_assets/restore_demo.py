#!/usr/bin/env python3
"""
Demo Restoration Script

This script restores all demo files from the demo_assets backup to their original locations.
Run this script from the project root directory.
"""

from pathlib import Path
import shutil
import sys


def restore_demo_files():
    """Restore all demo files from demo_assets backup"""
    
    # Get the project root directory
    project_root = Path.cwd()
    demo_assets = project_root / "demo_assets"
    
    if not demo_assets.exists():
        print("❌ Error: demo_assets directory not found!")
        print("Please run this script from the project root directory.")
        sys.exit(1)
    
    print("🔄 Restoring demo files from backup...")
    
    # Restore templates
    print("📄 Restoring templates...")
    templates_src = demo_assets / "templates"
    templates_dest = project_root / "templates"
    
    if templates_src.exists():
        # Copy individual template files
        for template_file in templates_src.glob("*.html"):
            dest_file = templates_dest / template_file.name
            shutil.copy2(template_file, dest_file)
            print(f"  ✅ Restored {template_file.name}")
        
        # Copy partials directory
        partials_src = templates_src / "partials"
        partials_dest = templates_dest / "partials"
        
        if partials_src.exists():
            if partials_dest.exists():
                shutil.rmtree(partials_dest)
            shutil.copytree(partials_src, partials_dest)
            print("  ✅ Restored partials/")
    
    # Restore static files
    print("🎨 Restoring static files...")
    static_src = demo_assets / "static"
    static_dest = project_root / "static"
    
    if static_src.exists():
        # Copy images
        images_src = static_src / "images"
        images_dest = static_dest / "images"
        
        if images_src.exists():
            if images_dest.exists():
                shutil.rmtree(images_dest)
            shutil.copytree(images_src, images_dest)
            print("  ✅ Restored images/")
        
        # Copy other static files
        for static_file in static_src.glob("*"):
            if static_file.is_file() and static_file.name != "uploads":
                dest_file = static_dest / static_file.name
                shutil.copy2(static_file, dest_file)
                print(f"  ✅ Restored {static_file.name}")
        
        # Copy CSS and JS directories
        for subdir in ["css", "js"]:
            subdir_src = static_src / subdir
            subdir_dest = static_dest / subdir
            
            if subdir_src.exists():
                if subdir_dest.exists():
                    shutil.rmtree(subdir_dest)
                shutil.copytree(subdir_src, subdir_dest)
                print(f"  ✅ Restored {subdir}/")
    
    # Restore routes
    print("🛣️  Restoring routes...")
    routes_src = demo_assets / "routes"
    routes_dest = project_root / "routes"
    
    if routes_src.exists():
        for route_file in routes_src.glob("*.py"):
            dest_file = routes_dest / route_file.name
            shutil.copy2(route_file, dest_file)
            print(f"  ✅ Restored {route_file.name}")
    
    # Restore services (application-specific services only, core services remain in core/)
    print("🔧 Restoring services...")
    services_src = demo_assets / "services"
    services_dest = project_root / "services"
    
    if services_src.exists():
        for service_file in services_src.glob("*.py"):
            dest_file = services_dest / service_file.name
            shutil.copy2(service_file, dest_file)
            print(f"  ✅ Restored {service_file.name}")
    
    # Restore models
    print("📊 Restoring models...")
    models_src = demo_assets / "models.py"
    models_dest = project_root / "models.py"
    
    if models_src.exists():
        shutil.copy2(models_src, models_dest)
        print("  ✅ Restored models.py")
    
    # Copy sample data scripts
    print("📝 Restoring sample data scripts...")
    scripts_src = demo_assets / "scripts"
    scripts_dest = project_root / "scripts"
    
    if scripts_src.exists():
        for script_file in scripts_src.glob("*.py"):
            dest_file = scripts_dest / script_file.name
            shutil.copy2(script_file, dest_file)
            print(f"  ✅ Restored {script_file.name}")
    
    print("\n✅ Demo restoration completed successfully!")
    print("\n📋 Next steps:")
    print("1. Run sample data scripts to populate the database:")
    print("   python scripts/add_sample_products.py")
    print("   python scripts/add_sample_webinar_registrants.py")
    print("   python scripts/download_sample_photos.py")
    print("2. Start the application: python main.py")
    print("3. Visit the demo pages:")
    print("   - http://localhost:8000/ai-demo")
    print("   - http://localhost:8000/dashboard-demo")
    print("   - http://localhost:8000/design-demo")
    print("   - http://localhost:8000/webinar-demo")


if __name__ == "__main__":
    restore_demo_files()
