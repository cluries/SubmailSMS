import json
import time
import hashlib
import requests


class SubmailSMS(object):
    APIURL = 'https://api.submail.cn/message/xsend.json'

    def __init__(self, appid, appkey, projectid):
        super(SubmailSMS, self).__init__()
        self.appid = appid
        self.appkey = appkey
        self.projectid = projectid
        self.to = list()
        self.vars = dict()

    def addto(self, mobile):
        if isinstance(mobile, list) or isinstance(mobile, tuple):
            for m in mobile:
                self.to.append(m)
        else:
            self.to.append(mobile)

    def setvar(self, key, value):
        self.vars[key] = value

    def signature(self, params):
        sortedkeys = sorted(params.keys())
        payload = self.appid + self.appkey
        payload += '&'.join(["%s=%s" % (key, params[key]) for key in sortedkeys])
        payload += self.appid + self.appkey
        h = hashlib.md5()
        h.update(payload.encode('utf-8'))
        return h.hexdigest()

    def requests(self):
        req = dict()
        req['appid'] = self.appid
        req['sign_type'] = 'md5'
        req['project'] = self.projectid
        req['to'] = ','.join(self.to)
        req['vars'] = json.dumps(self.vars)
        req['timestamp'] = int(time.time())
        req['signature'] = self.signature(req)
        return req

    def send(self):
        res = requests.post(SubmailSMS.APIURL, json=self.requests())
        if 200 <= res.status_code < 300:
            return res.json()
        return None
