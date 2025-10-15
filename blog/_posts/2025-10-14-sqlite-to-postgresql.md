---
layout: post
title: "Python Development with Asynchronous SQLite and PosgreSQL"
date: 2025-10-08
author: Craig Oda
author_bio: "Craig Oda is a partner at Oppkey and an active contributor to FastOpp"
image: /assets/images/2025_10/run.jpg
excerpt: "Solving security, database connector, and prepared statement problems with PostgreSQL"
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
not build a Django-like interface around FastAPI. The primary motivation occurred when I was using Django for asynchronous communication with LLM endpoints. Although Django works fine with
asynchronous communication, because its default communication style is synchronous,
it created a number of problems for me. For most average people like me, it's going
to be difficult to keep a method asynchronous and not have any
synchronous calls in it to other libraries that might be synchronous or
other synchronous communication channels like a database access.

At this point, I had already committed to FastAPI and making things asynchronous.
I thought I just needed to use an asynchronous driver with PostgresSQL
and everything would work.

I was wrong.

## psycopg2, psycopg3 or asyncpg

The default way to connect to Python for many people is psycopg2.
This is a very proven way.  It is the default usage in most Django applications.
Unfortunately, it is synchronous. The most common asynchronous PostgresSQL connector is asyncpg.
Initially, I used psycopg2 and rewrote the database connection to be synchronous.
As the latency with the LLM is much higher than the latency with the database,
this seemed like a reasonable solution at the time.

However, I ran into problems with organizing my code to be synchronous
connections to the database within asynchronous methods that were talking
to the LLM and storing the history in the database.

Next I moved to asyncpg.  


## SSL Security Not Needed in SQLite, But Needed in PostgresSQL Production

The asyncpg connector worked fine in development but not in production.

Although this seems obvious, I didn't really appreciate this because
I had been deploying to sites like Fly.io, Railway and DigitalOcean Droplets with SQLite.
For small prototype applications, SQLite works surprisingly well with FastAPI.
I was trying to deploy to the free version, hobby tier, of Leapcell to set up a
tutorial for students who didn't want to pay or didn't want to put their
credit card into a hosting service.

There's no way to write to the project file system on Leapcell.
They do offer a free tier that is pretty generous for PostgresSQL.
They require SSL communication between the PostgresSQL database and their engine,
which they call the service.

Unfortunately, the syntax is different for the SSL mode between psycopg2
and asyncpg.  I couldn't just add sslmode=require to the end of the connection URL.

Leapcell did not have an example for asyncpg. Likely due to my limited skills, I wasn't able to modify my application completely enough to put the SSL connections in all the required places.

In order to just use the URL connection point with sslmode=require, I decided
to use psycopg3.

## Prepared Statements Caused Application to Crash With SQLAlchemy

As I was trying to use an async ORM, I used SQLAlchemy. I
didn't have too much experience with it initially. I didn't realize that
even though I wasn't making prepared statements in my Python application,
the communication process between psycopg and PostgresSQL was storing
prepared statements.

Due to the way the connections were pooled on Leapcell, I had to disable the
prepared statements.  It took me a while to isolate the problem and
then implement the fix.

The problem never occurred when using SQLite because SQLite runs prepared statements
in the same process using the same memory space as the Python program.
This is different from PostgreSQL where the network and session state can change.

As I was worried about the performance impact, I did some research and it does appear that
SQLAlchemy already does statement caching on the Python side.

The real world impact of disabling the prepared statement in PostgreSQL
appears to be negligible.

