# -*- coding:utf-8 -*-
import sys
from aliyunsdkmts.request.v20140618 import SearchMediaRequest
from aliyunsdkcore import client
import oss2
import json
import requests
import re
reload(sys)
sys.path.append('../')
from config.conf import alisetting


def search_media():
    clt = client.AcsClient(alisetting['ak'], alisetting['sk'], 'mts-cn-beijing')
    request = SearchMediaRequest.SearchMediaRequest()
    request.set_accept_format('JSON')
    request.set_PageSize(100)
    response = json.loads(clt.do_action_with_exception(request))
    return response

def upload_file(filename, path) :
    auth = oss2.Auth(alisetting['ak'], alisetting['sk'])
    end = alisetting['bucket']
    if filename.endswith('mp4') :
        end = alisetting['vbucket']
    bucket = oss2.Bucket(auth, alisetting['endpoint'], end)
    result = bucket.put_object_from_file(path, filename)
    return result

def upload_all_video() :
    path = '/data/uploads/video/'
    with open(path + 'video.info', 'r') as f :
        for one in f.readlines():
            item, vname, des = tuple(one.split(','))
            vname = vname.strip()
            print vname
            print upload_file(path + vname, 'm3u8MultibitrateIn22/' + vname)

def insert_video2db() :
    medias = search_media()
    name_maps = {}
    path = '/data/uploads/video/'
    with open(path + 'video.info', 'r') as f :
        for one in f.readlines():
            item, vname, des = tuple(one.split(','))
            vname = vname.strip()
            des = re.sub('\n','', des)
            des = des.strip()
            name_maps[vname] = des
    for one in medias['MediaList']['Media'] :
        data = {'name' : one['Title'], 'vid' : one['MediaId'], 'des' : name_maps.get(one['Title'], ''), 'vtype' : item}
        r = requests.post('http://localhost:8082/video/add/', data = json.dumps(data))
        print r.content

def upload_all_img() :
    path = '/data/uploads/img/'
    with open(path + 'img.info', 'r') as f :
        for one in f.readlines():
            item, vname, des = tuple(one.split(','))
            vname = vname.strip()
            print upload_file(path + vname, 'img/' + vname)


def insert_img2db() :
    name_maps = {}
    urlpath = 'http://xindognvyou-file.oss-cn-beijing.aliyuncs.com/img/'
    path = '/data/uploads/img/'
    with open(path + 'img.info', 'r') as f :
        for one in f.readlines():
            item, vname, des = tuple(one.split(','))
            vname = vname.strip()
            des = re.sub('\n','', des)
            des = des.strip()
            name_maps[vname] = des
            data = {'des' : des, 'url' : urlpath + vname, 'itype' : item, 'name' : vname}
            r = requests.post('http://localhost:8082/img/add/', data = json.dumps(data))

def upload_all_audio() :
    path = '/data/uploads/audio/'
    with open(path + 'audio.info', 'r') as f :
        for one in f.readlines():
            vtype, vname, des = tuple(one.split(','))
            vname = vname.strip()
            print upload_file(path + vname, 'audio/' + vname)

def insert_audio2db() :
    name_maps = {}
    urlpath = 'http://xindognvyou-file.oss-cn-beijing.aliyuncs.com/audio/'
    path = '/data/uploads/audio/'
    with open(path + 'audio.info', 'r') as f :
        for one in f.readlines():
            vtype, vname, des = tuple(one.split(','))
            print des
            des = re.sub('\n','', des)
            des = des.strip()
            vname = vname.strip()
            name_maps[vname] = des
            data = {'des' : des, 'url' : urlpath + vname, 'name' : vname, 'atype' : vtype}
            r = requests.post('http://localhost:8082/audio/add/', data = json.dumps(data))
            print r.content

if __name__ == '__main__' :
    #upload_all_video()
    insert_video2db()
    # print json.dumps(search_media(), indent=1)
    #upload_all_img()
    # insert_img2db()
    #upload_all_audio()
    # insert_audio2db()