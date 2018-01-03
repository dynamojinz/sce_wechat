# -*- coding: utf-8 -*-

from odoo import models, fields, api

# class sce_sso(models.Model):
#     _name = 'sce_sso.sce_sso'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         self.value2 = float(self.value) / 100
import urllib.request
import json

WECHAT_URL = "https://qyapi.weixin.qq.com"

class WechatLog(models.Model):
    _name = 'sce_wechat.wechat_log'

    name = fields.Char()
    request = fields.Char()
    data = fields.Char()
    response = fields.Char()

class Wechat(models.Model):
    _name = 'sce_wechat.wechat'

    name = fields.Char()
    token = fields.Char()
    corpid = fields.Char()
    agentid = fields.Integer()
    corpsecret = fields.Char()
    is_master = fields.Boolean(default=False)

    def get_token(self):
        if not self.token:
            self.refresh_token()
        return self.token

    def refresh_token(self):
        self.token = get_token(self.env, WECHAT_URL, self.corpid, self.corpsecret)
        print("token="+self.token)

    def send_message(self, user, message):
        raw_message = messages(user, message, self.agentid)
        error_code = send_message(self.env, WECHAT_URL, self.get_token(), raw_message)
        if error_code == 0:
            print ('Succesfully')
        elif error_code==42001:  # access_token expired
            self.refresh_token()
            error_code = send_message(self.env, WECHAT_URL, self.get_token(), raw_message)
        else:
            print ('Failed')

    def action_test(self):
        self.send_message('JinZan', 'Test message')


#--------------------------------
# 记录与微信服务器通信日志
#--------------------------------
def write_log(env, name, request, data, response):
    env['sce_wechat.wechat_log'].create({
        'name': name,
        'request': request,
        'data': data,
        'response': response})


#--------------------------------
# 获取企业微信token
#--------------------------------

def get_token(env, url, corpid, corpsecret):
    token_url = '%s/cgi-bin/gettoken?corpid=%s&corpsecret=%s' % (url, corpid, corpsecret)
    token_resp = urllib.request.urlopen(token_url).read().decode()
    write_log(env, 'GET_TOKEN', token_url, '', token_resp)
    token = json.loads(token_resp)['access_token']
    return token

#--------------------------------
# 构建告警信息json
#--------------------------------
def messages(user, msg, agentid):
    values = {
        "touser": user,
        "msgtype": 'text',
        "agentid": agentid,
        "text": {'content': msg},
        "safe": 0
        }
    msges=(bytes(json.dumps(values), 'utf-8'))
    return msges

#--------------------------------
# 发送告警信息, 返回error_code
#--------------------------------
def send_message(env, url, token, data):
        send_url = '%s/cgi-bin/message/send?access_token=%s' % (url,token)
        response = urllib.request.urlopen(urllib.request.Request(url=send_url, data=data)).read()
        write_log(env,'SEND_MESSAGE', send_url, data, response)
        # print("response="+respone)
        x = json.loads(response.decode())['errcode']
        return x

##############函数结束########################

# corpid = 'wx***********************'
# corpsecret = 'Iwy******************************'
# url = 'https://qyapi.weixin.qq.com'
# msg='test,Python调用企业微信测试'

# #函数调用
# test_token=get_token(url, corpid, corpsecret)
# msg_data= messages(msg)
# send_message(url,test_token, msg_data)
