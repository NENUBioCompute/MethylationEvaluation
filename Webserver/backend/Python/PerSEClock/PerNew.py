import pandas as pd
import numpy as np
import torch
from torch.utils.data import Dataset
from torch.utils.data import DataLoader
import time
import json
#画图
import matplotlib.pyplot as plt #导入matplotlib模块，并简写成plt
from scipy import optimize
import scipy.stats as stats


#数据处理函数
class MyDataset(Dataset):

    def __init__(self, feature_array, label_array, dtype=np.float32):

        self.features = feature_array.astype(np.float32)
        self.labels = label_array

    def __getitem__(self, index):
        inputs = self.features[index]
        label = self.labels[index]
        return inputs, label

    def __len__(self):
        return self.labels.shape[0]


#模型导入
#SENet注意力机制
pre = []
post = []
class SEAttention(torch.nn.Module):
    def __init__(self, channel=512, reduction=16):
        super().__init__()
        # 池化层，将每一个通道的宽和高都变为 1 (平均值)
        self.avg_pool = torch.nn.AdaptiveAvgPool2d(1)
        self.fc = torch.nn.Sequential(
            # 先降低维
            torch.nn.Linear(channel, channel // reduction, bias=False),
            torch.nn.LeakyReLU(inplace=True),
            # 再升维
            torch.nn.Linear(channel // reduction, channel, bias=False),
            torch.nn.LeakyReLU(inplace=True)
        )

    def forward(self, x):
        b, c, _ , _ = x.size()
        y = self.avg_pool(x).view(b, c)
        y = self.fc(y).view(b, c, 1, 1)
        return x * y.expand_as(x)


class MLP(torch.nn.Module):

    def __init__(self, in_features,num_hidden_1=32,num_hidden_2=32,num_hidden_3=32,num_hidden_4=32):
        super().__init__()
        self.atten = SEAttention(1362)
        self.my_network = torch.nn.Sequential(
            # 1st hidden layer
            torch.nn.Linear(in_features, num_hidden_1, bias=False),
            torch.nn.LeakyReLU(),
            torch.nn.BatchNorm1d(num_hidden_1),
            torch.nn.Dropout(0.1),

            # 2nd hidden layer
            torch.nn.Linear(num_hidden_1, num_hidden_2, bias=False),
            torch.nn.LeakyReLU(),
            torch.nn.BatchNorm1d(num_hidden_2),
            torch.nn.Dropout(0.1),

            # 3nd hidden layer
            torch.nn.Linear(num_hidden_2, num_hidden_3, bias=False),
            torch.nn.LeakyReLU(),
            torch.nn.BatchNorm1d(num_hidden_3),
            torch.nn.Dropout(0.1),

            # 4nd hidden layer
            torch.nn.Linear(num_hidden_3, num_hidden_4, bias=False),
            torch.nn.LeakyReLU(),
            torch.nn.BatchNorm1d(num_hidden_4),
            torch.nn.Dropout(0.1),

            # 5nd hidden layer
            torch.nn.Linear(num_hidden_4, 1, bias=False),

        )

    def forward(self, x):

        x = np.reshape(x,(x.shape[0], 1362,6,3),order='F')
        x = self.atten(x)
        x = x.detach().numpy()
        x = np.reshape(x,(x.shape[0],-1),order='F')
        x = torch.tensor(x)
        x = self.my_network(x)

        return x


#画图函数
def r2(x,y):
    # return r squared
    return stats.pearsonr(x,y)[0] **2

# def plot_known_predicted_ages(known_ages, predicted_ages, label=None):
#     # define optimization function
#     def func(x, a, b, c):
#         return a * np.asarray(x)**0.5 + c
#     # fit trend line
#     popt, pcov = optimize.curve_fit(func, [1 + x for x in known_ages], predicted_ages)
#     # get r squared
#     rsquared = r2(predicted_ages, func([1 + x for x in known_ages], *popt))
#     # format plot label
#     plot_label = f'$f(x)={popt[0]:.2f}x^{{1/2}} {popt[2]:.2f}, R^{{2}}={rsquared:.2f}$'
#     # initialize plt plot
#     fig, ax = plt.subplots(figsize=(8,8))
#     # plot trend line
#     ax.plot(sorted(known_ages), func(sorted([1 + x for x in known_ages]), *popt), 'r--', label=plot_label)
#     # scatter plot
#     ax.scatter(known_ages, predicted_ages, marker='o', alpha=0.8, color='k')
#     ax.set_title(label, fontsize=18)
#     ax.set_xlabel('Chronological Age', fontsize=16)
#     ax.set_ylabel('Predicted Age', fontsize=16)
#     ax.tick_params(axis='both', which='major', labelsize=16)
#     ax.legend(fontsize=16)
#     plt.xlim(0, 100)
#     plt.ylim(0, 100)
#
#     plt.show()

#评价指标计算
def compute_mae_and_mse(model, data_loader, device):
    model = model.eval()
    with torch.no_grad():

        mae, mse, acc, num_examples = 0., 0., 0., 0

        pre_Age = []#预测结果列表
        true_Age = []#实际结果列表

        for i, (features, targets) in enumerate(data_loader):
            features = features.to(device)
            targets = targets.float().to(device)
            logits = model(features)
            predicted_labels = logits.float()
            predicted_labels = predicted_labels.squeeze(1)

            pre_Age += predicted_labels.tolist()
            true_Age += targets.tolist()

            # num_examples += targets.size(0)#0维度的数据数量
            # mae += torch.sum(torch.abs(predicted_labels - targets))
            # mse += torch.sum((predicted_labels - targets)**2)


        #返回预测年龄
        return pre_Age

# 读入数据集预测
geo_check = [
#'GSE56046_1','GSE56046_2','GSE56046_3',
# 'GSE147221_1','GSE147221_2','GSE152027','GSE134379', 'GSE196696',
#'GSE183920_1','GSE183920_2', 'GSE80417', 'GSE117859', 'GSE132203_1','GSE132203_2','GSE132203_3'
# 'GSE80417'
    # 'GSE20242',
    # 'GSE53740',
    # 'GSE64495',
    # 'GSE42861',
    # 'GSE43414',
    # 'GSE59685',
    # 'GSE111223',
    # 'GSE50759',
    # 'GSE61431',
    # 'GSE80261',
    # 'GSE80970',
    # 'GSE74193',
    # 'GSE38873',
    # 'GSE112987',
    # 'GSE152026'

    # 'GSE142439',
    # 'GSE151600',
    # 'GSE151601',
    # 'GSE151602',
    # 'GSE151603',
    # 'GSE151604',
    # 'GSE152026_1',
    # 'GSE152026_2',
    # 'GSE152026_3',
    # 'GSE152026_4',
    # 'GSE152026_5',
    # 'GSE179325_1',
    # 'GSE179325_2',
    # 'GSE198904_1',
    # 'GSE198904_2',
    'cpg_0_0.5_1'
]
#cpg位点读入
cpg_path = "Python/PerSEClock/24516cpg.csv"
cpg = pd.read_csv(cpg_path)
cpg = cpg["cpg"]

#文件路径

for GEO in geo_check:

    # 临床数据
    ph_name = pd.read_csv('/home/data/Standardized/pheno/{}_pheno.csv'.format(GEO))
    check_labels = ph_name["Age"]

    #表达矩阵(行名是特征，列名是样本)####不读入序号列
    check_features = pd.read_csv('/home/data/Standardized/express/{}_beta.csv.gz'.format(GEO),index_col=0,compression='gzip')
    check_features = check_features.T#转置

    #筛选CpG
    # a = [1, 2, 3]
    # b = [0, 1, 2, 3, 4]
    if set(cpg).issubset(set(check_features.columns.values.tolist())) == False:
        set_A = set(check_features.columns.values.tolist())  # 利用无序的概念降低复杂度
        new_list = [item for item in cpg if item not in set_A]
        for i in new_list:
            check_features[i] = 0.5
        # print("缺少的位点数："+str(len(new_list)))
        # print(new_list)
    # print(set(cpg).issubset(set(check_features.columns.values.tolist())))
    # print(check_features.columns.values.tolist())
    data_featuresF = check_features.loc[:,cpg]

    print("样本数",check_labels.shape)
    print("表达矩阵",data_featuresF.shape)

    #不用归一化
    X_Test_std = np.array(data_featuresF)

    # 参数
    # random_seed = 1check_labels
    batch_size = check_labels.shape[0]
    print(batch_size)
    # Other
    # DEVICE = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    DEVICE = torch.device("cpu")
    print('Training on', DEVICE)

    #进入模型前--数据处理
    Test_dataset = MyDataset(X_Test_std, check_labels.values)

    Test_loader = DataLoader(dataset=Test_dataset,
                              batch_size=batch_size,
                              shuffle=False, # want to shuffle the dataset
                              num_workers=0) # number processes/CPUs to use

    # Checking the dataset
    for inputs, labels in Test_loader:
        print('Input batch dimensions:', inputs.shape)
        In_features = inputs.shape[1]
        print('Input label dimensions:', labels.shape)
        break

    model1 = MLP(in_features=In_features)
    model1.load_state_dict(torch.load("/home/lihaixia/MethylationEvaluation/Evaluation/Python/PerSEClock/PerSE_model.pt"))#加载参数

    #测试
    MlpSEAge = compute_mae_and_mse(model1, Test_loader, DEVICE)
    print(GEO)
    print(MlpSEAge)

    # pheno data path
    pheno_path = '/home/data/Standardized/pheno/' + GEO + '_pheno.csv'
    # get  pheno data
    pheno_data = pd.read_csv(pheno_path)
    pheno_data.fillna('Unknown', inplace=True)

    # run R test function
    start_t = time.time()
    end_t = time.time()

    trueAge = pheno_data['Age'].tolist()
    FileName = GEO + "_predicted_by_NO.PerSEClock.json"
    localTime = time.localtime()
    curTime = time.strftime("%Y-%m-%d %H:%M:%S", localTime)
    ageData = {
        "FileName": FileName,
        "datetime": curTime,
        "Algorithm": "NO.PerSEClock",
        "Dataset": GEO,
        # "Age_unit": pheno_data['Age_unit'].tolist()[0],
        "AgeRange": [min(trueAge), max(trueAge)],
        "SampleNum": len(trueAge),
        "ConsumeTime(Sec)": str(round((end_t - start_t), 3)) + 's',
        # "Tissue": pheno_data['Tissue'].tolist(),
        # "Condition": pheno_data['Condition'].tolist(),
        # "Disease": pheno_data['Disease'].tolist(),
        # "Gender": pheno_data['Gender'].tolist(),
        # "Race": pheno_data['Race'].tolist(),
        "ID_REF": pheno_data['ID'].tolist(),
        "PredAge": MlpSEAge,
        "TrueAge": trueAge,
        # "Platform": pheno_data['Platform'].tolist()[0]
    }
    file = '/home/lihaixia/MethylationEvaluation/Evaluation/Result/PerSEClock/' + FileName
    with open(file, 'w') as f:
        json.dump(ageData, f)

    print("hhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhh")
