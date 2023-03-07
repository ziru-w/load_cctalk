






import os
try:
    from .apiUtils import getVideoIdDict, getVideoInfoList, getVideoUrlDict, loads,init
    from .dataParseUtils import deSize,deSizes
    from .config import infoDir,dataDir,smallDir,headers,baseVideoDetailUrl,videoInfoListUrl
    from .fileUtils import readFile
except ImportError as res:
    # print("ImportError",res)
    from apiUtils import getVideoIdDict, getVideoInfoList, getVideoUrlDict, loads,init
    from dataParseUtils import deSize,deSizes
    from config import infoDir,dataDir,smallDir,headers,baseVideoDetailUrl,videoInfoListUrl
    from fileUtils import readFile

# headers={
#     "Host": "www.cctalk.com",
#     "Referer": "https://www.cctalk.com",
#     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:102.0) Gecko/20100101 Firefox/102.0"
# }
# videoInfoListUrl='https://www.cctalk.com/webapi/content/v1.2/series/all_lesson_list?_timestamp=1657872199847&seriesId=1645960105478200&showStudyTime=true'
# infoDir=os.path.dirname(__file__)+'/info'
# dataDir=os.path.dirname(__file__)+'/data'
# smallDir=os.path.dirname(__file__)+'/smallData'

def main(sleepTime=1):
    init(infoDir,dataDir,smallDir,headers,baseVideoDetailUrl,videoInfoListUrl)
    print('start')
    videoInfoList=getVideoInfoList(videoInfoListUrl,headers)
    videoIdDict=getVideoIdDict(videoInfoList)
    videoUrlDict=getVideoUrlDict(videoIdDict,headers)
    # videoUrlDict=readFile(infoDir+'/videoUrlDict.json','json')
    loads(videoUrlDict, headers,sleepTime)
    deSizes(dataDir,smallDir)

if __name__ == '__main__':
    main()
    # getVideoUrl('https://www.cctalk.com/webapi/content/v1.1/video/detail?videoId=16460167394909',headers)
    # deSize(dataDir,smallDir)
    # print(1)