import urllib, urllib2, re

_UserAgent_ = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.8.1.14) Gecko/20080404 Firefox/2.0.0.14'

class Resolver:
    def __init__(self):
        self.name = 'Z-SHARE'

    def videoURL(self, url):
        print self.name + ' url -> ' + url
#       try:
#           url = urllib2.build_opener(urllib2.HTTPRedirectHandler).open(url).url
        req = urllib2.Request(url)
        req.add_header('User-Agent', _UserAgent_)
        req.add_header('Referer', 'http://www.zshare.net/')
        page = urllib2.urlopen(req);response=page.read();page.close()
        match = re.compile('iframe src\="http://www.zshare.net/videoplayer(.+?)"').findall(response)
        newURL = 'http://www.zshare.net/videoplayer%s' % (match[0].replace(' ','%20'))
        req = urllib2.Request(newURL)
        req.add_header('User-Agent', _UserAgent_)
        response = urllib2.urlopen(req);link=response.read();response.close()
        movielink = re.compile('file: "(.+?)"').findall(link)[0]
        movielink = movielink.replace(' ','%20')+'|User-Agent='+urllib.quote_plus(_UserAgent_+'&Accept='+urllib.quote_plus('text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')+'&Accept_Encoding='+urllib.quote_plus('gzip, deflate'))
        print self.name + '->' + movielink
        return movielink, ''
#       except: pass
