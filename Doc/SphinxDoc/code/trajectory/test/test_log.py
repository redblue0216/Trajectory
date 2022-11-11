import logging
import datetime
import json
import pymongo 
import yaml
import trajectory as tjtr




trajectory_package_path = tjtr.__file__.replace('__init__.py','')
trajectory_config_file = open('{}trajectory_config.yaml'.format(trajectory_package_path),encoding='UTF-8')
trajectory_config_yaml = yaml.load(trajectory_config_file,Loader=yaml.FullLoader)
print(trajectory_config_yaml)



a = 'aa'
print(a.upper())

SAVE_ATTR = trajectory_config_yaml['SAVE_ATTR']#['filename','lineno','module','msg']
LOGLEVEL_ALLOWED = trajectory_config_yaml['LOGLEVEL_ALLOWED']#['INFO','ERROR','DEBUG']#,'WARNING']
print("~~~~~~~~~~")
print(SAVE_ATTR,LOGLEVEL_ALLOWED)



class MongoHandler(logging.Handler):

    def __init__(self,name):

        super(MongoHandler,self).__init__()

        self.name = name
        self.age = 100
        ### 实例化自定义的日志过滤器并加入到处理器中
        filter = MongoLogFilter(name='mongo_log_filter')
        self.addFilter(filter)
        ### 实例化自定义的日志格式化对象
        json_format = JsonFormatter()
        self.setFormatter(json_format)
        

    def emit(self,record):
        
        print('------------')
        # print(record.__dict__)
        value = self.format(record)
        # value = json.dumps(value, ensure_ascii=False).encode("utf-8")
        print(type(value))
        print(value)



class JsonFormatter(logging.Formatter):


    def format(self,record):

        msg = self.translate(record)
        self.set_format_time(msg)

        return msg


    @staticmethod
    def translate(record):
        json_dict = {}
        for attr_name in record.__dict__:
            if attr_name in SAVE_ATTR:
                json_dict[attr_name] = record.__dict__[attr_name]

        return json_dict


    @staticmethod
    def set_format_time(msg):
        ### 获取当前时间
        nowtime = datetime.datetime.now()
        ### 将时间转为字符串后存入日志信息中
        msg['time'] = nowtime.strftime("%Y-%m-%d %H:%M:%S" + ".%03d" % (nowtime.microsecond / 1000))



class MongoLogFilter(logging.Filter):

    def __init__(self,name):
        super(MongoLogFilter,self).__init__()
        self.name = name

    def filter(self,record):
        if record.__dict__['levelname'] in LOGLEVEL_ALLOWED:
            return True
        else:
            return False



### 创建日志操作对象
logger = logging.getLogger()
### 设置日志操作对象的日志等级
logger.setLevel(logging.INFO)
### 创建一个mongodb处理器
mongohandler = MongoHandler(name='mongohandler')
### 设置mongodb处理器的日志等级
mongohandler.setLevel(logging.INFO)
### 向日志操作对象添加mongodb处理器
logger.addHandler(mongohandler)
logger.info('start test log handler')
logger.warning('this is a warning log')



# class MongoManager(object):
#     '''
#     类介绍：

#         这是一个MongoDB数据库连接管理类
#     '''


#     def __init__(self,host,port,username,password,database,collection):
#         '''
#         属性功能：

#             定义一个汇总数据库基本信息的属性方法

#         参数:
#             host (str): mongodb的ip地址
#             port (int): mongodb的端口
#             username (str): mongodb的用户名
#             password (str): mongodb的密码
#             database (str): 数据库名称
#             collection (str): 集合名称
#             client (object): mongodb客户端对象

#         返回：
#             无
#         '''

#         self.host = host
#         self.port = port 
#         self.username = username
#         self.password = password
#         self.database = database
#         self.collection = collection
#         self.client = self.create_mongodb_client()


#     def create_mongodb_client(self):
#         '''
#         方法功能：

#             定义一个连接mongodb的方法，从MongoManager实例参数中获取方法

#         参数：
#             无

#         返回：
#             mongodb_collection (object): mongodb客户端对象-mongodb集合
#         '''

#         mongodb_client = pymongo.MongoClient(host=self.host,port=self.port,username=self.username,password=self.password)
#         mongodb_database = mongodb_client[self.database]
#         database_list = mongodb_client.list_database_names()
#         if self.database not in database_list: ### 执行数据库操作前，需要判断数据库是否存在
#             mongodb_database.create_collection(self.collection)
#         mongodb_collection = mongodb_database[self.collection]
#         print('=============================>>>>>> fiche info {} create well done!'.format(self.collection))

#         return mongodb_collection


#     def insert_info(self,info_dict_list):
#         '''
#         方法功能：

#             定义一个插入信息json串的方法

#         参数：
#             info_dict_list (list): 信息字典列表 

#         返回：
#             result (str): 插入成功信息
#         '''

#         self.client.insert_many(info_dict_list)
#         result = "=============>>>>>> fiche info insert well done!"
#         print(result)

#         return result


#     def update_info(self,query,update):
#         '''
#         方法功能：

#             定义一个更新信息json串的方法

#         参数：
#             query (dict): mongodb查询字典
#             update (dict): mongodb更新字典 

#         返回：
#             result (str): 更新成功信息
#         '''

#         self.client.update_many(query,update) 
#         result = "=============>>>>>> fiche info update well done!"
#         print(result)

#         return result


#     def query_info(self,query,view_index = 0):
#         '''
#         方法功能：

#             定义一个查询信息json串的方法

#         参数：
#             query (dict): mongodb查询字典 

#         返回：
#             result_iter (object): 查询结果
#         '''

#         result_iter = self.client.find(query,projection={'_id': False})### 使用保护机制引入{'_id':false})来去除id额外索引
#         result = "=============>>>>>> fiche info query well done!"
#         print(result)

#         return result_iter[view_index]       


#     def delete_info(self,query):
#         '''
#         方法功能：

#             定义一个删除信息json串的方法

#         参数：
#             query (dict): mongodb查询字典 

#         返回：
#             result (str): 删除成功信息
#         '''

#         self.client.delete_many(query)
#         result = "=============>>>>>> fiche info delete well done!"
#         print(result)

#         return result  




# # mongomanager = MongoManager(host='192.168.1.36',port=27017,username='admin',password='123456',database='test',collection='aabbcc')
# # tmp_data_dict = {'a':100,'b':'bbbb','c':'ccccccccc'}
# # tmp_insert_list = [tmp_data_dict]
# # mongomanager.insert_info(tmp_insert_list)


