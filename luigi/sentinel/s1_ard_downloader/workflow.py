import luigi
import products_list_manager
import products_downloader
import products_metadata
import os
import logging
import time

from luigi.s3 import S3Target
from luigi.util import requires
import datetime

FILE_ROOT =  '/home/felix/temp/s1_ard'
LOG_ROOT = '/home/felix/temp/logs'

def getFilePath(filename):
    return os.path.join(os.path.join(FILE_ROOT, datetime.datetime.now().strftime('%Y-%m-%d')), filename)

def getLogger(folder, name):
    if not os.path.isdir(folder):
        os.makedirs(folder)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    fh = logging.FileHandler(os.path.join(folder, '%s-%s.log' % (name, time.strftime('%y%m%d-%H%M%S'))))
    fh.setFormatter(formatter)
    fh.setLevel(logging.DEBUG)

    logger.addHandler(fh)    

# Create new products list
class CreateProductsList(luigi.Task):

    def run(self):
        with self.output().open('w') as output:
            products_list_manager.createList(output)

    def output(self):
        return luigi.LocalTarget(getFilePath('available.json'))


# Download new products
class DownloadProducts(luigi.Task):

    def requires(self):
        return CreateProductsList()

    def run(self):
        with self.input().open() as available, self.output().open('w') as downloaded:
            products_downloader.downloadProducts(available, downloaded)

    def output(self):
        return luigi.LocalTarget(getFilePath('downloaded.json'))


# Get metadata for downloaded products
class GetMetadata(luigi.Task):

    def requires(self):
        return DownloadProducts()

    def run(self):
        with self.input().open() as downloaded, self.output().open('w') as success:
            products_metadata.getProductMetadata(downloaded, success)
    def output(self):
        return luigi.LocalTarget(getFilePath('_success.json'))

# Requires
# - downloaded.json
# Creates:
# - _success.json

# - read downloaded.json
# - Log into api
# - for each product in downloaded prodcuts list
# 	-Request gemini metadata from get_metadata
# 	-Write metadata to catalog
# 		-Prduction catalog could error if not valid gemini deal with this.
# - Create _success.json
