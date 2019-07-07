import numpy as np
import json
import database as db
from collections import namedtuple
from ast import literal_eval as make_tuple


def _json_object_hook(d): return namedtuple('X', d.keys())(*d.values())
def json2obj(str_data): return json.loads(str_data, object_hook=_json_object_hook)


def get_variable(ws_name, var_name):
    v = db.load_variable_meta_json(ws_name, var_name)
    #print v[2]
    meta = json2obj(str(v[2]))
    return Variable(ws_name, var_name, meta)


def get_all_variables(**args):
    ws_name = args['workspace']
    #print ws_name
    v_data = db.load_variables_in_workspace(ws_name)

    return [Variable(v[0], v[1], json2obj(str(v[2]))) for v in v_data]


class Workspace:
    def __init__(self, ws_name):
        res = db.load_workspace_meta_json(ws_name)
        self.meta_ = json2obj(str(res[2]))

        var_list = get_all_variables(workspace=ws_name)

        for var in var_list:
            self.__dict__[var.meta_.name] = var.value()

    def name(self):
        return self.meta_.name


    def get_variable(self, var_name):
        return self.__dict__[var_name]

    # def variables(self):
    #     def parse_variable(key):
    #         k = key[0].split('.')
    #         return Variable(k[0], k[1])
    #
    #     return [parse_variable(v[0]) for v in db.load_variables_in_workspace(self.name())]


class Variable:
    def __init__(self, ws_name, var_name, meta):
        self.meta_ = meta
        #json2obj(db.load_variable_meta_json(ws_name, var_name))

    def type(self):
        return self.meta_.type

    # lazy load : double or string or npz binary
    # data = np.genfromtxt(s, dtype=[('myint','i8'),('myfloat','f8'),
    # ... ('mystring','S5')], delimiter=",")
    def value(self):
        #res = db.load_variable_value(self.meta_.workspace, self.meta_.key)
        res = db.load_variable_value(self.meta_.key)

        if self.meta_.type == 0 or self.meta_.type == 'default':
            #sss =
            lines = str.splitlines(str(res[2]))
            return np.array([str.split(line,',') for line in lines], np.str)
            #return np.fromstring(sss, dtype=np.str, sep='\n')
            #return np.genfromtxt(sss, dtype=np.str, delimiter=",")
        elif self.meta_.type == 2 or self.meta_.type == 'matrix':
            shape = make_tuple(self.meta_.shape)
            buffer = res[2]
            row = shape[0]
            col = shape[1]

            # matrix = np.ndarray((shape[0],shape[1]))
            d = np.frombuffer(buffer, dtype=np.double, count=row*col, offset=0)
            d.shape = shape
            #d= [ np.frombuffer(buffer , dtype=np.double, count=col, offset=r) for r in range(row)]
            #d = np.frombuffer(buffer , dtype=np.double, count=5, offset=0)
            return d
        else:
            return 'not supported type : ' + str(self.meta_.type)

        # if self.meta_.type == 'default' or self.meta_.var_type == 'cell' :
        #     return np.genfromtxt(StringIO(res),delimiter=",")
        # elif self.meta_.var_type == 'double':
        #     return np.genfromtxt(StringIO(res),delimiter=",")
        # else:
        #     return 'load fail'


class DefaultVariable(Variable):
    def __init__(self):
        Variable.__init__(self)

    def value(self):
        pass