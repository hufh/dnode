import luigi
import docker
import datetime
import os
import json

from ftp_client import FTPClient
from config_manager import ConfigManager
from catalog_manager import CatalogManager
from luigi.util import requires

#FILE_ROOT = 's3://jncc-data/workflows/s2ard/'
FILE_ROOT = '/tmp/meo-ap'
#DOCKER_IMAGE = '914910572686.dkr.ecr.eu-west-1.amazonaws.com/process-test'

class CreateFTPDump(luigi.Task):
    runDate = luigi.DateParameter(default=datetime.datetime.now())
    ftp = FTPClient()

    def run(self):
        with self.output().open('w') as wddump:
            plist = {}

            print('Getting file list for: daily')
            plist['daily'] = self.ftp.listProductFiles('daily')

            print('Getting file list for: 5day')
            plist['fiveDaily'] = self.ftp.listProductFiles('5day')

            print('Getting file list for: monthly')
            plist['monthly'] = self.ftp.listProductFiles('monthly')

            print('Writing file list')
            json.dump(plist, wddump, indent=4, sort_keys=True, separators=(',', ':'))    
    
    def output(self):
       filePath = os.path.join(os.path.join(FILE_ROOT, self.runDate.strftime("%Y-%m-%d")), 'list.json')  

       return luigi.LocalTarget(filePath)

class TransformSrcFileToTiff(luigi.Task):
    runDate = luigi.DateParameter(default=datetime.datetime.now())
    product = luigi.Parameter()
    srcFile = luigi.Parameter()
    fileDate = luigi.Parameter()

    ftp = FTPClient()
    catalog = CatalogManager()

    def run(self):
        ncFile = os.path.join(os.path.join(FILE_ROOT, self.runDate.strftime("%Y-%m-%d")), self.product + '-' + self.fileDate + '.nc')
        tiffFile = os.path.join(os.path.join(FILE_ROOT, self.runDate.strftime("%Y-%m-%d")), 'UK-' + self.product + '-' + self.fileDate + '.tiff')

        print('Retrieving ' + self.srcFile)
        self.ftp.getFile(self.product, self.srcFile, ncFile)

        os.system('gdal_translate NETCDF:' + ncFile + ':chlor_a -projwin -24 63 6 48 ' + tiffFile)

        self.catalog.addEntry(self.product, 'Chlorophyll-A Density for UK Waters - ' + self.product + ' - ' + self.fileDate, self.srcFile, tiffFile, datetime.datetime.now().strftime("%Y-%m-%d"))
        with self.output().open('w') as outp:
            outp.write('Test\n')

        return

    def output(self):
       filePath = os.path.join(os.path.join(FILE_ROOT, self.runDate.strftime("%Y-%m-%d")), self.product + '-' + self.fileDate + '.tmp')  

       return luigi.LocalTarget(filePath) 

    
class ProcessFiles(luigi.Task):
    runDate = luigi.DateParameter(default=datetime.datetime.now())

    def requires(self):
        return CreateFTPDump(self.runDate)

    def run(self):
        with self.input().open('r') as inp:
            data = json.load(inp)
            for k, v in data['daily'].items():
                yield TransformSrcFileToTiff(self.runDate, 'daily', v, k)
            
        with self.output().open('w') as outp:
            outp.write('Test\n')

    def output(self):
       filePath = os.path.join(os.path.join(FILE_ROOT, self.runDate.strftime("%Y-%m-%d")), 'first.txt')  

       return luigi.LocalTarget(filePath)
        
