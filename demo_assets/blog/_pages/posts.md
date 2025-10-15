---
layout: default
title: Blog Posts
permalink: /posts/
---

<div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
    <div class="text-center mb-16">
        <h1 class="text-4xl font-bold text-gray-900 mb-4">Blog Posts</h1>
        <p class="text-xl text-gray-600 max-w-3xl mx-auto">
            Stay updated with the latest FastOpp developments, tutorials, and insights about building AI applications.
        </p>
    </div>
    
    {% if site.posts.size > 0 %}
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
        {% for post in site.posts %}
        <article class="bg-white rounded-xl shadow-lg overflow-hidden hover:shadow-xl transition-shadow">
            {% if post.image %}
            <img src="{{ post.image | relative_url }}" alt="{{ post.title }}" class="w-full h-48 object-cover">
            {% endif %}
            <div class="p-6">
                <div class="flex items-center text-sm text-gray-500 mb-2">
                    <time datetime="{{ post.date | date_to_xmlschema }}">
                        {{ post.date | date: "%B %d, %Y" }}
                    </time>
                    <span class="mx-2">•</span>
                    <span>{{ post.author | default: site.author }}</span>
                </div>
                <h2 class="text-xl font-semibold mb-3 text-gray-900">
                    <a href="{{ post.url | relative_url }}" class="hover:text-ai-blue transition-colors">
                        {{ post.title }}
                    </a>
                </h2>
                <p class="text-gray-600 mb-4">
                    {{ post.excerpt | strip_html | truncate: 150 }}
                </p>
                <a href="{{ post.url | relative_url }}" 
                   class="inline-flex items-center text-ai-blue hover:text-blue-700 font-medium">
                    Read more
                    <svg class="w-4 h-4 ml-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"></path>
                    </svg>
                </a>
            </div>
        </article>
        {% endfor %}
    </div>
    {% else %}
    <div class="text-center py-12">
        <div class="w-24 h-24 bg-gray-100 rounded-full flex items-center justify-center mx-auto mb-4">
            <svg class="w-12 h-12 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>
            </svg>
        </div>
        <h3 class="text-xl font-semibold text-gray-900 mb-2">No posts yet</h3>
        <p class="text-gray-600">Check back soon for the latest FastOpp updates and tutorials.</p>
    </div>
    {% endif %}
</div>
