import threading
import urlparse
import mechanize

""" Link Grabber and populate content queue and url queue
    content queue, is the queue consumed by the parsers for extract content from the url
    url queue, is the
"""


class Thread(threading.Thread):
    HTTP = 'http://'
    STATUS_403 = '403'

    def __init__(self, context, domain):
        self.c_queue = context.get("content_queue")
        self.u_queue = context.get("url_queue")
        self.visited = context.get("visited")
        self.prohibited = context.get("prohibited")
        self.br = mechanize.Browser()
        self.allowed_domain = domain

        super(Thread, self).__init__()

    def run(self):
        while True:
            next_url = self.u_queue.get()
            try:
                if self.HTTP in next_url and \
                                next_url not in self.visited and \
                                next_url not in self.prohibited:
                    self.br.open(next_url)
                    self.visited.append(next_url)
                    self.br._factory.is_html = True

                    if self.br.links():
                        for link in self.br.links():
                            new_url = urlparse.urljoin(link.base_url, link.url)
                            if self.HTTP in new_url and new_url not in self.visited and new_url not in self.prohibited \
                                    and self.allowed_domain in new_url:
                                self.c_queue.put(new_url)
                                self.u_queue.put(new_url)
            except Exception, e:
                if self.STATUS_403 in e:
                    self.prohibited.append(next_url)

            while self.c_queue.full():
                pass

            self.u_queue.task_done()