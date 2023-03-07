import os


headers={
    "Host": "www.cctalk.com",
    "Referer": "https://www.cctalk.com",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:102.0) Gecko/20100101 Firefox/102.0"
}
videoInfoListUrl='https://www.cctalk.com/webapi/content/v1.2/series/all_lesson_list?_timestamp=1657872199847&seriesId=1645960105478200&showStudyTime=true'
baseVideoDetailUrl='https://www.cctalk.com/webapi/content/v1.1/video/detail?videoId='
infoDir=os.path.dirname(__file__)+'/info'
dataDir=os.path.dirname(__file__)+'/data'
smallDir=os.path.dirname(__file__)+'/smallData'