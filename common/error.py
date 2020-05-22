'''程序错误码'''

OK = 0  # 正常

class LogicError(Exception):
    code = OK
    data = 'OK'

    def __init__(self, data=None):
        cls_name = self.__class__.__name__
        self.data = data or cls_name


def gen_error(name, code):
    '''生成一个logicError的子类(LogicError的工厂函数)'''
    err_cls = type(name, (LogicError,), {'code': code})
    return err_cls


VcodeSendErr = gen_error('VcodeSendErr', 1000)  # 验证码发送失败
VcodeErr = gen_error('VcodeErr', 1001)  # 验证码错误
LoginRequired = gen_error('LoginRequired', 1002)  # 需要用户登入
ProfileErr = gen_error('ProfileErr', 1003)  # 用户资料表单数据错误
SidError = gen_error('SidError', 1004)  # SID 错误
StypeError = gen_error('StypeError', 1005)  # 滑动类型错误
SwiperRepeatErr = gen_error('SwiperRepeatErr', 1006)  # 重复滑动
