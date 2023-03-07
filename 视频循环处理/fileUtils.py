


import json
import os
import time
def save(resContent,path,type='w',encoding='utf-8'):
    if 'b' in type:
        with open(path,type) as fp:
            fp.write(resContent)
    elif 'json' in type:
        with open(path,'w',encoding=encoding) as fp:
            json.dump(resContent,fp,ensure_ascii=False)
    else:
        with open(path,type,encoding=encoding) as fp:
            fp.write(resContent)

def parsePath(basedir,name:str,type='bytes'):
    if name=='':
        if type=='bytes':
            name='temp{}'.format(time.time()).replace('.','')
        elif type=='json':
            name='temp.json'
        else:
            name='temp.txt'
    
    return '{}/{}'.format(basedir,name)

def parseDir(basedir,op=True):
    existsBool=os.path.exists(basedir)
    if existsBool:
        return True
    else:
        if op:
            print(existsBool)
            os.makedirs(basedir)
        return False

def readFile(path,type='r',encoding='utf-8'):
    if 'b' in type:
        with open(path,type) as fp:
            return fp.read()
    elif 'json' in type:
        with open(path,'r',encoding=encoding) as fp:
            return json.loads(fp.read())
    else:
        with open(path,type,encoding=encoding) as fp:
            return fp.read()
    
    