import logging
import re
import scrapy

from datetime import datetime
from scrapy import Request
from scrapy.linkextractors import LinkExtractor
from urllib.parse import urlparse

import logging

logging.basicConfig(
    filename="file.log", format="%(levelname)s: %(message)s", level=logging.INFO
)

class SpiderICMC(scrapy.Spider):

    name = 'icmc'
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

    extractor = LinkExtractor()

    ignore_extensions = (
        '.pdf', '.jpg', '.jpeg', '.png', '.gif', '.doc', '.docx', '.ppt', '.pptx',
        '.xls', '.xlsx', '.zip', '.rar', '.tar', '.gz', '.exe', '.avi', '.flv',
    )

    def parse(self, response):
        self.logger.info('Processing: %s | Status: %d', response.url, response.status)

        if response.status != 200:
            self.logger.warning('Error %s: %s', response.status, response.url)
            return None

        links = self.extractor.link_extractor.extract_links(response)

        scripts = response.xpath("//script")
        scripts.drop()

        if 'perguntas-frequentes' in response.url:
            yield from self.parse_faq(response, links)
        else :
            yield from self.parse_standard(response, links)

        for link in links:
            url = urlparse(link.url)
            if url.fragment.startswith('#'): continue
            if not any(url.path.startswith(s) for s in self.subdomains): continue
            if url.path.endswith(self.ignore_extensions) : continue
            yield response.follow(link.url, self.parse)

    def parse_standard(self, response, links):

        main = response.xpath(".//div[contains(@class, 'conteudo')]//div[contains(@class, 'main')]")
        articleBody = main.xpath(".//div[@itemprop='articleBody']//div[not(.//div)]")

        if not articleBody:
            contents = main.xpath(".//text()").getall()
        else:
            contents = articleBody.xpath(".//text()").getall()

        content = ' '.join(contents)
        content = re.sub(r'\s+', ' ', content)
        content = content.strip()

        yield {
            'url' : response.url,
            'date' : datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'status' : response.status,
            'contents' : content,
            'type' : 'page',
            'file_urls' : self.parse_file_links(links)
        }

    def parse_faq(self, response, links):

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
                    'type' : 'faq',
                    'file_urls' : self.parse_file_links(links)
                }

    def parse_file_links(self, links):
        return [ l.url for l in links if l.url.endswith('.pdf') ]



class SpiderNormasICMC(scrapy.Spider):

    name = 'normas'
    start_urls = ['https://www.icmc.usp.br']
    # start_urls = ['https://www.icmc.usp.br/pos-graduacao/ppgccmc/informacoes-gerais']
    allowed_domains = [
            'icmc.usp.br',
            'www.leginf.usp.br',
            'leginf.usp.br'
        ]

    subdomains = {
        '/graduacao',
        '/pos-graduacao',
        '/pesquisa',
        # '/cultura-e-extensao',
        # '/inclusao-e-pertencimento',
        # '/institucional'
    }

    allowed = {
        'www.leginf.usp.br',
        'www.icmc.usp.br'
    }

    extractor = LinkExtractor()

    ignore_extensions = (
        '.pdf', '.jpg', '.jpeg', '.png', '.gif', '.doc', '.docx', '.ppt', '.pptx',
        '.xls', '.xlsx', '.zip', '.rar', '.tar', '.gz', '.exe', '.avi', '.flv',
    )

    def parse(self, response):
        self.logger.info('Processing: %s | Status: %d', response.url, response.status)

        if response.status != 200:
            self.logger.warning('Error %s: %s', response.status, response.url)
            return None

        links = self.extractor.link_extractor.extract_links(response)
        url = urlparse(response.url)
        scripts = response.xpath("//script")
        scripts.drop()

        if url.netloc in {'www.leginf.usp.br', 'leginf.usp.br'}:
            yield from self.parse_legal_norm(response, links)
            links = []
        else:
            yield {
                'url' : response.url,
                'date' : datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'status' : response.status,
                'netloc' : url.netloc,
                'contents' : False,
                'type' : 'parse',
                'file_urls' : [],
                'links' : self.check_link(links)
            }

        for url in self.check_link(links):
            yield Request(url=url, callback=self.parse)

    def check_link(self, links):
        urls = list()
        for link in links:
            url = urlparse(link.url)
            if (url.netloc not in self.allowed): continue
            if (url.netloc == 'www.icmc.usp.br') and (not any(url.path.startswith(s) for s in self.subdomains)): continue
            if (url.netloc == 'www.icmc.usp.br') and url.fragment.startswith('#'): continue
            if url.path.endswith(self.ignore_extensions): continue
            # if (url.netloc == 'www.icmc.usp.br'): continue
            urls.append(link.url)
        return urls


    def parse_legal_norm(self, response, links):
        div = response.xpath("//div[@id='content']")
        article = div.xpath(".//article")
        header = article.xpath(".//header//text()").getall()
        header = ' '.join(header)
        header = re.sub(r'\s+', ' ', header)
        header = header.strip()
        paragraphs = article.xpath("//div[contains(@class, 'content')]/*")
        blocks = list()
        block = list()
        for p in paragraphs:
            if p.root.tag != 'p' or bool(p.attrib):
                block.append(" ".join(p.getall()))
            else:
                block.append(" ".join(p.getall()))
                blocks.append('\n'.join(block))
                block = list()

        content = [header]
        content.extend(blocks)

        yield {
            'url' : response.url,
            'date' : datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'status' : response.status,
            'contents' : ' '.join(content),
            'type' : 'legal_norm',
            'file_urls' : self.parse_file_links(links),
            'links' : [l.url for l in links]
        }

    def parse_standard(self, response, links):

        main = response.xpath(".//div[contains(@class, 'conteudo')]//div[contains(@class, 'main')]")
        articleBody = main.xpath(".//div[@itemprop='articleBody']//div[not(.//div)]")

        if not articleBody:
            contents = main.xpath(".//text()").getall()
        else:
            contents = articleBody.xpath(".//text()").getall()

        content = ' '.join(contents)
        content = re.sub(r'\s+', ' ', content)
        content = content.strip()

        yield {
            'url' : response.url,
            'date' : datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'status' : response.status,
            'contents' : content,
            'type' : 'page',
            'file_urls' : self.parse_file_links(links)
        }

    def parse_faq(self, response, links):

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
                    'type' : 'faq',
                    'file_urls' : self.parse_file_links(links)
                }

    def parse_file_links(self, links):
        return [ l.url for l in links if l.url.endswith('.pdf') ]