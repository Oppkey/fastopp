#!/usr/bin/env python3
"""
Script to add sample webinar registrants with photos for testing the photo upload functionality
"""

import asyncio
from datetime import datetime, timezone
import os
from pathlib import Path
import uuid

from core.services.storage import get_storage
from db import AsyncSessionLocal


async def add_sample_registrants():
    """Add sample webinar registrants to the database with photos"""
    from models import WebinarRegistrants  # Import inside function to avoid module-level import error

    sample_registrants = [
        {
            "name": "John Smith",
            "email": "john.smith@example.com",
            "company": "Tech Corp",
            "webinar_title": "Advanced FastAPI Development",
            "webinar_date": datetime(2024, 2, 15, 14, 0, tzinfo=timezone.utc),
            "status": "registered",
            "photo_filename": "john_smith.jpg",
            "notes": ("Interested in implementing authentication systems. "
                      "Has experience with Django and wants to migrate to FastAPI.")
        },
        {
            "name": "Sarah Johnson",
            "email": "sarah.johnson@startup.io",
            "company": "Startup Inc",
            "webinar_title": "Building Scalable APIs",
            "webinar_date": datetime(2024, 2, 20, 10, 0, tzinfo=timezone.utc),
            "status": "attended",
            "photo_filename": "sarah_johnson.jpg",
            "notes": ("Startup founder looking to scale their API from 100 to 10,000 users. "
                      "Currently using Express.js and considering FastAPI for better performance.")
        },
        {
            "name": "Michael Chen",
            "email": "michael.chen@enterprise.com",
            "company": "Enterprise Solutions",
            "webinar_title": "Database Design Best Practices",
            "webinar_date": datetime(2024, 2, 25, 16, 0, tzinfo=timezone.utc),
            "status": "registered",
            "photo_filename": "michael_chen.jpg",
            "notes": ("Senior architect evaluating database solutions for a new microservices project. "
                      "Interested in PostgreSQL and Redis integration patterns.")
        },
        {
            "name": "Emily Davis",
            "email": "emily.davis@freelance.dev",
            "company": "Freelance Developer",
            "webinar_title": "Modern Web Development",
            "webinar_date": datetime(2024, 3, 1, 13, 0, tzinfo=timezone.utc),
            "status": "registered",
            "photo_filename": "emily_davis.jpg",
            "notes": ("Full-stack developer specializing in React and Node.js. "
                      "Looking to expand skillset to include Python and FastAPI for backend development.")
        },
        {
            "name": "David Wilson",
            "email": "david.wilson@consulting.co",
            "company": "Tech Consulting",
            "webinar_title": "API Security Fundamentals",
            "webinar_date": datetime(2024, 3, 5, 15, 0, tzinfo=timezone.utc),
            "status": "registered",
            "photo_filename": "david_wilson.jpg",
            "notes": ("Security consultant working with financial services clients. "
                      "Needs to implement OAuth2 and JWT token validation for compliance requirements.")
        }
    ]

    # Get storage instance
    storage = get_storage()

    async with AsyncSessionLocal() as session:
        for registrant_data in sample_registrants:
            # Check if registrant already exists
            from sqlmodel import select
            existing = await session.execute(
                select(WebinarRegistrants).where(WebinarRegistrants.email == registrant_data['email'])
            )
            if existing.scalar_one_or_none():
                print(f"Registrant {registrant_data['email']} already exists, skipping...")
                continue

            # Copy sample photo if it exists
            photo_url = None
            photo_filename = registrant_data.pop('photo_filename')
            sample_photo_path = f"sample_photos/{photo_filename}"

            print(f"Looking for sample photo: {sample_photo_path}")
            # Try with prefix first, then without prefix (for backward compatibility)
            actual_photo_path = None
            if storage.file_exists(sample_photo_path):
                actual_photo_path = sample_photo_path
                print(f"✓ Found sample photo with prefix: {sample_photo_path}")
            elif storage.file_exists(photo_filename):
                actual_photo_path = photo_filename
                print(f"✓ Found sample photo without prefix: {photo_filename}")
            
            if actual_photo_path:
                # Generate unique filename for the photo
                unique_filename = f"{uuid.uuid4()}_{photo_filename}"
                storage_path = f"photos/{unique_filename}"
                print(f"Will copy to: {storage_path}")

                # Read the sample photo from storage and save to photos directory
                photo_content = storage.get_file(actual_photo_path)
                print(f"Read {len(photo_content)} bytes from sample photo")
                
                photo_url = storage.save_file(
                    content=photo_content,
                    path=storage_path,
                    content_type="image/jpeg"
                )
                print(f"✓ Copied photo for {registrant_data['name']} to {photo_url}")
            else:
                print(f"⚠ Sample photo not found: {sample_photo_path}")
                # Let's also check what files exist in sample_photos directory
                try:
                    if hasattr(storage, 'list_files'):
                        files = storage.list_files("sample_photos/")
                        print(f"Available files in sample_photos/: {files}")
                except Exception as e:
                    print(f"Error listing files: {e}")

            # Create new registrant
            registrant = WebinarRegistrants(
                id=uuid.uuid4(),
                name=registrant_data['name'],
                email=registrant_data['email'],
                company=registrant_data['company'],
                webinar_title=registrant_data['webinar_title'],
                webinar_date=registrant_data['webinar_date'],
                status=registrant_data['status'],
                notes=registrant_data['notes'],
                photo_url=photo_url
            )

            session.add(registrant)
            print(f"Added registrant: {registrant_data['name']} ({registrant_data['email']})")

        await session.commit()
        print(f"\nSuccessfully added {len(sample_registrants)} sample webinar registrants with photos!")


if __name__ == "__main__":
    asyncio.run(add_sample_registrants())
