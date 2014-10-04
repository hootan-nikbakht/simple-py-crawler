simple-py-crawler
=================

Python crawler for your basic use. Crawl a complete site &amp; extract your data.
This crawler leverages the producer/consumer design pattern, inspired from a blog which I can't seem to find.
The crawler is fairly tested and skips visited and prohibited urls.
    - visited url avoids parsing the same url twice or more
    - prohibited urls are parts of the site that are not your business territory that should be avoided for parsing


How to run ?
============

* Install required packages:

on the cmd line run:

    * sudo pip install -r requirements.txt

this should install all packages for you, then run:

    * python main.py


if you have difficulty installing lxml in Max OSx, try:
    * STATIC_DEPS=true pip install lxml