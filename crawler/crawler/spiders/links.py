import logging
import scrapy
import re
import yaml
import trrex as tx

from datetime import datetime
from pathlib import Path

class SpiderFAQ(scrapy.Spider):

    name = 'arquivo'
    allowed_domains = ['icmc.usp.br']
    file = Path('urls.yaml') # Verificar como definir a localização desse arquivo da melhor forma
    file_storage = Path('data', 'files')

    if file.exists():
        logging.info('Loading start urls from file: %s', file)
        configs = yaml.safe_load( file.read_text() )
        start_urls = configs['urls']
    else:
        start_urls = list()
        files = list(Path('..', '..').iterdir())
        logging.warning('File not found: %s', file)
        logging.warning('Available files: %s', files)

    async def start(self):
        '''
        '''
        for url in self.start_urls:
           yield scrapy.Request(url, self.parse, cb_kwargs={'name': 'Giliard'})

    def parse(self, response, **kwargs):

        name = kwargs.get('name', 'Not provided')
        self.logger.info('Hello %s, parsing: %s', name, response.url)

        if 'perguntas-frequentes' in response.url \
            or 'faq' in response.url:
            yield from self.parse_faq(response)
        elif response.url.endswith('.pdf'):
            self.logger.info('PDF file found: %s', response.url)
            yield from self.download_pdf_files(response)
        else:
            yield from self.parse_standard(response)

    def parse_standard(self, response):
        '''
        '''
        self.logger.info('Parsing standard page: %s', response.url)
        div = response.css('div.item-page')
        title = div.css('h1::text, h2::text').get()
        elements = ".//h3 | .//h4 | .//h5 | .//h6 | .//p | .//ul | .//table | .//blockquote | .//div[not(*)]"
        elements = div.xpath(elements).xpath("string(.)").getall()
        for content in elements:
            yield {
                    'title': title,
                    'contents': content,
                    'url': response.url,
                    'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    'type' : 'info'
                }

    def parse_faq(self, response):
        '''
        '''
        self.logger.info('Parsing standard page: %s', response.url)
        div = response.css('div.item-page')
        questions = div.xpath('//div[@class="panel"][not(descendant::div[@class="panel"])]')
        questions = [q.css('p::text, a::text').getall() for q in questions]
        title = div.css('h1::text, h2::text, h3::text').get()

        for question in questions:
            yield {
                    'title': title,
                    'contents': question,
                    'url': response.url,
                    'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    'type' : 'faq'
                }

class SpiderLinks(scrapy.Spider):

    name = 'links'
    start_urls = ['https://www.icmc.usp.br/']
    allowed_domains = ['icmc.usp.br']

    subdomains = {
        '/graduacao',
        '/pos-graduacao',
        '/pesquisa',
        # '/cultura-e-extensao',
        # '/inclusao-e-pertencimento',
        # '/institucional'
    }

    ignore_extensions =[
        '.pdf', '.jpg', '.jpeg', '.png', '.gif', '.doc', '.docx', '.ppt', '.pptx',
        '.xls', '.xlsx', '.zip', '.rar', '.tar', '.gz', '.exe', '.avi', '.flv',
    ]

    ignore_pattern = re.compile(tx.make(ignore_extensions))

    def parse(self, response):
        self.logger.info('Parsing links: %s', response.url)
        links = response.xpath('//a[not(starts-with(@href, "#"))]/@href')
        links = links.getall()

        item = {
            'url' : response.url,
            'date' : datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'status' : response.status,
            'contents' : 'Extracted links',
            'links' : [response.urljoin(link) for link in links],
            'type' : 'link',
            'file_urls' : [ link for link in links if link.endswith('.pdf') ]
        }

        yield item

        for url in links:
            if url is None: continue
            tmp = url.strip('/').split('/')

            if isinstance(tmp, list) and len(tmp) == 0: continue
            if tmp[0] not in self.subdomains: continue

            # self.logger.info('Processing link: %s', url)
            yield response.follow(url, self.parse)