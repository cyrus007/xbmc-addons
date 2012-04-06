# -*- coding: utf-8 -*-
#------------------------------------------------------------
# Original author Ivo Brhel
# Modified by Swapan Sarkar
#------------------------------------------------------------
import re, urllib2
import os

_UserAgent_ =  'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.8.1.14) Gecko/20080404 Firefox/2.0.0.14'

class Resolver:
    def __init__(self):
        self.name = 'VIDEOWEED'

    def videoURL(self, url):
        print self.name + 'url: ' + url
        try:
            data = self.getUrlData(url)
            patronvideos = 'flashvars\.domain="(.+?)"[\s|\S]*?flashvars\.file="(.+?)"[\s|\S]*?flashvars\.filekey="(.+?)";'
            match = re.compile(patronvideos,re.DOTALL).findall(data)
            movielink = "";
            if len(match)>0:
                data = getUrlData('%s/api/player.api.php?file=%s&key=%s&user=undefined&codes=undefined&pass=undefined'% (match[0][0],match[0][1],match[0][2]))
                match = re.compile("url=(.+?[^\&]+)").findall(data)
                if len(match)>0:
                    movielink=match[0]
                else:
                    return '', 'Error in extracting movielink.'
            print self.name + '->' + movielink
            return movielink, ''
        except: pass

    def getUrlData(url):
        req = urllib2.Request(url)
        req.add_header('User-Agent',_UserAgent_)
        response = urllib2.urlopen(req)
        data=response.read()
        response.close()
        return data
