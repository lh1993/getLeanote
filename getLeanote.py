#!/usr/bin/python
# -*- coding:utf-8 -*-

from requests import Session
import json
import csv
import re

class Leanote(Session):
    def __init__(self, baseUrl):
        Session.__init__(self)
        self.baseUrl = baseUrl

	# 登录
    def login(self, email, password):
        url = self.baseUrl + '/api/auth/login'
        data = {
            "email": email,
            "pwd": password
        }
        response = self.post(url, data=data)
        jsonObj = response.json()
        print('login: %s' % jsonObj)
        assert jsonObj['Ok']
        self.token = jsonObj['Token']
        return self.token

	# 得到所有笔记本
    def getNotebooks(self):
        url = self.baseUrl + '/api/notebook/getNotebooks?token=%s' % self.token
        response = self.get(url)
        jsonObj = json.loads(response.content)
        return jsonObj

	# 获得某笔记本下的笔记(无内容)
    def getNotes(self, notebookId):
        url = self.baseUrl + '/api/note/getNotes?token=%s&notebookId=%s' % (self.token, notebookId)
        response = self.get(url)
        jsonObj = json.loads(response.content)
        return jsonObj

	# 获得某笔记本下的笔记(无内容)
    def getNoteAndContent(self, noteId):
        url = self.baseUrl + '/api/note/getNoteAndContent?token=%s&noteId=%s' % (self.token, noteId)
        response = self.get(url)
        jsonObj = json.loads(response.content)
        return jsonObj

	# 获得笔记内容
    def getNoteContent(self, noteId):
        url = self.baseUrl + '/api/note/getNoteContent?token=%s&noteId=%s' % (self.token, noteId)
        response = self.get(url)
        jsonObj = json.loads(response.content)
        return jsonObj

if __name__ == "__main__":
    url = "http://**************"
	
    email = "lhln0119@163.com"
    password = "********"
	
    leanote = Leanote(url)
    leanote.login(email, password)
    notebook1 = ["运维", "分享", "DBA", "P2P平台报表SQL"]
    notebookId = None
    tmplist = [['账号', '创建时间', '标题']]
    notebooks = leanote.getNotebooks()
    for book in notebooks:
        print book
        
        if book['Title'].encode('utf-8') in notebook1 and book['IsDeleted'] is False:
            notebookId = book['NotebookId']
            print notebookId
            notes = leanote.getNotes(notebookId)

            for note in notes:
                pattern = re.compile('([0-9]{4}-[0-9]{2}-[0-9]{2})')
                createdate = pattern.findall(note['CreatedTime'])
                createdate = createdate[0].encode('utf-8')
                title = note['Title'].encode('utf-8')
                data = [email, createdate, title]
                print data
                tmplist.append(data)

    print tmplist
    with open('leanote.csv', 'wb') as f:
        writer = csv.writer(f, delimiter=',')
        for line in tmplist:
            print line
            writer.writerow(line)
            
