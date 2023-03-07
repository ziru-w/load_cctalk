




import json
import random
from time import sleep
import time
import requests
import ffmpy3
import os



def deSize(bigDir='/data',smallDir='/smallData'):
    fileNameList=os.listdir(bigDir)
    for i,fileName in enumerate(fileNameList):
        print(i)
        bigPath='{}/{}'.format(bigDir,fileName)
        smallPath='{}/{}'.format(smallDir,fileName)
        ffmpy3.FFmpeg(inputs={bigPath: None}, outputs={smallPath:None}).run()
        i+=1

def buildVideoDetailUrl(videoId):
    return 'https://www.cctalk.com/webapi/content/v1.1/video/detail?videoId={}'.format(videoId)

def getVideoInfoList(videoInfoListUrl,headers,op=True):
    response = requests.get(videoInfoListUrl, headers=headers)
    res=response.json()
    videoInfoList=res['data']['items']
    if op:
        with open(infoDir+'/videoList.json','w',encoding='utf-8') as fp:
            json.dump(videoInfoList,fp,ensure_ascii=False)
    return videoInfoList

def getVideoIdDict(videoInfoList,op=True):
    videoIdDict={}
    for temp in videoInfoList:
        if videoIdDict.get(temp['unitName'])==None:
            videoIdDict[temp['unitName']]={}
        videoIdDict[temp['unitName']][temp['videoInfo']['videoName']]=temp['videoInfo']['videoId']
        # ['videoInfo'](['videoName']['videoId']['materialId'])
    
    if op:
        with open(infoDir+'/videoIdDict.json','w',encoding='utf-8') as fp:
            json.dump(videoIdDict,fp,ensure_ascii=False)
    return videoIdDict

def getVideoUrl(videoDetailUrl,headers):
    # videoDetailUrl=buildVideoDetailUrl(videoId)
    print(videoDetailUrl)
    response = requests.get(videoDetailUrl, headers=headers)
    print(response)
    # headers['Referer']='https://www.cctalk.com/v/16460167394909'
    res=response.json()
    videoUrl=res['data']['videoUrl']
    
    return videoUrl
def getVideoUrlDict(videoIdDict:dict,headers,op=True):
    videoUrlDict={}
    for unitVideoKeys in videoIdDict.keys():
        if videoUrlDict.get(unitVideoKeys)==None:
            videoUrlDict[unitVideoKeys]={}
        unitVideoValues=videoIdDict[unitVideoKeys]
        for videoName in unitVideoValues.keys():
            videoId=unitVideoValues[videoName]
            videoUrlDict[unitVideoKeys][videoName]=getVideoUrl(buildVideoDetailUrl(videoId),headers)
            
    if op:
        with open(infoDir+'/videoUrlDict.json','w',encoding='utf-8') as fp:
            json.dump(videoUrlDict,fp,ensure_ascii=False)
    return videoUrlDict

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

def getResponse(videoUrl,headers,encoding='bytes'):
    if encoding=='bytes':
        response = requests.get(videoUrl, headers=headers)
        return response.content
    else:
        response = requests.get(videoUrl, headers=headers)
        return response.content.decode(encoding=encoding)

def parsePath(basedir,name:str,type='bytes'):
    if name=='':
        if type=='bytes':
            name='temp{}'.format(time.time()).replace('.','')
        elif type=='json':
            name='temp.json'
        else:
            name='temp.txt'
    
    return '{}/{}'.format(basedir,name)


def load(videoUrl,headers,name='',type='wb'):
    resContent=getResponse(videoUrl,headers)
    path=parsePath(dataDir,name)
    save(resContent,path,type)

def loads(videoUrlDict,headers,sleepTime=1,exp='.mp4'):
    for unitVideoKeys in videoUrlDict.keys():
        print(unitVideoKeys)
        unitVideoValues=videoUrlDict[unitVideoKeys]
        for videoName in unitVideoValues.keys():
            print(videoName)
            videoUrl=unitVideoValues[videoName]
            load(videoUrl,headers,videoName+exp)
            sleep(sleepTime+random.randint(0,5))
    return videoUrlDict

def printData(data):
    if isinstance(data,dict):
        data=list(data.values())
    if isinstance(data,list):
        data=data[:1000]
    print(data)

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
headers={
    "Host": "www.cctalk.com",
    "Referer": "https://www.cctalk.com/",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:102.0) Gecko/20100101 Firefox/102.0"
}

def parseDir(basedir,op=True):
    existsBool=os.path.exists(basedir)
    if existsBool:
        return True
    else:
        if op:
            print(existsBool)
            os.makedirs(basedir)
        return False
def main(sleepTime=1):
    videoInfoList=getVideoInfoList(videoInfoListUrl,headers)
    videoIdDict=getVideoIdDict(videoInfoList)
    videoUrlDict=getVideoUrlDict(videoIdDict,headers)
    printData(videoUrlDict)
    loads(videoUrlDict, headers,sleepTime)
    deSize()
videoInfoListUrl='https://www.cctalk.com/webapi/content/v1.2/series/all_lesson_list?_timestamp=1657872199847&seriesId=1645960105478200&showStudyTime=true'
infoDir=os.path.dirname(__file__)+'/info'
dataDir=os.path.dirname(__file__)+'/data'
smallDir=os.path.dirname(__file__)+'/smallData'

parseDir(infoDir)
parseDir(dataDir)
parseDir(smallDir)

if __name__ == '__main__':
    main()
    # getVideoUrl('https://www.cctalk.com/webapi/content/v1.1/video/detail?videoId=16460167394909',headers)
    # deSize()
    