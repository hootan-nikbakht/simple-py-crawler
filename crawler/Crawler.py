from Queue import Queue
from crawler import Producer

from crawler.parsers import FirstParser


class Crawler(object):
    """ Change the number for Threads for num_threads to speed up your crawler
    """
    num_threads = 24
    max_size = 100000
    daemon = False

    parsers = []
    producers = []

    context = {}
    context.update({"content_queue": Queue(maxsize=max_size)})
    context.update({"url_queue": Queue(maxsize=max_size)})
    context.update({"parsed": []})
    context.update({"prohibited": []})
    context.update({"visited": []})

    def __init__(self):
        allowed_domain = FirstParser.Thread.ALLOWED_DOMAIN
        self.producers = [Producer.Thread(self.context, domain=allowed_domain)
                          for i in xrange(self.num_threads)]
        self.parsers = [FirstParser.Thread(self.context) for i in xrange(self.num_threads)]

    def crawl(self, url):

        """ Kick start the crawler by starting the threads for producer & parser(consumer) thread
        """
        for thread in self.parsers + self.producers:
            thread.daemon = self.daemon
            thread.start()

        self.context.get('url_queue').put(url)
        self.context.get('content_queue').put(url)
