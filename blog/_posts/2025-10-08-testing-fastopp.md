---
layout: post
title: "Our Process for Testing and Contributing to FastOpp"
date: 2025-10-08
author: Ethan Luke Kim
author_bio: "Ethan Luke Kim is a student at UC Berkeley and a contributor to the FastOpp project."
image: https://lh3.googleusercontent.com/gg-dl/AJfQ9KRhVzJiKWNAJOaSeVa5NZQ6zEz3NjCnj9UNhTUB-oPwUhod6Iq0-VN3qLoNyrm4ZRxxLM_ASBfqI4JriGx6L2wVRBhgIyyqL1RYpTdzpaOnseMICQcLI9PaCE5PZUV0n0voR41gzmiMLbtn-xeM1RCIhulEnhIPvkNF0bRhw8kulA1zjQ=s1024-rj
excerpt: "A quick guide and personal notes on testing the FastOpp framework, including the essential git commands for contributing."
---

First Impressions: Putting a New LLM to the Test
I recently had the opportunity to try FastOpp's AI Chat assistant and decided to test it using different procedures. My goal was to test its performance across a variety of tasks, from its raw speed and accuracy to its conversational memory. Here’s a look at how it performed.

Speed and Versatility: The Bright Spots

Right away, I was impressed by the LLM's results. It handled a diverse set of prompts, tackling controversial topics, generating specific coding examples, and even constructing travel plans around a given timeframe and location of interest. The speed was great, too. Most responses were generated in a quick 3 to 5 seconds.

The model also proved its accuracy in specific tasks. I tested its summarization ability with a short, four-sentence paragraph about the sun and asked it to condense it into a single sentence. It passed perfectly, creating one concise sentence that captured all the necessary information without losing accuracy.

A Few Hiccups:

While I enjoyed tinkering with the LLM, a prototype wouldn't be a prototype without things it can improve on.

First, I noticed that response times weren't always consistent. Some simple prompts took longer than expected (6-10 seconds), while, interestingly, some complex requests (e.g., debugging a recursive function) took around the same time a simple prompt would.

Second, during longer sessions, particularly after about 30 prompts, the model would sometimes run into errors and temporarily refuse to accept a new prompt. However, to my surprise, after a short 5-to-10-second wait, the LLM would again accept prompts as if nothing had happened.

I also dug into its conversational memory (or at least I attempted to). My procedure was simple. First, I fed the LLM a simple fact: I told the LLM that my cat's name is Kathy. Afterward, I would ask the LLM to write some simple code for minor tasks such as writing a sentence or printing a range of numbers.

My tests showed it could reliably remember the context of a conversation for up to 8 messages, but it struggled beyond that. Later, I tried again with more complex prompts. It could not remember the simple fact after 10, 20, or 30 messages, regardless of prompt complexity. This was even though I manually changed the message history limit through Visual Studio Code on my local machine.

Final Thoughts:

Overall, my experience with the AI Chat Assistant was very promising. It demonstrates a powerful and fast core capability while able to handle tasks with impressive detail. The occasional errors are expected of a prototype. Personally, they were no hindrance in assisting me with my daily activities. The foundation is clearly solid, and I'm excited to see how this LLM can help users accomplish more in a quick and cost-efficient manner.