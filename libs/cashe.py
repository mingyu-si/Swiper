from pickle import dumps, loads, HIGHEST_PROTOCOL, UnpicklingError

from redis import Redis as _Redis

from swiper.config import REDIS


class Redis(_Redis):
    def set(self, name, value, ex=None, px=None, nx=False, xx=False, keepttl=False):
        pickled_data = dumps(value)  # 将需要保存到 Redis 中的值进行序列化
        return super().set(name, pickled_data, ex, px, nx, xx)  # super()调用父类的方法

    def get(self, name, default=None):
        picked_data = super().get(name)
        if picked_data is None:
            return default
        else:
            try:
                value = loads(picked_data)
            except UnpicklingError:
                return picked_data
            else:
                return value

    def hmset(self, name, mapping):
        for k, v in mapping.items():
            mapping[k] = dumps(v, HIGHEST_PROTOCOL)
        return super().hmset(name, mapping)

    def hmget(self, name, keys, *args):
        value_list = super().hmget(name, keys, *args)
        for idx, value in enumerate(value_list):
            if value is not None:
                try:
                    value_list[idx] = loads(value)
                except UnpicklingError:
                    pass

    def hgetall(self, name):
        mapping = super().hgetall(name)
        for k, v in mapping.items():
            try:
                mapping[k] = loads(v)
            except UnpicklingError:
                pass
        return mapping


rds = Redis(**REDIS)  # Redis 连接的单例
