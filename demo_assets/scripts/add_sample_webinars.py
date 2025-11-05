# =========================
# add_sample_webinars.py - Add sample webinar registrants
# =========================
import asyncio
from datetime import datetime, timedelta

from sqlmodel import select

from db import AsyncSessionLocal


async def add_sample_webinars():
    """Add sample webinar registrants to the database"""
    from models import WebinarRegistrants  # Import inside function to avoid module-level import error
    
    async with AsyncSessionLocal() as session:
        
        # Sample webinar registrants with different groups and sales reps
        webinars = [
            {
                "email": "john.doe@techcorp.com",
                "name": "John Doe",
                "company": "TechCorp Inc.",
                "webinar_title": "FastAPI Best Practices",
                "webinar_date": datetime.utcnow() + timedelta(days=7),
                "status": "registered",
                "assigned_sales_rep": "sales@example.com",
                "group": "marketing",
                "is_public": True,
                "notes": "Interested in enterprise features"
            },
            {
                "email": "jane.smith@startup.io",
                "name": "Jane Smith",
                "company": "Startup.io",
                "webinar_title": "Database Migration Strategies",
                "webinar_date": datetime.utcnow() + timedelta(days=14),
                "status": "registered",
                "assigned_sales_rep": "sales@example.com",
                "group": "sales",
                "is_public": True,
                "notes": "Looking for PostgreSQL migration help"
            },
            {
                "email": "bob.wilson@enterprise.com",
                "name": "Bob Wilson",
                "company": "Enterprise Solutions",
                "webinar_title": "Production Deployment",
                "webinar_date": datetime.utcnow() + timedelta(days=21),
                "status": "registered",
                "assigned_sales_rep": "marketing@example.com",
                "group": "marketing",
                "is_public": False,
                "notes": "Enterprise customer - high priority"
            },
            {
                "email": "alice.brown@consulting.com",
                "name": "Alice Brown",
                "company": "Brown Consulting",
                "webinar_title": "API Security Best Practices",
                "webinar_date": datetime.utcnow() + timedelta(days=5),
                "status": "attended",
                "assigned_sales_rep": "sales@example.com",
                "group": "sales",
                "is_public": True,
                "notes": "Attended previous webinar, very engaged"
            },
            {
                "email": "charlie.davis@agency.com",
                "name": "Charlie Davis",
                "company": "Digital Agency",
                "webinar_title": "Microservices Architecture",
                "webinar_date": datetime.utcnow() + timedelta(days=10),
                "status": "registered",
                "assigned_sales_rep": "marketing@example.com",
                "group": "marketing",
                "is_public": True,
                "notes": "Agency looking to standardize on FastAPI"
            },
            {
                "email": "diana.evans@startup.io",
                "name": "Diana Evans",
                "company": "Startup.io",
                "webinar_title": "Testing Strategies",
                "webinar_date": datetime.utcnow() + timedelta(days=3),
                "status": "cancelled",
                "assigned_sales_rep": "sales@example.com",
                "group": "sales",
                "is_public": True,
                "notes": "Cancelled due to scheduling conflict"
            },
            {
                "email": "edward.foster@corp.com",
                "name": "Edward Foster",
                "company": "Foster Corp",
                "webinar_title": "Performance Optimization",
                "webinar_date": datetime.utcnow() + timedelta(days=28),
                "status": "registered",
                "assigned_sales_rep": "marketing@example.com",
                "group": "marketing",
                "is_public": False,
                "notes": "Large enterprise customer"
            },
            {
                "email": "fiona.garcia@tech.com",
                "name": "Fiona Garcia",
                "company": "Tech Solutions",
                "webinar_title": "Authentication & Authorization",
                "webinar_date": datetime.utcnow() + timedelta(days=12),
                "status": "registered",
                "assigned_sales_rep": "sales@example.com",
                "group": "sales",
                "is_public": True,
                "notes": "Security-focused company"
            }
        ]
        
        for webinar_data in webinars:
            # Skip if registrant already exists (idempotent by email)
            result = await session.execute(
                select(WebinarRegistrants).where(WebinarRegistrants.email == webinar_data["email"])  # type: ignore[index]
            )
            if result.scalar_one_or_none():
                print(f"ℹ️  Webinar registrant already exists, skipping: {webinar_data['email']}")
                continue
            registrant = WebinarRegistrants(**webinar_data)
            session.add(registrant)
        
        await session.commit()
        print("✅ Added sample webinar registrants to database (skipping existing)")
        print("Sample webinars:")
        print("- FastAPI Best Practices (TechCorp)")
        print("- Database Migration Strategies (Startup.io)")
        print("- Production Deployment (Enterprise Solutions)")
        print("- API Security Best Practices (Brown Consulting)")
        print("- Microservices Architecture (Digital Agency)")
        print("- Testing Strategies (Startup.io) - Cancelled")
        print("- Performance Optimization (Foster Corp)")
        print("- Authentication & Authorization (Tech Solutions)")
        print("\nPermission testing:")
        print("- Marketing users see all registrants")
        print("- Sales users see only their assigned registrants")
        print("- Support users see only public registrants")
        print("- Superusers see all registrants")


if __name__ == "__main__":
    asyncio.run(add_sample_webinars()) 