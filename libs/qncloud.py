from qiniu import Auth, put_file, etag
import qiniu.config

from swiper import config


def upload_to_qncloud(filepath, filename):
    '''将文件上传到七牛云'''
    # 构建鉴权对象
    qn_auth = Auth(config.QN_ACCESS_KEY, config.QN_SECRET_KEY)

    # 生成上传 Token，可以指定过期时间等
    token = qn_auth.upload_token(config.QN_BUCKET, filename, 3600)

    # 要上传文件的本地路径
    result, info = put_file(token, filename, filepath)

    # 拼接文件链接
    file_url = '%s%s' % (config.QN_BASEURL, filename)
    return file_url


def upload_data_to_qncloud(filename, filedata):
    '''将文件的数据上传到七牛云'''
    # 构建鉴权对象
    qn_auth = Auth(config.QN_ACCESS_KEY, config.QN_SECRET_KEY)

    # 生成上传 Token，可以指定过期时间等
    token = qn_auth.upload_token(config.QN_BUCKET, filename, 3600)

    # 要上传文件的本地路径
    result, info = put_file(token, filename, filepath)

    # 拼接文件链接
    file_url = '%s%s' % (config.QN_BASEURL, filename)
    return file_url
