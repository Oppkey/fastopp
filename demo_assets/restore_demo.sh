#!/bin/bash

# Demo Restoration Script
# This script restores all demo files from the demo_assets backup to their original locations.
# Run this script from the project root directory.

set -e  # Exit on any error

echo "🔄 Restoring demo files from backup..."

# Check if we're in the right directory
if [ ! -d "demo_assets" ]; then
    echo "❌ Error: demo_assets directory not found!"
    echo "Please run this script from the project root directory."
    exit 1
fi

# Restore templates
echo "📄 Restoring templates..."
cp demo_assets/templates/*.html templates/ 2>/dev/null || true
if [ -d "demo_assets/templates/partials" ]; then
    rm -rf templates/partials
    cp -r demo_assets/templates/partials templates/
    echo "  ✅ Restored partials/"
fi

# Restore static files
echo "🎨 Restoring static files..."
if [ -d "demo_assets/static/images" ]; then
    rm -rf static/images
    cp -r demo_assets/static/images static/
    echo "  ✅ Restored images/"
fi

# Copy other static files
for file in demo_assets/static/*; do
    if [ -f "$file" ] && [[ "$(basename "$file")" != "uploads" ]]; then
        cp "$file" static/
        echo "  ✅ Restored $(basename "$file")"
    fi
done

# Copy CSS and JS directories
for subdir in css js; do
    if [ -d "demo_assets/static/$subdir" ]; then
        rm -rf "static/$subdir"
        cp -r "demo_assets/static/$subdir" static/
        echo "  ✅ Restored $subdir/"
    fi
done

# Restore routes
echo "🛣️  Restoring routes..."
cp demo_assets/routes/*.py routes/ 2>/dev/null || true

# Restore services (application-specific services only, core services remain in core/)
echo "🔧 Restoring services..."
cp demo_assets/services/*.py services/ 2>/dev/null || true

# Restore models
echo "📊 Restoring models..."
cp demo_assets/models.py . 2>/dev/null || true
echo "  ✅ Restored models.py"

# Copy sample data scripts
echo "📝 Restoring sample data scripts..."
cp demo_assets/scripts/*.py scripts/ 2>/dev/null || true

echo ""
echo "✅ Demo restoration completed successfully!"
echo ""
echo "📋 Next steps:"
echo "1. Run sample data scripts to populate the database:"
echo "   python scripts/add_sample_products.py"
echo "   python scripts/add_sample_webinar_registrants.py"
echo "   python scripts/download_sample_photos.py"
echo "2. Start the application: python main.py"
echo "3. Visit the demo pages:"
echo "   - http://localhost:8000/ai-demo"
echo "   - http://localhost:8000/dashboard-demo"
echo "   - http://localhost:8000/design-demo"
echo "   - http://localhost:8000/webinar-demo"
