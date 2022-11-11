# -*- coding: utf-8 -*-
# author:shihua
# coder:shihua
# 这是一个日志处理器类，包括各种转发后端的处理器
"""
模块介绍
-------

这是一个日志处理器类，包括各种转发后端的处理器

设计模式：

    （1）  无 

关键点：    

    （1）日志转发处理

主要功能：            

    （1）提供各种转发后端的处理器                                

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
import trajectory




####### 日志处理器类 ########################################################
### 设计模式：                                                           ###
### （1）无                                                              ###
### 关键点：                                                             ###
### （1）日志转发处理                                                     ###
### 主要功能：                                                           ###
### （1）提供各种转发后端的处理器                                          ###
############################################################################


####### 日志处理器类 ####################################################################################
########################################################################################################



### mongo日志转发处理器
class MongoHandler(logging.Handler):
    '''
    类介绍：

        这是一个mongo日志转发处理器类，主要功能提供mongo日志转发功能，主要技术pymongo和方法重写。
    '''


    def __init__(self,log_database,log_collection,remark = 'no remark'):
        '''
        属性功能：

            定义一个初始化mongo转发处理器的方法

        参数：
            remark (str): 备注
            filter (object): 这是一个日志过滤器实例属性
            json_format (object): 这是一个json格式化实例属性
            log_database (str): 日志数据库
            log_collection (str): 日志集合
        '''
        
        super(MongoHandler,self).__init__()
        self.log_database = log_database
        self.log_collection = log_collection
        self.remark = remark
        ### 实例化自定义的日志过滤器并加入到处理器中
        filter = trajectory.MongoLogFilter()
        self.addFilter(filter)
        ### 实例化自定义的日志格式化对象
        json_format = trajectory.JsonFormatter()
        self.setFormatter(json_format)
        

    def emit(self,record):
        '''
        方法功能：

            重写一个处理日志的方法

        参数：
            record (object): logging的日志记录对象

        返回：
            无
        '''
        
        ### 配置mongo日志记录collection
        mongolog_dict = trajectory.MONGO_CONFIG
        mongolog_dict['database'] = self.log_database
        mongolog_dict['collection'] = self.log_collection
        ### 加载mongodb连接器
        mongomanager = trajectory.MongoManager(**mongolog_dict)
        ### 开始处理日志记录，转为mongo接受的字典格式
        value = self.format(record)
        # value = json.dumps(value, ensure_ascii=False).encode("utf-8")
        ### 插入到mongodb中
        tmp_insert_list = [value]
        mongomanager.insert_info(tmp_insert_list)
        print('====================>>>>>> Log to mongodb well done!')



#############################################################################################################
#############################################################################################################


