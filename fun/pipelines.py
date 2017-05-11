# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import requests
import os


class ImageDownloadPipeline(object):
    def process_item(self, item, spider):
        if 'image_urls' in item:
            images = []
            from spy.fun_crawler.fun import settings
            dir_path = '%s/%s' % (settings.IMAGES_STORE, spider.name)

            request_data = {'allow_redirects': False,
                            'auth': None,
                            'cert': None,
                            'data': {},
                            'files': {},
                            'headers': {
                                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.98 Safari/537.36'},
                            'method': 'get',
                            'params': {},
                            'proxies': {},
                            'stream': True,
                            'timeout': 30,
                            'url': '',
                            'verify': True}

            if not os.path.exists(dir_path):
                os.makedirs(dir_path)
            for image_url in item['image_urls']:
                request_data['url'] = image_url
                us = image_url.split('/')[3:-1]
                image_file_name = '_'.join(us)
                if not image_file_name.endswith('.jpg'):
                    image_file_name = image_file_name + '.jpg'
                file_path = '%s/%s' % (dir_path, image_file_name)
                images.append(file_path)
                # print(file_path, image_url)
                if os.path.exists(file_path):
                    continue

                with open(file_path, 'wb') as handle:
                    response = requests.request(**request_data)
                    for block in response.iter_content(1024):
                        if not block:
                            break

                        handle.write(block)

            item['images'] = images
        return item
