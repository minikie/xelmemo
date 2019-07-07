import database as db
import variables as vr

db.initialize('mytest')

# usage
ws_name1 = 'ws'

print('variable load..............')
variable = vr.get_variable('ws', 'newVar')
print(variable)

print('variable value data load..............')
print variable.value()

print('')
print('---------------------------------')
print('')

print('all variable load..............')
variables  = vr.get_all_variables(workspace='ws')
print(variables)

for v in variables:
    print v.value()

#repo.get_variable('ws', 'newVar')

#print( variabless)
