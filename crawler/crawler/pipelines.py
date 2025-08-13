# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import re
from itemadapter import ItemAdapter
import w3lib.html as w3html

from scrapy.exceptions import DropItem

class CrawlerPipeline:
    def process_item(self, item, spider):
        return item


# class PipelineExpander:

#     def process_item(self, item, spider):
#         if 'content' in item and isinstance(item['content'], (list, tuple)):
#             for subitem in item['content']:
#                 yield {**item, 'content': subitem }
#         else:
#             yield item

class FilterPipeline:

    def process_item(self, item, spider):
        if ('contents' not in item) or (not bool(item['contents'])):
            raise DropItem('Empty content')
        return item

class StringfyPipeline:

    def process_item(self, item, spider):
        ''' '''
        if 'contents' in item and isinstance(item['contents'], (list, tuple)):
            item['contents'] = '\n'.join(item['contents'])
        return item

class CleaningTextPipeline:

    def process_item(self, item, spider):
        for key in ['title', 'contents']:
            value = item.get(key, '')
            if isinstance(value, str):
                item[key] = self.preprocessing(value)
        return item

    def preprocessing(self, text):
        ''' '''
        text = re.sub(r"<script>.*?</script>", "", text, flags=re.DOTALL)
        text = re.sub(r"<style>.*?</style>", "", text, flags=re.DOTALL)
        text = w3html.remove_tags(text)
        text = re.sub(r'[\r\t\xa0 ]+', ' ', text)
        text = re.sub(r'\n+', '\n', text)
        text = text.strip()
        text = '' if text == '\n' else text
        return text
