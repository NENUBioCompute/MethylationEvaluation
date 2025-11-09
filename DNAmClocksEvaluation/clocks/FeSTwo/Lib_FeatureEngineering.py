import pandas as pd
import numpy as np
from scipy.stats import pearsonr
from sklearn.svm import LinearSVR
import pickle
import random
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from sklearn import preprocessing
from multiprocessing import Pool


# ****************************NewFeatures dependency Functions****************************
# ****************************DiffGender & MulTwo****************************
def CalPearsonr(col, data_y, data_x):
    return pearsonr(data_x[col], data_y)[0]


def GetAllPearsonr(data_x, data_y):
    dic = {}
    for i in data_x.columns:
        dic[i] = abs(CalPearsonr(i, data_y, data_x))
    return dic


def GeneCols(data_x, data_y, col1, col2, dic, threshold):
    tmp_dict = {}
    for i in ['plus', 'subtract', 'multi', 'devide']:
        if i == 'plus':
            tmp = data_x[col1] + data_x[col2]
        elif i == 'subtract':
            tmp = data_x[col1] - data_x[col2]
        elif i == 'multi':
            tmp = data_x[col1] * data_x[col2]
        else:
            tmp1 = data_x[col1] / data_x[col2]
            tmp2 = data_x[col2] / data_x[col1]
            tmp = [tmp1, tmp2]
        if isinstance(tmp, list):
            tmp_p = abs(pearsonr(tmp[0], data_y)[0])
            if tmp_p - dic[col1] > threshold and tmp_p - dic[col2] > threshold:
                tmp_dict[col1 + '_' + i + '_' + col2] = tmp[0]
            tmp_p = abs(pearsonr(tmp[1], data_y)[0])
            if tmp_p - dic[col1] > threshold and tmp_p - dic[col2] > threshold:
                tmp_dict[col2 + '_' + i + '_' + col1] = tmp[1]
        else:
            tmp_p = abs(pearsonr(tmp, data_y)[0])
            if tmp_p - dic[col1] > threshold and tmp_p - dic[col2] > threshold:
                tmp_dict[col1 + '_' + i + '_' + col2] = tmp
    return pd.DataFrame(data=tmp_dict)


# ****************************Week Model****************************
def Stratified(mode, data_other, n_bins, n_frac, random_seed):
    data = data_other.copy()
    data['age'] = data['age'].astype('int')
    data['raw_index'] = [i for i in range(data.shape[0])]
    data = data.sort_values('age')
    LabelIndex = pd.cut(data['age'].values.tolist(), bins=n_bins, labels=[i for i in range(n_bins)])
    data['LabelIndex'] = list(LabelIndex)
    Index = []
    if mode == 'RandomSampling':
        for i in range(n_bins):
            tmp = data[data['LabelIndex'] == i]
            tmp = tmp.sample(frac=n_frac, random_state=random_seed)
            Index += tmp['raw_index'].tolist()
    elif mode == 'Resampling':
        for i in range(n_bins):
            tmp = data[data['LabelIndex'] == i]
            tmp['new_index'] = [_ for _ in range(tmp.shape[0])]
            np.random.seed(random_seed)
            idx = np.random.randint(0, tmp.shape[0], size=int(n_frac * tmp.shape[0]))
            Index += tmp.iloc[idx]['raw_index'].tolist()
    return Index


def Sample(mode, data_other, random_seed, n_bins, n_frac):
    if mode == 'Resampling':
        if n_bins == 0:
            np.random.seed(random_seed)
            idx = np.random.randint(0, data_other.shape[0], size=int(n_frac * data_other.shape[0]))
        else:
            idx = Stratified(mode, data_other, n_bins, n_frac, random_seed)
    elif mode == 'RandomSampling':
        if n_bins == 0:
            tmp = data_other.sample(frac=n_frac, random_state=random_seed)
            idx = tmp.index.tolist()
        else:
            idx = Stratified(mode, data_other, n_bins, n_frac, random_seed)
    return idx


def SampleCols(columns, random_seed, n_frac):
    random.seed(random_seed)
    sample_cols = random.sample(columns, int(len(columns) * n_frac))
    return sample_cols


# 返回弱分类器预测值组成的矩阵
def StackingFeatures(clf, mode, n_bins, n_frac_samples, n_frac_cols, data_gene, data_other, nums):
    data_y = data_other['age']
    F = np.zeros((data_gene.shape[0], nums))
    for i in range(nums):
        idx = Sample(mode, data_other, i, n_bins, n_frac_samples)
        cols = SampleCols(data_gene.columns.tolist(), i, n_frac_cols)
        clf.fit(data_gene.iloc[idx][cols], data_y.iloc[idx])
        pre = clf.predict(data_gene[cols])
        F[:, i] = pre
    '''
    if MinMaxScaler_:
        scaler = MinMaxScaler()
        scaler.fit(F)
        F = scaler.transform(F)
        '''
    data_gene = preprocessing.scale(F)
    data_gene = pd.DataFrame(data=data_gene)

    return data_gene


