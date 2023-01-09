"""
  Author:  Jing.Qu
  Purpose: Process Excel files
  Created: 2022.12.25
"""
import pandas as pd
from MethylationEvaluation.Utilities.FileDealers.FileSystem import *


class ExcelDealer:
    """
     Process Excel files
    """
    def __init__(self):
        pass

    @staticmethod
    def IterReadRoWMatrix(file_path: str, sheet_name: str):
        """
        Iteratively read rows. Note: need to assign sheet name.
        :param file_path:
        :param sheet_name:
        :return:
        """
        if file_is_exists.__func__(file_path):
            sheet = pd.read_excel(file_path, sheet_name=sheet_name)
            for row in sheet.itertuples():
                yield row
        else:
            raise Exception("FileNotFound")

    @staticmethod
    def MultiExcelReader(params_dict):
        """
        read the excel file
        :param params_dict:
        :return:
        """
        for item, infor in params_dict.items():
            yield pd.read_excel(infor['path'], sheet_name=infor['sheet'])[params_dict[item]['columns'].split(', ')]

    @staticmethod
    def MultiSheetWriterFromDict(report_excel_file, report_dict):
        writer = pd.ExcelWriter(report_excel_file, engine='openpyxl')
        for sheet_name, _dict in report_dict.items():
            report_df = pd.DataFrame({index: item for index, item in enumerate(zip(*_dict.items()))})
            report_df.to_excel(excel_writer=writer, sheet_name=sheet_name, index=False, header=False)
        writer.save()
        writer.close()
