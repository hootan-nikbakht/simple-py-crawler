simple-py-crawler
=================

Python crawler for your basic use. Crawl a complete site &amp; extract your data.
This crawler leverages the producer/consumer design pattern, inspired from a blog which I can't seem to find.
The crawler is fairly tested and skips visited and prohibited urls.
    - visited url avoids parsing the same url twice or more
    - prohibited urls are parts of the site that are not your business territory that should be avoided for parsing


Something to take away home with you is GIL(Global Interpreter Lock) prevents multiple native threads from executing Python bytecodes at once.
BUT, potentially blocking or long-running operations, such as I/O(web requests), image processing, and NumPy number crunching, happen outside the GIL.

How to run ?
============

Install required packages:

on the cmd line run:

    ** sudo pip install -r requirements.txt

Note:if you have difficulty installing lxml in Max OSx, try:

    ** STATIC_DEPS=true pip install lxml

this should install all packages for you, then run:

    ** python main.py

