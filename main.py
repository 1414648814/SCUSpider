# -*- coding:utf-8 -*-

import urllib
import urllib2
import cookielib
import re
import HTMLParser

class SCU:
    def __init__(self):
        self.loginURL = 'http://202.115.47.141/loginAction.do'
        self.gradeURL = 'http://202.115.47.141/gradeLnAllAction.do?type=ln&oper=fainfo&fajhh=848'
        # gradeLnAllAction.do?type=ln&oper=sxinfo&lnsxdm=001 课程属性成绩
        # gradeLnAllAction.do?type=ln&oper=fainfo&fajhh=848 方案成绩
        # gradeLnAllAction.do?type=ln&oper=lnfaqk&flag=zx 方案完成情况
        # gradeLnAllAction.do?type=ln&oper=qb 全部及格成绩（分学期）
        # gradeLnAllAction.do?type=ln&oper=bjg 不及格成绩
        # bxqcjcxAction.do 本学期成绩

        self.user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
        self.headers = {'User-Agent':self.user_agent}
        self.cookies = cookielib.CookieJar()
        self.postData = urllib.urlencode({
            'zjh':'2012141463069',
            'mm':'110017'
        })
        self.opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cookies))
        self.html_parser = HTMLParser.HTMLParser()
        self.allGrades = []

    def getPage(self):
        request = urllib2.Request(url=self.loginURL,data=self.postData,headers=self.headers)
        result = self.opener.open(request)
        result = self.opener.open(self.gradeURL)
        pageCode = result.read().decode('gbk')
        return pageCode

    def getGrades(self):
        pageCode = self.getPage()
        if not pageCode:
            print "page load error"
            return None
        pattern = re.compile(r'<tr class="odd".*?<td.*?>(.*?)</td>.*?<td.*?>(.*?)</td>.*?<td.*?>(.*?)</td>.*?<td.*?>(.*?)</td>.*?<td.*?>(.*?)</td>.*?<td.*?>(.*?)</td>.*?<td.*?<p.*?>(.*?)</P>.*?</td>.*?<td.*?<p.*?>(.*?)</P>.*?</td>',re.S)
        # pattern = re.compile(r'<tr class="odd".*?<td.*?<p.*?>(.*?)</P>.*?</td>.*?<td.*?<p.*?>(.*?)</P>.*?</td>',re.S)

        items = re.findall(pattern,pageCode)
        if items:
            print "Found group"
        else:
            print "No found"
        grades = []

        for item in items:
            grades.append([item[0].strip(),item[1].strip(),item[2].strip(),item[3].strip(),item[4].strip(),item[5].strip(),self.html_parser.unescape(item[6].strip()),self.html_parser.unescape(item[7].strip())])
            # grades.append([self.html_parser.unescape(item[0].strip()),self.html_parser.unescape(item[1].strip())])
        return grades

    def printGrades(self):
        index = 1
        self.allGrades = self.getGrades()
        for item in self.allGrades:
            print u"第%d个\t 课程号:%s\t 课序号:%s\t 课程名:%s\t 英文课程名:%s\t 学分:%s\t 课程属性:%s\t 成绩:%s\t 原因:%s\n" %(index,item[0],item[1],item[2],item[3],item[4],item[5],item[6],item[7])
            # print u"第%d个\t 成绩:%s\t 原因:%s\n" %(index,item[0],item[1])
            index+=1

if __name__ == '__main__':
    scu = SCU()
    scu.printGrades()
