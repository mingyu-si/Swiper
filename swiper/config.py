'''
程序自身业务配置 和 第三方平台配置
'''
REDIS = {
    'host': 'localhost',
    'port': 6379,
    'db': 7,
    # 'password':None
}

# 云之讯配置
YZX_API = 'https://open.ucpaas.com/ol/sms/sendsms'
YZX_VCODE_ARGS = {
    'appid': 'a1c285253d104cdd954714e3df5bbdf3',
    'sid': 'cc55474718edc7451fc9d187f1416939',
    'token': '8a114503cdc86bbc010dce6092798b89',
    'templateid': '535424',
    'mobile': None,
    'param': None
}

# 七牛云配置
QN_ACCESS_KEY = 'sychPWY-cnh_kvMAr6R8Y2vbYWEJf1UtHIkQQsWk'
QN_SECRET_KEY = 'I2wt05so9BFDTxtIU0VnmxEO7eTNb17Vf_RVAj5U'
QN_BUCKET = 'uploadavator'
QN_BASEURL = 'http://qaj4kw5fi.bkt.clouddn.com/'
