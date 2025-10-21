---
layout: post
title: "Python Development with Asynchronous SQLite and PostgreSQL"
date: 2025-10-14
author: Craig Oda
author_bio: "Craig Oda is a partner at Oppkey and an active contributor to FastOpp"
image: /assets/images/2025_10/time.jpg
excerpt: "Solving SQL security, database connector, and prepared statement problems with Asynchronous PostgresSQL"
---

An updated version of this article is [available on DZone](https://dzone.com/articles/python-async-sqlite-postgresql-development).

After years of working from the comfort of Python and Django,
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

## Problems Moving to Asynchronous Database Connections psycopg2, psycopg3 or asyncpg

The default way to connect to Python for many people is psycopg2.
This is a very proven way.  It is the default usage in most Django applications.
Unfortunately, it is synchronous. The most common asynchronous PostgresSQL connector is asyncpg.
Initially, I used psycopg2 and rewrote the database connection to be synchronous and 
have everything around the connection be asynchronous. 
As the latency with the LLM is much higher than the latency with the database,
this seemed like a reasonable solution at the time.  I just had to await
for the database to send me back the response and then I was free to deal
with other asynchronous problems such as LLM query and Internet search
status updates.

This is great in theory and I'm sure that other more experienced Python
developers can easily solve this problem and keep the synchronous and asynchronous
code nicely separated with clean use of async and await.

However, I ran into problems with organizing my code to be synchronous
connections to the database within asynchronous methods that were talking
to the LLM and storing the history in the database.

As I was familiar with async/await from using Dart for many years,
I was pretty surprised I was having these problems.  The problem
I had might have been due to my lack of experience understanding
which pre-made Python modules were sending back synchronous versus asynchronous responses.

I think that other Python developers might be able to understand my pain.

To keep to an asynchronous database connection for both SQLite and PostgresSQL,
I moved to asyncpg.  


## SSL Security Not Needed in SQLite, But Needed in PostgresSQL Production

The asyncpg connector worked fine in development but not in production.

Although establishing an SSL network connection seems obvious, I didn't really appreciate this because
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

## Summary

Using SQLite in asynchronous mode has been quite easy.  Getting PostgresSQL to work has been more difficult.
There were three areas that I had trouble with for PostgresSQL:

1. Asynchronous connection. How write asynchronous Python code effectively to await the return data.
2. Security. How to deal with both SQLite that doesn't require a SSL and PostgresSQL in production that does require a SSL.
3. Prepared statements. I needed to learn to rely on the SQLAlchemy statement caching instead of the built-in prepared statements on the PostgresSQL server.


I like FastAPI and there are many huge advantages to using it that I got in the first hour of use.
I'm going to continue using it instead of Django.  However, I'm starting to really appreciate how much Django shielded me from much of the infrastructure setup for my applications.

FastAPI is unopinionated in things like the database, the connectors, authentication and models,
I find it difficult to gain expertise in any one area.  Thus, I am focusing on a smaller set of open source components that work with FastAPI so that I can gain a deeper understanding of how to use these components.

I feel that many other Python developers are on a similar journey to experiment more with asynchronous Python web applications.  I would appreciate feedback and ideas on which open source components or techniques to use to build effective asynchronous AI applications.

## Resources

* [FastOpp](https://github.com/Oppkey/fastopp) - Open source stack I am building around FastAPI
* [FastAPI](https://fastapi.tiangolo.com/) - A better Flask