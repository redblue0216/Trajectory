# -*- coding: utf-8 -*-
# author:shihua
# coder:shihua
# 这是一个基础工具集合类
"""
模块介绍
-------

这是一个基础工具集合类

设计模式：

    （1）  无 

关键点：    

    （1）基础依赖

主要功能：            

    （1）基础操作工具集合                                

使用示例
-------


类说明
------

"""



####### 载入程序包 ##########################################################
############################################################################



import logging
import datetime
import json
import pymongo 
import yaml
import trajectory as tjtr




####### 基础工具集合类 ######################################################
### 设计模式：                                                           ###
### （1）无                                                              ###
### 关键点：                                                             ###
### （1）基础依赖                                                        ###
### 主要功能：                                                           ###
### （1）基础操作工具集合                                                 ###
############################################################################


####### 基础工具集合 ####################################################################################
########################################################################################################



### 暴露指定的公开接口
__all__ = ['SAVE_ATTR','LOGLEVEL_ALLOWED','MONGO_CONFIG','MongoLogFilter','JsonFormatter','MongoManager']



### 基础参数配置-使用yaml保存配置
trajectory_package_path = tjtr.__file__.replace('__init__.py','')
trajectory_config_file = open('{}trajectory_config.yaml'.format(trajectory_package_path),encoding='UTF-8')
trajectory_config_yaml = yaml.load(trajectory_config_file,Loader=yaml.FullLoader)
### 获取输出参数和日志允许等级
SAVE_ATTR = trajectory_config_yaml['SAVE_ATTR']
LOGLEVEL_ALLOWED = trajectory_config_yaml['LOGLEVEL_ALLOWED']
MONGO_CONFIG = trajectory_config_yaml['MONGO_CONFIG']



### Mongo日志等级过滤器类
class MongoLogFilter(logging.Filter):
    '''
    类介绍：

        这是一个针对mongo的日志过滤器类，主要功能提供日志过滤功能，主要技术方法重写。
    '''


    def __init__(self,remark='no remark'):
        '''
        属性功能：

            定义一个初始化mongo日志等级过滤器的初始化方法
        
        参数：
            remark (str): 备注
        '''

        super(MongoLogFilter,self).__init__()
        self.remark = remark


    def filter(self,record):
        '''
        方法功能：

            重写一个过滤方法

        参数：
            record (object): logging日志记录对象

        返回：
            bool (bool): 是否过滤判断
        '''

        if record.__dict__['levelname'] in LOGLEVEL_ALLOWED:
            return True
        else:
            return False



### JSON格式化类             
class JsonFormatter(logging.Formatter):
    '''
    类介绍：

        这是一个JSON格式化类，主要功能提供json格式化日志功能，主要技术方法重写
    '''


    def format(self,record):
        '''
        方法功能：

            重写一个格式化方法

        参数：
            record (object): logging日志记录对象

        返回：
            msg (dict): 日志字典
        '''

        msg = self.translate(record)
        self.set_format_time(msg)

        return msg


    @staticmethod
    def translate(record):
        '''
        方法功能：

            定义一个转化日志记录为json的静态方法

        参数：
            record (object): logging日志记录对象

        返回：
            json_dict (dict): json日志字典
        '''

        json_dict = {}
        for attr_name in record.__dict__:
            if attr_name in SAVE_ATTR:
                json_dict[attr_name] = record.__dict__[attr_name]

        return json_dict


    @staticmethod
    def set_format_time(msg):
        '''
        方法功能：

            定义一个设置格式化时间的静态方法

        参数：
            msg (dict): json日志字典

        返回：
            无
        '''

        ### 获取当前时间
        nowtime = datetime.datetime.now()
        ### 将时间转为字符串后存入日志信息中
        msg['time'] = nowtime.strftime("%Y-%m-%d %H:%M:%S" + ".%03d" % (nowtime.microsecond / 1000))



### Mongo管理类
class MongoManager(object):
    '''
    类介绍：

        这是一个MongoDB数据库连接管理类
    '''


    def __init__(self,host,port,username,password,database,collection):
        '''
        属性功能：

            定义一个汇总数据库基本信息的属性方法

        参数:
            host (str): mongodb的ip地址
            port (int): mongodb的端口
            username (str): mongodb的用户名
            password (str): mongodb的密码
            database (str): 数据库名称
            collection (str): 集合名称
            client (object): mongodb客户端对象

        返回：
            无
        '''

        self.host = host
        self.port = port 
        self.username = username
        self.password = password
        self.database = database
        self.collection = collection
        self.client = self.create_mongodb_client()


    def create_mongodb_client(self):
        '''
        方法功能：

            定义一个连接mongodb的方法，从MongoManager实例参数中获取方法

        参数：
            无

        返回：
            mongodb_collection (object): mongodb客户端对象-mongodb集合
        '''

        mongodb_client = pymongo.MongoClient(host=self.host,port=self.port,username=self.username,password=self.password)
        mongodb_database = mongodb_client[self.database]
        database_list = mongodb_client.list_database_names()
        if self.database not in database_list: ### 执行数据库操作前，需要判断数据库是否存在
            mongodb_database.create_collection(self.collection)
        mongodb_collection = mongodb_database[self.collection]
        print('=============================>>>>>> fiche info {} create well done!'.format(self.collection))

        return mongodb_collection


    def insert_info(self,info_dict_list):
        '''
        方法功能：

            定义一个插入信息json串的方法

        参数：
            info_dict_list (list): 信息字典列表 

        返回：
            result (str): 插入成功信息
        '''

        self.client.insert_many(info_dict_list)
        result = "=============>>>>>> fiche info insert well done!"
        print(result)

        return result


    def update_info(self,query,update):
        '''
        方法功能：

            定义一个更新信息json串的方法

        参数：
            query (dict): mongodb查询字典
            update (dict): mongodb更新字典 

        返回：
            result (str): 更新成功信息
        '''

        self.client.update_many(query,update) 
        result = "=============>>>>>> fiche info update well done!"
        print(result)

        return result


    def query_info(self,query,view_index = 0):
        '''
        方法功能：

            定义一个查询信息json串的方法

        参数：
            query (dict): mongodb查询字典 

        返回：
            result_iter (object): 查询结果
        '''

        result_iter = self.client.find(query,projection={'_id': False})### 使用保护机制引入{'_id':false})来去除id额外索引
        result = "=============>>>>>> fiche info query well done!"
        print(result)

        return result_iter[view_index]       


    def delete_info(self,query):
        '''
        方法功能：

            定义一个删除信息json串的方法

        参数：
            query (dict): mongodb查询字典 

        返回：
            result (str): 删除成功信息
        '''

        self.client.delete_many(query)
        result = "=============>>>>>> fiche info delete well done!"
        print(result)

        return result 



####################################################################################################################################
####################################################################################################################################


