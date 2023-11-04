import os
import json
geo = ['GSE61257', 'GSE41169', 'GSE75248', 'GSE77136', 'GSE20242', 'GSE109042', 'GSE27097', 'GSE30870', 'GSE34035',
           'GSE32146', 'GSE64511', 'GSE32867', 'GSE87571', 'GSE67705', 'GSE36064', 'GSE17448', 'GSE137894', 'GSE71245',
           'GSE151602', 'GSE58045', 'GSE38873', 'GSE80261', 'GSE148000', 'GSE49908', 'GSE56105', 'GSE62867',
           'GSE137502', 'GSE142439', 'GSE151600', 'GSE151603', 'GSE53128', 'GSE61431', 'GSE20236', 'GSE67024',
           'GSE59685', 'GSE53740', 'GSE94876', 'GSE76105', 'GSE72338', 'GSE72556', 'GSE74193', 'GSE80970', 'GSE71678',
           'GSE151601', 'GSE37008', 'GSE137495', 'GSE23638', 'GSE51954', 'GSE26126', 'GSE15745', 'GSE77241', 'GSE72773',
           'GSE34257', 'GSE36194', 'GSE112987', 'GSE40005', 'GSE73832', 'GSE32149', 'GSE61496', 'GSE83334', 'GSE38608',
           'GSE59509', 'GSE62219', 'GSE61258', 'GSE115797', 'GSE54211', 'GSE137903', 'GSE32396', 'GSE32393', 'GSE94734',
           'GSE22595', 'GSE38291', 'GSE27317', 'GSE73103', 'GSE57484', 'GSE101764', 'GSE108213', 'GSE99029', 'GSE30601',
           'GSE137884', 'GSE32148', 'GSE37988', 'GSE28746', 'GSE41826', 'GSE42861', 'GSE44763', 'GSE57285', 'GSE69176',
           'GSE36054', 'GSE41037', 'GSE77445', 'GSE111223', 'GSE56342', 'GSE72775', 'GSE63106', 'GSE137898', 'GSE56606',
           'GSE65638', 'GSE42700', 'GSE31979', 'GSE40279', 'GSE49904', 'GSE63384', 'GSE90124', 'GSE152026', 'GSE78874',
           'GSE101961', 'GSE137688', 'GSE30758', 'GSE43414', 'GSE137841', 'GSE59157', 'GSE49905', 'GSE50759',
           'GSE137904', 'GSE58119', 'GSE19711', 'GSE50660', 'GSE40360', 'GSE72777', 'GSE50498', 'GSE48325', 'GSE56581',
           'GSE151604', 'GSE99624', 'GSE36812', 'GSE73377', 'GSE48988', 'GSE59457', 'GSE138279', 'GSE25892', 'GSE64495',
           'GSE90060', 'GSE60132', 'GSE92767', 'GSE55763']
for i in geo:
    FileName_15 = '/home/zongxizeng/MissCpGTest/Result/15/' + i + "_predicted_by_NO.15.json"
    FileName_22 = '/home/zongxizeng/MissCpGTest/Result/22/' + i + "_predicted_by_NO.22.json"
    FileName_09 = '/home/zongxizeng/MissCpGTest/Result/09/' + i + "_predicted_by_NO.09.json"
    if os.path.exists(FileName_15):
        with open(FileName_15, "r") as f:
            data = json.load(f)
        no_geo = []
        if data['PredAge'][0] == '':
            no_geo.append(i)
    else:
        print(i)
        print('not exists')