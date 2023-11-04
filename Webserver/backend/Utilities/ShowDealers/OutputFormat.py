
import json
import datetime

def output_format(**params):
    output = {'FileName': '{}_predicted_by_NO.{}.json'.format(params['GSE'], params['NO']),
              'datetime': str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')),
              'Algorithm': 'NO.{}_{}'.format(params['NO'], params['model_name']),
              'Dataset': params['GSE'],
              'FeaType': params['fea_type'],
              'AgeRange': params['age_range'],
              'SampleNum': params['sample_num'],
              'ConsumeTime(Min)': params['consume_time'],
              'Tissue': list(params['tissue']),
              'ID_REF': list(params['id_ref']),
              'PredAge': list(np.array(params['pred'], dtype='float64')),
              'TrueAge': list(np.array(params['true'], dtype='float64'))
             }
    with open('{}_predicted_by_NO.{}.json'.format(params['GSE'], params['NO']), 'w') as jf:
        json.dump(output, jf, indent=4, ensure_ascii=False)