import threading
import urllib2
from decimal import Decimal

import mechanize
from bs4 import BeautifulSoup
from pprint import pprint


class Thread(threading.Thread):
    ALLOWED_DOMAIN = 'www.prestigetime.com/'

    def __init__(self, context):
        self.c_queue = context.get('content_queue')
        self.u_queue = context.get('url_queue')
        self.br = mechanize.Browser()
        self.parsed = context.get('parsed')
        self.prohibited = context.get('prohibited')
        super(Thread, self).__init__()

    def run(self):
        while True:
            try:
                """ get urls from the content queue to pull in the content and parse """
                url = self.c_queue.get()
                if url not in self.parsed and url not in self.prohibited:
                    self.parsed.append(url)
                    #print url
                    response = urllib2.urlopen(url)
                    if response.code == 200:
                        content = response.read()

                        data_context = Thread.parse_html(content, url)
                        if data_context:
                            data_context.update({"url": url})
                            pprint(data_context)
                            print

            except Exception, e:
                pass
                #TODO: Swallowing exceptions are for losers
            self.c_queue.task_done()


    @staticmethod
    def parse_html(content, url):
        """Example screen that I am parsing here:
            http://www.prestigetime.com/item/Panerai/Luminor-Marina-1950-3-Days-Manual-Wind/pam00422.html
        """

        try:
            """bs4 to get all td elements with given classes."""
            soup = BeautifulSoup(content)
            tds = soup.find_all("td", {"class": "desctdB"}) \
                + soup.find_all("td", {"class": "desctd"}) \
                + soup.find_all("td", {"class": "desctd1"})

            data_context = {}

            """Get basic info you need from your HTML page"""
            for td in tds:
                try:
                    if td.string == 'Brand:':
                        data_context.update({'brand': td.findNext('td').string})
                    elif td.string == 'Series:':
                        data_context.update(({'model_name': td.findNext('td').string}))
                    elif td.string == 'Model #:':
                        data_context.update({'model_number': td.findNext('td').string.split()[0]})
                    elif td.string == 'Retail:':
                        msrp_str = td.findNext('td').string
                        for ch in ['$', ',']:
                            msrp_str = msrp_str.replace(ch, '')
                        data_context.update({'msrp': Decimal(msrp_str)})
                    else:
                        pass

                except Exception, e:
                    pass
                    #TODO: Swallowing exceptions are for losers
            return data_context
        except Exception, e:
            pass
            #TODO: Swallowing exceptions are for losers

