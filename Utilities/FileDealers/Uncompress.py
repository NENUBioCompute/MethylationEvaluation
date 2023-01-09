"""
@Author  ：Jing.Qu
@File    ：Uncompress.py
@Purpose ：Offer the common uncompress method
@Created ：2022.12.22
"""

import os
import gzip
import tarfile
import zipfile
import rarfile


class Uncompress:
    """
    uncompress the zipped file that compress in popular methods,
    and then save to a new path
    """
    def __init__(self):
        pass

    def start(self, file_path, save_dir):
        """
        uncompress file and save to a new path
        :param file_path: the zipped file
        :param save_dir: for save as unzipped file
        :return:
        """
        suffix = file_path.split('.')[-1]
        if suffix == 'gz':
            self.__un_gz(file_path, save_dir)
        elif suffix == 'tar':
            self.__un_tar(file_path, save_dir)
        elif suffix == 'zip':
            self.__un_zip(file_path, save_dir)
        elif suffix == 'rar':
            self.__un_rar(file_path, save_dir)

    def __un_gz(self, file_path, save_dir):
        """
        ungz zip file
        :param file_path:
        :return:
        """
        file_name = file_path.replace(".gz", "").split('/')[-1]
        save_path = os.path.join(save_dir, file_name)
        g_file = gzip.GzipFile(file_path)
        open(save_path, "wb+").write(g_file.read())
        g_file.close()

    def __un_tar(self, file_path, save_dir):
        """
        untar zip file
        :param file_name
        :return:
        """
        file_name = file_path.replace(".tar", "").split('/')[-1]
        save_path = os.path.join(save_dir, file_name)
        tar = tarfile.open(file_path)
        names = tar.getnames()
        for name in names:
            tar.extract(name, save_path)
        tar.close()

    def __un_zip(self,  file_path, save_dir):
        """
        unzip zip file
        :param file_name:
        :return:
        """
        file_name = file_path.replace(".zip", "").split('/')[-1]
        save_path = os.path.join(save_dir, file_name)
        zip_file = zipfile.ZipFile(file_path)
        for names in zip_file.namelist():
            zip_file.extract(names, save_path)
        zip_file.close()

    def __un_rar(self,  file_path, save_dir):
        """
        unrar zip file
        :param file_name:
        :return:
        """
        file_name = file_path.replace(".rar", "").split('/')[-1]
        save_path = os.path.join(save_dir, file_name)
        rar = rarfile.RarFile(file_path)
        rar.extractall(save_path)
        rar.close()


if __name__ == '__main__':

    def get_filelist(dir_path, file_list):
        """
        Recursively fetch the file list under the dir
        :param dir_path:
        :return:
        """
        if os.path.isfile(dir_path):
            file_list.append(dir_path)
        elif os.path.isdir(dir_path):
            for file in os.listdir(dir_path):
                newDir = os.path.join(dir_path, file)
                get_filelist(newDir, file_list)
        return file_list

    nc = Uncompress()
    dir_path = '/home/data/Download'
    save_path = '/home/data/Uncompressed'
    file_list = get_filelist(dir_path, [])
    for file_path in file_list:
        nc.start(file_path, save_path)