# ****************************NewFeatures****************************
class NewFeatures(object):
    'Used for generating features.\
    Dif_cols::Difference between the group\'s mean value and the true value.\
    AbsDif_cols:The absolute value of the difference between the group\'s mean value and the true value.\
    ComFea:Features combination with arithmetic.'

    def __init__(self, *initial_data, n_jobs, type_='DifAbs', threshold=0.1, **kwargs):
        self.type_ = type_
        self.threshold = threshold
        self.n_jobs = n_jobs
        for dictionary in initial_data:
            for key in dictionary:
                setattr(self, key, dictionary[key])
        for key in kwargs:
            setattr(self, key, kwargs[key])

            # ****************Add_Diff_Abs*******************

    def AddFeatures_DiffGender(self, data_x, data_y, data_gender):
        length = data_x.shape[1]
        data = data_x.copy()
        data['gender'] = data_gender
        category_columns = 'gender'
        features = [col for col in data.columns if col not in ['gender']]
        new_df = pd.DataFrame()
        for col in features:
            tmp_df = data[[category_columns, col]]
            group_mean_df = tmp_df.groupby(category_columns)[col].agg([('tmp_mean', np.mean)]).reset_index()
            t_df = pd.merge(tmp_df, group_mean_df, how='left', on=category_columns)
            t_df[col + '*diff'] = t_df[col] - t_df['tmp_mean']
            t_df[col + '*diff*abs'] = np.abs(t_df[col + '*diff'])
            new_df = pd.concat([new_df, t_df[[col + '*diff', col + '*diff*abs']]], axis=1)
        if length * 2 == new_df.shape[1]:
            print('Diff,diff_abs success')
        else:
            print('Error')
        return new_df

    # ****************Add_Diff_Abs*******************

    # ***************Add_combination*****************
    def AddFeatures_MulTwo(self, data_x, data_y, data_gender):
        features = [col for col in data_x]
        label_cols = 'age'
        result_df = pd.DataFrame()
        dic = GetAllPearsonr(data_x, data_y)
        print(len(dic))
        p = Pool(self.n_jobs)
        res = []
        print(len(features))
        for i in range(len(features)):
            for j in range(len(features)):
                if j > i:
                    res.append(p.apply_async(GeneCols, \
                                             args=(data_x, data_y, features[i], features[j], dic, self.threshold)))
        p.close()
        p.join()
        result_df = pd.DataFrame()
        # np.isinf(res).sum()
        print(len(res))
        # for i in res:
        #     tmp_df = i.get()
        #     result_df=pd.concat([result_df,tmp_df],axis=1)
        for num, i in enumerate(res):
            # try:
            #     tmp_df = i.get()
            #     # print(tmp_df)
            # except:
            #     tmp_df = np.array(len(result_df[num-1]))
            tmp_df = i.get()
            result_df = pd.concat([result_df, tmp_df], axis=1)

        result_df = result_df.replace(np.inf, np.nan)
        result_df['gender'] = data_gender
        result_df = result_df.groupby('gender').transform(lambda x: x.fillna(x.mean()))
        return result_df

    def AddFeatures_Square(self, data_x):
        Square_df = np.square(data_x)
        Square_df.columns = [i + '**2' for i in data_x.columns]
        return Square_df

    def AddFeatures_WeekModel(self, data_x, data_other):
        result_df = StackingFeatures(self.clf, self.mode, self.n_bins, self.n_frac_samples, self.n_frac_cols, \
                                     data_x, data_other, self.nums)
        return result_df

    # ***************Add_combination*****************

    # ********************transform***********************
    def transform(self, data_x, data_y=pd.DataFrame(), data_gender=pd.DataFrame()):
        data_other = pd.concat([data_y, data_gender], axis=1)
        if self.type_ == 'DifAbs':
            features_df = self.AddFeatures_DiffGender(data_x, data_y, data_gender)
        elif self.type_ == 'MulTwo':
            features_df = self.AddFeatures_MulTwo(data_x, data_y, data_gender)
        elif self.type_ == 'Square':
            features_df = self.AddFeatures_Square(data_x)
        elif self.type_ == 'WeakModel':
            features_df = self.AddFeatures_WeekModel(data_x, data_other)
        else:
            print('type_: Error!')
        return features_df