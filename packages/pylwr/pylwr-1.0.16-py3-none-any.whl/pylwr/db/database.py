
import datetime
import json
import oracledb
import pymysql
from pylwr.const import *
import pylwr

class Db(object):
    def __init__(self,db_name: int, ) -> object:
        if db_name == DB_HCU:
            self.oracle_init('192.168.1.141','1521','orcl','drg','1')
            self.db_type = DRIVE_ORACLE
        if db_name == DB_SH:
            self.oracle_init_less12('192.168.6.147','1521','orcl','drg','1', PATH_LWR_ROG)
            self.db_type = DRIVE_ORACLE
        if db_name == DB_LICUS:
            self.mysql_init('192.168.6.147','micm_szlg_lhkf','root','root')
            self.db_type = DRIVE_MYSQL
        

    def mysql_init(self,host: str, database: str, user: str, password: str, ) -> object:
        self.connection = pymysql.connect(
            host = host,
            database = database,
            user = user,
            password = password,
        )
    def oracle_init(self,host: str, port: int, service_name: str, user: str, password: str, ) -> object:
        dsn = oracledb.makedsn(host, port, service_name)
        self.connection = oracledb.connect(
            dsn = dsn,
            user = user,
            password = password,
        )
        self.cursor = self.connection.cursor()
    def oracle_init_less12(self,host: str, port: int, service_name: str, user: str, password: str, env: int) -> object:
        if env == PATH_LWR_ROG:
            d = r"C:\tool\instantclient_12_2"
            oracledb.init_oracle_client(lib_dir=d)
        dsn = oracledb.makedsn(host, port, service_name)
        self.connection = oracledb.connect(
            dsn = dsn,
            user = user,
            password = password,
        )
        self.cursor = self.connection.cursor()
    def select(self, sql):
        list = []
        self.cursor.execute(sql)
        result = self.cursor.fetchall()
        col_name = self.cursor.description
        for row in result:
            dict = {}
            for col in range(len(col_name)):
                key = col_name[col][0]
                value = row[col]
                if isinstance(value,datetime.datetime):
                    dict[key] = value.strftime("%Y-%m-%d %H:%M:%S")
                else:
                    dict[key] = value
                
            list.append(dict)
        return json.dumps(list, ensure_ascii=False, indent=2, separators=(',', ':'))
    
    def select_json(self, sql):
        list = []
        self.cursor.execute(sql)
        result = self.cursor.fetchall()
        col_name = self.cursor.description
        for row in result:
            dict = {}
            for col in range(len(col_name)):
                key = col_name[col][0]
                value = row[col]
                if isinstance(value,datetime.datetime):
                    dict[key] = value.strftime("%Y-%m-%d %H:%M:%S")
                else:
                    dict[key] = value
                
            list.append(dict)
        return list

    def execute(self, sql, data= None):
        if self.db_type == DRIVE_MYSQL:
            try:
                if data is None:
                    self.cursor.execute(sql)
                else:
                    self.cursor.execute(sql,data)
                self.connection.commit()
            except pymysql.Error as e:
                error_obj, = e.args
                raise Exception(
                    sql + 
                    ' ' + 
                    '\n' 
                    + str(error_obj.code) + 
                    ' ' + str(error_obj.message))
        if self.db_type == DRIVE_ORACLE:
            try:
                if data is None:
                    self.cursor.execute(sql)
                else:
                    self.cursor.execute(sql,data)
                self.connection.commit()
            except oracledb.Error as e:
                error_obj, = e.args
                raise Exception(
                    sql + 
                    ' ' + 
                    '\n' 
                    + str(error_obj.code) + 
                    ' ' + str(error_obj.message))
    
    def select_some_param(self, table: str, obj: object, func: str, input: str, type: int, update: str, print_debug: bool )-> list|None:
        '''
        通过表的json对象循环, 判断符合某种条件, 将所有符合条件的字段拼接成或连接的条件,然后执行语句
        :param: table 表名
        :type table: str

        :param: obj 表数据类型, 如{"A": "NOW IS ABC","B": 1}
        :type obj: object

        :param: func 调用方法名字, 调用方法默认返回bool
        :type func: str

        :param: input 最终查询语句条件内容,默认字符串
        :type input: str

        :param: table 想要执行SQL的类型, 有SELECT/DELETE/UPDATE三种
        :type table: int

        :param: update UPDATE的修改内容,直接写SQL语句片段, 参考: A=1,B=2,C=3
        :type update: str

        :param: print_debug 是否打印DEBUG日志
        :type print_debug: bool

        :rtype: list|None
        '''
        sql = ''
        NOT_ZERO = False
        for key, value in obj.items():
            # 默认入参是字符串
            
            if pylwr.distribute.target_fun(func, value):
                if NOT_ZERO:
                    sql = sql + ' OR '+ key + '=\'' + input + '\''
                else:
                    sql = sql + key + '=\'' + input + '\''
                    NOT_ZERO =True
        if not NOT_ZERO:
            pylwr.warning('Now, the table ['+table+'] not match rule <'+func+'>, program will be skip.')
            return
        if type == SQL_DELETE:
            sql = 'DELETE FROM ' + table + ' WHERE ' + sql
            if print_debug:
                print(sql)
            return self.execute(sql)
        if type == SQL_SELECT:
            sql = 'SELECT * FROM ' + table + ' WHERE ' + sql
            if print_debug:
                print(sql)
            return self.select_json(sql)
        if type == SQL_UPDATE:
            sql = 'UPDATE ' + table + ' SET ' + update + ' WHERE ' + sql
            if print_debug:
                print(sql)
            return self.execute(sql)
        return

        
        

    def check(self):
        try:
            self.connection.ping()
        except:
            self.connection()

    def close(self):
        self.connection.close()