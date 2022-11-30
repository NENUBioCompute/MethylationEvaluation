##!/usr/bin/python3
"""
Author: J.QU
Purpose: Record the Mapping argparse
Created: 11/28/2022
"""
import argparse

def get_argparse():
    parser = argparse.ArgumentParser()
    parser.add_argument('--LogDir', type=str, default='./log',
                        help='Log dir path')
    parser.add_argument('--DataMappingPath', type=str, default='../Datasets/DataMapping_V2.xlsx',
                        help='DataMapping file path')
    parser.add_argument("--ValueMappingPath", type=str, default='../Datasets/ValueMapping_V3.xlsx',
                        help='ValueMapping file path')
    parser.add_argument("--DirPath", type=str, default='../Datasets/orignal',
                        help='dir path of saving the orignal heading file')
    parser.add_argument("--SavePath", type=str, default='../Datasets/mapped_lv3',
                        help='dir path of saving the mapped heading file')
    parser.add_argument("--data_col", type=list,
                        default=['GEO ID', 'Tissue', 'Disease', 'Condition', 'Age', 'Age_unit', 'Gender', 'Race'],
                        help='extract columns of ValueMapping-tissue ')
    parser.add_argument("--tissue_col", type=list,
                        default=['GEO ID', 'Unique Value', 'Tissue lvl1', 'Tissue lvl2', 'Tissue lvl3'],
                        help='extract columns of ValueMapping-tissue ')
    parser.add_argument("--disease_col", type=list,
                        default=['GEO ID', 'Unique Value', 'Disease'],
                        help='extract columns of ValueMapping-disease ')
    parser.add_argument("--age_col", type=list,
                        default=['GEO ID', 'Unique Value', 'Age'],
                        help='extract columns of ValueMapping-age ')
    parser.add_argument("--gender_col", type=list,
                        default=['GEO ID', 'Unique Value', 'Gender'],
                        help='extract columns of ValueMapping-gender ')
    parser.add_argument("--condition_col", type=list,
                        default=['GEO ID', 'Unique Value', 'Condition'],
                        help='extract columns of ValueMapping-condition ')
    parser.add_argument("--race_col", type=list,
                        default=['GEO ID', 'Unique Value', 'Race lvl1', 'Race lvl2'],
                        help='extract columns of ValueMapping-race')
    parser.add_argument("--tissue_word", type=str,
                        default='Tissue lvl3',
                        help='Mapping level of tissue ')
    parser.add_argument("--disease_word", type=str,
                        default='Disease',
                        help='Mapping level of disease ')
    parser.add_argument("--age_word", type=str,
                        default='Age',
                        help='Mapping level of age ')
    parser.add_argument("--gender_word", type=str,
                        default='Gender',
                        help='Mapping level of gender ')
    parser.add_argument('-conditionW', "--condition_word", type=str,
                        default='Condition',
                        help='Mapping level of condition ')
    parser.add_argument('-raceW', "--race_word", type=str,
                        default='Race lvl2',
                        help='Mapping level of race')
    parser.add_argument('-Ft', "--Fetch", type=str,
                        default='ALL',
                        help='according to this value to fetch mapping dict')
    return parser