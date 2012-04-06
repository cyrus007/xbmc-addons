import urllib, urllib2, re

_UserAgent_ = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.8.1.14) Gecko/20080404 Firefox/2.0.0.14'

class Resolver:
    def __init__(self):
        self.name = 'DAILYMOTION'

    def videoURL(self, url):
        print self.name + ' url: ' + url
        try:
            match=re.compile('http://www.dailymotion.com/(.+)').findall(url)
            if(len(match) > 0):
                newUrl = url.replace('?','&')
                match=re.compile('video/(.+)').findall(newUrl)
                if len(match) == 0:
                    match=re.compile('swf/(.+)').findall(newUrl)
            url = 'http://www.dailymotion.com/video/'+str(match[0])
#           url = urllib2.build_opener(urllib2.HTTPRedirectHandler).open(url).url
            req = urllib2.Request(url)
            req.add_header('User-Agent', _UserAgent_)
            req.add_header('Referer', 'http://www.dailymotion.com/')
            page = urllib2.urlopen(req);response=page.read();page.close()
            sequence=re.compile('"sequence",  "(.+?)"').findall(response)
            newseqeunce = urllib.unquote(sequence[0]).decode('utf8').replace('\\/','/')
            movielink=re.compile('"hqURL":"(.+?)"').findall(newseqeunce)
            if movielink == []:
                movielink=re.compile('"sdURL":"(.+?)"').findall(newseqeunce)

            print self.name + '->' + movielink[0]
            return movielink[0], ''
        except: pass
