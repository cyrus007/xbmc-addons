# -*- coding: utf-8 -*-
#------------------------------------------------------------
# Original author Ivo Brhel
# Modified by Swapan Sarkar
#------------------------------------------------------------

import re, sys, os
import urllib2

_UserAgent_ =  'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.8.1.14) Gecko/20080404 Firefox/2.0.0.14'
novamov_url="http://www.novamov.com/api/player.api.php"

class Resolver:
    def __init__(self):
        self.name = 'NOVAMOV'

    def videoURL(self, url):
        print self.name + 'url: ' + url
        try:
            req = urllib2.Request(url)
            req.add_header('User-Agent',_UserAgent_)
            response = urllib2.urlopen(req)
            link = response.read()
            #
            match=re.compile('flashvars.advURL=\"(.+?)\".*').findall(link)
            if match[0] != "0":
                    # src='http://embed.novamov.com/embed.php?width=600&#038;height=480&#038;v=vje17kmmztnbb&#038;px=1'
                    req = urllib2.Request(match[0])
                    req.add_header('User-Agent', _UserAgent_)
                    response = urllib2.urlopen(req)
                    link=response.read()
            match=re.compile('flashvars.file=\"(.+?)\".*').findall(link)
            file=match[0]
            match=re.compile('flashvars.filekey=\"(.+?)\".*').findall(link)
            filekey=match[0]
            #
            #http://www.novamov.com/api/player.api.php?key=fc55ea26c57ac86c74918540a163a917&pass=undefined&file=7cv2x4wtrqzmi&user=undefined&codes=1
            newURL=novamov_url+"?key="+filekey+"&pass=undefined&file="+file+"&user=undefined&codes=1"
            req = urllib2.Request(newURL)
            req.add_header('User-Agent', _UserAgent_)
            response = urllib2.urlopen(req)
            link=response.read()
            response.close()
            #       
            #match=re.compile('url=(.+?)&title=.*').findall(link)
            match=re.compile('url=http://(.+?)&title=.+?').findall(link)
            movielink='http://'+match[0]

            print self.name + '->' + movielink
            return movielink, ''
        except: pass
