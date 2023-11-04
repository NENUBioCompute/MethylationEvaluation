import json
import re
import pandas as pd
from flask import Flask, request
from flask_cors import CORS
import os
from Mongo.GetOther import GetOther
from Mongo.GetDataFromDB import GetData
from Mongo.User import User
from timepredict.time_predict import time_predict
from Clocks.RunClocks import DNAAgePredictor
import smtplib
from smtplib import SMTP_SSL
from email.mime.text import MIMEText
from email.header import Header
app = Flask(__name__)
CORS(app)
import rpy2.robjects as robjects



@app.route('/')
def hello_world():
    return 'Hello'

#按钮功能，负责接受数据并检测上传格式等
@app.route('/api/upload', methods=['POST', 'GET'])
def upload():
    print('________first working________')
    beta_file = request.files.get('beta')
    pheno_file = request.files.get('pheno')
    # 保存文件
    beta_file_path = os.path.join("./data/beta/", beta_file.filename)
    pheno_file_path = os.path.join("./data/pheno/", pheno_file.filename)
    beta_file.save(beta_file_path)
    pheno_file.save(pheno_file_path)
    beta_reader = open(beta_file_path, 'r')
    beta_head_string = beta_reader.readline()
    beta_head_list = beta_head_string.split('","')
    if (beta_head_list.__len__() < 2):
        return 'BetaHeadErr'
    head_check = re.search('GSM', beta_head_list[1])
    if (head_check == None):
        return 'BetaHeadErr'
    beta_line_num = 0
    while beta_head_string.__len__() > 0 :
        beta_line_num = beta_line_num+1
        beta_head_string = beta_reader.readline()
    print(beta_line_num)
    print(beta_head_list.__len__())
    phone_head_reader = open(pheno_file_path, 'r')
    phone_head_string = phone_head_reader.readline()
    phone_head_list_a = phone_head_string.split('\n')
    phone_head_list = phone_head_list_a[0].split(',')
    phone_head_map = ['ID', 'Tissue', 'Disease', 'Condition', 'Age', 'Age_unit', 'Gender', 'Race', 'Platform']
    for phone_head_one in phone_head_map:
        if not phone_head_one in phone_head_list:
            return 'PhoneHeadErr'
    phone_num = 0
    while phone_head_string.__len__() > 0:
        phone_num = phone_num + 1
        phone_head_string = phone_head_reader.readline()
        if phone_head_string.__len__()>0:
            if re.match('GSM',phone_head_string) == None :
                return 'PhoneIdErr'
    if phone_num > 20:
        return 'TooMuchErr'
    data = pd.read_csv(beta_file_path, nrows=5)
    ph = pd.read_csv(pheno_file_path)
    clocks = request.form.get('clocks').split(',')
    print(clocks)
    if ph['ID'].tolist() != data.columns.tolist()[1:]:
        return 'IDMismatch'
    # 实例化类
    file = "../data/beta/" + beta_file.filename
    # predictor = DNAAgePredictor(beta_file.filename, pheno_file.filename, fill_value=0.5)
    # age = predictor.predict_age(clocks)
    # task = GetOther()
    # print(task_info)
    # task.insert_task(task_info)
    print(beta_line_num)
    print(phone_num)
    print(time_predict(clocks, beta_line_num, phone_num))
    return str(round(time_predict(clocks, beta_line_num, phone_num),3))

#wait页面的功能，负责费事的数据处理
@app.route('/api/upload_back', methods=['POST', 'GET'])
def upload_back():
    print('___________second working___________')
    beta_file = request.files.get('beta')
    pheno_file = request.files.get('pheno')
    # 保存文件
    beta_file_path = os.path.join("./data/beta/", beta_file.filename)
    pheno_file_path = os.path.join("./data/pheno/", pheno_file.filename)
    beta_file.save(beta_file_path)
    pheno_file.save(pheno_file_path)
    data = pd.read_csv(beta_file_path, nrows=5)
    ph = pd.read_csv(pheno_file_path)
    clocks = request.form.get('clocks').split(',')
    print(clocks)
    if ph['ID'].tolist() != data.columns.tolist()[1:]:
        return 'IDMismatch'
    task_info = {
        'task_id': request.form.get('taskID'),
        'user_name': request.form.get('userName'),
        'email': request.form.get('email'),
        'beta_data': beta_file.filename,
        'pheno_data': pheno_file.filename,
        'tissue': request.form.get('tissue'),
        'age_unit': request.form.get('ageUnit'),
        'imputation': request.form.get('imputation'),
        'clocks': clocks
    }
    # 实例化类
    file = "../data/beta/" + beta_file.filename
    predictor = DNAAgePredictor(beta_file.filename, pheno_file.filename, fill_value=0.5)
    age = predictor.predict_age(clocks)
    task = GetOther()
    print(task_info)
    task.insert_task(task_info)
    return 'success'

