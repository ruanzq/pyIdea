# python 接口缓存设计
# 适用于统计之类的接口缓存数据
# 不适用于分页之类的接口
# author：ruanzq
# GitHub：ruanzq.github.com
import time,random

# ----------- 缓存模块 -----------
cachepool = {}

def getOrSetCache(key,func):
	print(key)
	data = _getCache(key)
	if not data:
		data = _setCache(key,func)
	return data

def _getCache(key):
	return cachepool.get(key,None)

def _setCache(key,func):
	cachepool[key] = func() if callable(func) else func
	return cachepool[key]

# 转JSON装饰器
def jsonApi(func):
	def nameless(*args,**kwargs):
		import json
		import time
		import random
		start = time.time()
		data = func(*args,**kwargs)
		end = time.time()
		result = {
			"time":str(end-start),
			"data":data,
			"sign":random.randint(1,100)
		}
		return json.dumps(result)
	return nameless

# 缓存装饰器
def publicCache(key):
	def wrap(func):
		def nameless(*args,**kwargs):
				return getOrSetCache(key,func(*args,**kwargs))
		return nameless
	return wrap

@jsonApi
@publicCache(key=time.time())
def api(name):
	import datetime
	v = datetime.datetime.now()
	return {
	"time":str(v),
	"name":name,
	}

for i in range(5):
	print(api(random.randint(1,10)))
	time.sleep(1)
