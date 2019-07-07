import sqlite3
import win32com.client
import winpaths
import json
import os, io

conn = None
applicationName = 'mydata'
settings = None


def initialize(appname):
    global settings
    with open(os.path.join(winpaths.get_appdata(), 'Montrix', 'MxExcelAddIn', 'settings', 'settings.json')) as f:
        settings = json.load(f)

    db_filie = os.path.join(settings['GeneralOptionCategory_']['RepositoryDirectory_'], appname, 'BlobCache', 'userblobs.db')
    #db_filie = os.path.join('C:\\Users\\09928829\\Downloads\\userblobs.db')
    #db_filie = os.path.join('userblobs.db')

    print db_filie + ' load success!'

    global conn
    conn = sqlite3.connect(db_filie)


def load_workspace_meta_json(ws_name):
    #res  = b'{"name": "John Smith", "hometown": {"name": "New York", "id": 123}}'

    #sql = "SELECT Key, TypeName, Value FROM CacheElement WHERE TypeName='MxExcelAddInUI.WorkspaceKeyManager+WorkSapce' and KEY=:key"
    sql = "SELECT Key, TypeName, Value FROM CacheElement WHERE KEY=:key and TypeName=:type_name"
    param = { 'key':  ws_name, 'type_name' : 'ws_metadata'}
    cursor = conn.cursor()
    cursor.execute(sql, param)
    ws_meta = cursor.fetchone()

    return ws_meta


def load_variables_in_workspace(ws_name):
    sql = "SELECT Key, TypeName, Value FROM CacheElement WHERE TypeName=:type_name"
    param = {'type_name': 'metadata'}
    cursor = conn.cursor()
    cursor.execute(sql, param)
    #name, ws_meta = cursor.fetchone()
    return [v for v in cursor.fetchall() ]


def load_variable_meta_json(ws_name, var_name):
    sql = "SELECT Key, TypeName, Value FROM CacheElement WHERE KEY=:key and TypeName=:type_name"
    param = {'key':  ws_name + '.' + var_name, 'type_name' : 'metadata'}
    cursor = conn.cursor()
    cursor.execute(sql, param)
    meta = cursor.fetchone()

    # print 'meta : ' + str(meta)
    return meta
    #return value.encode("utf-8")


# http://www.numericalexpert.com/blog/sqlite_blob_time/
#def load_variable_value(ws_name, var_name):
def load_variable_value(var_key):
    #sql = "SELECT Key, TypeName, Value FROM CacheElement WHERE KEY=:key and TypeName='valuedata'"
    sql = "SELECT Key, TypeName, Value FROM CacheElement WHERE KEY=:key"
    #param = { 'key':  "#" + ws_name + '.' + var_name }
    param = {'key': "#" + var_key}
    cursor = conn.cursor()
    cursor.execute(sql, param)
    value  = cursor.fetchone()

    # print 'value : ' + str(bson.loads(value[2]))
    # decoded_doc =  io.BytesIO(value[2])

    return value
    #return va.encode("utf-8")


# initialize('mytest')
# load_variable_meta_json('ws', 'newVar')
# load_variable_value('ws', 'newVar')
# load_workspace_meta_json()