# 结果状态
@app.route('/api/resStatus', methods=['GET'])
def get_res_status():
    f = open('Result/GSE20242_predicted.json')
    data = json.load(f)
    print(data)
    return data


@app.route('/api/clocks', methods=['GET', 'POST'])
def get_clocks():
    clock = GetOther()
    clocks_list = clock.get_clocks()
    clock_data = {'data': clocks_list}
    return clock_data


@app.route('/api/getAgeUnits', methods=['GET', 'POST'])
def get_age_units():
    types = request.get_json(silent=True)
    print(types)
    return 'success'


# 登录
@app.route('/api/login', methods=['GET', 'POST'])
def login():
    email = request.form.get('email')
    password = request.form.get('password')
    print(email)
    print(password)
    user = User()
    res = user.get_user(email, password)
    if res is False:
        return 'error'
    return res


# 注册
@app.route('/api/register', methods=['GET', 'POST'])
def register():
    register_data = {
        'firstName': request.form.get('fname'),
        'lastName': request.form.get('lname'),
        'Email': request.form.get('Email'),
        'password': request.form.get('password'),
        'institution': request.form.get('institution'),
        'country': request.form.get('country'),
        'title': request.form.get('title'),
        'status': request.form.get('status')
    }
    user = User()
    res = user.add_user(register_data)
    print(res)
    return 'success'


# 验证邮箱
@app.route('/api/checkEmail', methods=['GET', 'POST'])
def check_email():
    email = request.form.get('email')
    print(email)
    user = User()
    if user.check(email):
        return 'success'
    else:
        return 'unsuccess'


# 修改密码
@app.route('/api/resetPsw', methods=['GET', 'POST'])
def reset_psw():
    email = request.form.get('Email')
    password = request.form.get('password')
    user = User()
    if user.update_psw(email, password):
        return 'success'
    else:
        return 'unsuccess'


# 获取数据集
@app.route('/api/dataset', methods=['GET'])
def get_dataset():
    get_data = GetData()
    data = get_data.get_dataset_data()
    return {'data': data}


# 获取疾病、组织、种族
@app.route('/api/tissue', methods=['GET'])
def get_tissue():
    get_data = GetData()
    data = get_data.get_tissue_data()
    return {'data': data}


# 获取疾病、组织、种族
@app.route('/api/race', methods=['GET'])
def get_race():
    get_data = GetData()
    data = get_data.get_race_data()
    return {'data': data}


# 获取疾病、组织、种族
@app.route('/api/disease', methods=['GET'])
def get_disease():
    get_data = GetData()
    data = get_data.get_disease_data()
    return {'data': data}


@app.route('/api/email_che', methods=['POST'])
def email_che():
    print('worked')
    answer_mail = request.form.get('beta')
    print(answer_mail)
    print(request.form.get('email'))
    mail_host = "smtp.163.com"
    mail_user = "taomi208874@163.com"
    mail_pass = "VDNZXWOSIMGOWIVK"
    receivers = request.form.get('email')
    message = MIMEText('Thanks for using our web', 'plain', 'utf-8')
    subject = 'Your CAPTCHA: '+str(answer_mail)
    message['Subject'] = Header(subject, 'utf-8')
    try:
        smtpObj = SMTP_SSL(mail_host)
        smtpObj.login(mail_user, mail_pass)
        smtpObj.sendmail(mail_user, receivers, message.as_string())
        print("邮件发送成功")
    except smtplib.SMTPException:
        print("Error: 无法发送邮件")
    return 'success'

@app.route('/api/email_send', methods=['POST'])
def email_send():
    print('answer:')
    print(request.form.get('email'))
    # 三个参数：第一个为文本内容，第二个 plain 设置文本格式，第三个 utf-8 设置编码
    # message = MIMEText('data are Accessible at http://47.99.71.176:8080/#/result', 'plain', 'utf-8')
    # message['Subject'] = "Your data have been analyzed"
    mail_host = "smtp.163.com"
    mail_user = "taomi208874@163.com"
    mail_pass = "VDNZXWOSIMGOWIVK"
    receivers = request.form.get('email')
    message = MIMEText('data are Accessible at http://47.99.71.176:8080/#/result', 'plain', 'utf-8')
    subject = 'Your data have been analyzed'
    message['Subject'] = Header(subject, 'utf-8')
    try:
        smtpObj = SMTP_SSL(mail_host)
        smtpObj.login(mail_user, mail_pass)
        smtpObj.sendmail(mail_user, receivers, message.as_string())
        print("邮件发送成功")
    except smtplib.SMTPException:
        print("Error: 无法发送邮件")
    return 'success'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8807)
