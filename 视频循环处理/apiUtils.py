







import json
from time import sleep
import requests
import os
from tqdm import tqdm
import random

try:
    from .fileUtils import parsePath,save,parseDir
    from .config import infoDir,dataDir,smallDir,headers,baseVideoDetailUrl,videoInfoListUrl
except ImportError:
    from fileUtils import parsePath,save,parseDir
    from config import infoDir,dataDir,smallDir,headers,baseVideoDetailUrl,videoInfoListUrl


def init(info,data,small,baseHeaders,baseurl,listurl):
    global infoDir,dataDir,smallDir,headers,baseVideoDetailUrl,videoInfoListUrl
    infoDir=info
    dataDir=data
    smallDir=small
    headers=baseHeaders
    baseVideoDetailUrl=baseurl
    videoInfoListUrl=listurl
    parseDir(infoDir)
    parseDir(dataDir)
    parseDir(smallDir)
def buildVideoDetailUrl(videoId):
    return baseVideoDetailUrl+str(videoId)

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
    for temp in tqdm(videoInfoList,desc='VideoIdDict'):
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
    response = requests.get(videoDetailUrl, headers=headers)
    res=response.json()
    videoUrl=res['data']['videoUrl']
    return videoUrl




def getVideoUrlDict(videoIdDict:dict,headers,op=True):
    videoUrlDict={}
    for unitVideoKeys in tqdm(videoIdDict.keys(),desc='VideoUrlDict'):
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



def getResponse(videoUrl,headers,encoding='bytes'):
    if encoding=='bytes':
        print(videoUrl,headers)
        response = requests.get(videoUrl, headers=headers)
        print(response.status_code)
        return response.content
    else:
        response = requests.get(videoUrl, headers=headers)
        return response.content.decode(encoding=encoding)



def load(videoUrl,headers,name='',type='wb'):
    resContent=getResponse(videoUrl,headers)
    res=requests.get(videoUrl,headers)
    print(res.status_code)
    if res.status_code==502:
        return
    resContent=res.content
    path=parsePath(dataDir,name)
    save(resContent,path,type)

def loads(videoUrlDict,headers,sleepTime=1,exp='.mp4'):
    for unitVideoKeys in videoUrlDict.keys():
        unitVideoValues=videoUrlDict[unitVideoKeys]
        for videoName in tqdm(unitVideoValues.keys(),desc=unitVideoKeys):
            print(videoName)
            videoUrl=unitVideoValues[videoName]
            load(videoUrl,headers,videoName+exp)
            sleep(sleepTime+random.randint(0,5))
    return videoUrlDict

