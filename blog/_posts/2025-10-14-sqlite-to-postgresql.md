---
layout: post
title: "Python Development with Asynchronous SQLite and PosgreSQL"
date: 2025-10-08
author: Craig Oda
author_bio: "Craig Oda is a partner at Oppkey and an active contributor to FastOpp"
image: /assets/images/2025_10/run.jpg
excerpt: "Solving security, driver, and prepared statement problems with PostgreSQL"
---

After years of working with the comfort of Python and Django,
I moved to the wild asynchronous world of FastAPI to improve
latency in web-based AI applications. I started with FastAPI
and built an open source stack called [FastOpp](https://github.com/Oppkey/fastopp) which adds command line and web tools similar to Django.

Initially, things with smoothly using SQLite and
[aiosqlite](https://github.com/omnilib/aiosqlite) to add
AsyncIO to SQLite. I used [SQLAlchemy](https://www.sqlalchemy.org/) as my Object Relational
Mapper (ORM) and Alembic as the database migration tool. Everything
seemed to work easily, so I added a Python script to make things
similar to Django's `migrate.py`.

As things were going smoothly, I added [Pydantic](https://docs.pydantic.dev/latest/) for data validation and
connected Pydantic to the SQLAlchemy models with [SQLModel](https://sqlmodel.tiangolo.com/).
Although I was pulling in open source packages that I wasn't that familiar with, the packages
were popular and I didn't have problems during initial use.

Django comes with an opinated stack of stable, time-tested tools, which I was
started to miss. However, in order to give
FastAPI a proper assessment, I continued forward by integrating
[SQLAdmin](https://github.com/aminalaee/sqladmin)
for a pre-configured web admin panel for SQLAlchemy.

I also implemented [FastAPIUsers](https://github.com/fastapi-users/fastapi-users).
At this point, I started to miss Django even more as I needed to implement my own
JWT authentication, using FastAPIUsers as the hash mechanism.
The FastAPI project has a [full-stack-fastapi-template](https://github.com/fastapi/full-stack-fastapi-template)
that might have been a better starting point.

I chose not to use it since my primary goal was focused on using Jinja2
templates for a streaming application from an LLM. This would provide a more Django-like experience
for FastAPI and provide the opportunity in the future to use the built-in API and auto-documentation
of FastAPI instead of implementing something like Django REST framework.

The obvious question is whether it's better to just use Django from the beginning and
not build a Django-like interface around FastAPI. The primary motivation occurred when I was using Django for asynchronous communication with LLM endpoints. although Django works fine with
asynchronous communication, because its default communication style is synchronous,
it created a number of problems for me. For most average people like me, it's going
to be difficult to keep a method asynchronous and not have any
synchronous calls in it to other libraries that might be synchronous or
other synchronous communication channels like a database access.

