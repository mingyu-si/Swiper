'''程序错误码'''

OK = 0  # 正常


class LogicError(Exception):
    code = OK
    data = 'OK'

    def __init__(self, data=None):
        cls_name = self.__class__.__name__
        self.data = data or cls_name


def gen_logic_error(name, code):
    '''生成一个logicError的子类(LogicError的工厂函数)'''
    err_cls = type(name, (LogicError,), {'code': code})  # type 是所有类的元类
    return err_cls


VcodeSendErr = gen_logic_error('VcodeSendErr', 1000)  # 验证码发送失败
VcodeErr = gen_logic_error('VcodeErr', 1001)  # 验证码错误
LoginRequired = gen_logic_error('LoginRequired', 1002)  # 需要用户登入
ProfileErr = gen_logic_error('ProfileErr', 1003)  # 用户资料表单数据错误
SidError = gen_logic_error('SidError', 1004)  # SID 错误
StypeError = gen_logic_error('StypeError', 1005)  # 滑动类型错误
SwiperRepeatErr = gen_logic_error('SwiperRepeatErr', 1006)  # 重复滑动
RewindLimitErr = gen_logic_error('RewindLimitErr', 1007)  # 反悔次数达到限制
RewindTimeout = gen_logic_error('RewindTimeout', 1008)  # 反悔超时
NonSwiper = gen_logic_error('NonSwiper', 1009)  # 当前用户还没有滑动记录
