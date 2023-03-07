



import ffmpy3
import os

def printData(data):
    if isinstance(data,dict):
        data=list(data.values())
    if isinstance(data,list):
        data=data[:1000]
    print(data)


def deSizes(bigDir='/data',smallDir='/smallData'):
    fileNameList=os.listdir(bigDir)
    for i,fileName in enumerate(fileNameList):
        print(i)
        bigPath='{}/{}'.format(bigDir,fileName)
        smallPath='{}/{}'.format(smallDir,fileName)
        ffmpy3.FFmpeg(inputs={bigPath: None}, outputs={smallPath:None}).run()
        i+=1

def deSize(bigPath='/data',smallPath='/smallData',threadsNum=10):
    ffmpy3.FFmpeg(inputs={bigPath: None}, outputs={smallPath:'-threads {} -preset ultrafast'.format(threadsNum)}).run()

# basedir='E:/我的/王的工作文件夹/学习作品/其舒/python爬取练习/工具/视频循环处理'
# # basedir=''
# deSize(basedir+'/data/概念1.8 矩阵的逆.mp4',basedir+'/smallData/概念1.8 矩阵的逆.mp4')
# ffmpy3.FFmpeg(inputs={'/data/概念1.8 矩阵的逆.mp4': None}, outputs={'/smallData/概念1.8 矩阵的逆.mp4':'-threads 5 -preset ultrafast'}).run()
