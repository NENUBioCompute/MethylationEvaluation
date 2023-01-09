# @Author : Jing.Qu
# @Time :2022/12/22

import os
from optparse import OptionParser
import traceback
from MethylationEvaluation.Utilities.NetDownloads.HttpDownloader import HTTP
from MethylationEvaluation.Utilities.FileDealers.ConfigParser import ConfigParser
from MethylationEvaluation.Utilities.FileDealers.TxtFileDealer import TxtFileDealer
from MethylationEvaluation.Utilities.FileDealers.Uncompress import Uncompress

class MethylationDownloader:
    '''
    Download the methylation data
    '''

    def start(self):
        '''
        You can download data based on the source and destination addresses in the configuration file
        @return: None
        '''
        config = ConfigParser.GetConfig('../conf/MethylationData.config')
        download_list = config.get('DataSources', 'source_url')
        urls = TxtFileDealer.IterRead(download_list)
        for url in urls:
            url = url[0]
            local_path, filename = config.get('DataSources', 'download_data_path'), url.split('/')[-1]
            uncompress_path = config.get('DataSources', 'uncompress_data_path')
            try:
                data_path = os.path.join(local_path, filename)
                HTTP.DownLoad(url, local_path, filename)
            except Exception:
                try:
                    HTTP.DownLoad(url, local_path, filename)
                except Exception:
                    traceback.print_exc()
        Uncompress.start(local_path, uncompress_path)

    def pause(self):
        pass

    def stop(self):
        pass

    def get_status(self):
        pass


if __name__ == '__main__':

    optparse = OptionParser()
    optparse.add_option(
        "-s",
        "--start",
        action="store_true",
        dest="start",
    )
    (options, args) = optparse.parse_args()

    d = MethylationDownloader()
    d.start()

