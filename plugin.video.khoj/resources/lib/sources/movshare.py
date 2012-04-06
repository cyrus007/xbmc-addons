import urllib, urllib2, re

_UserAgent_ = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.8.1.14) Gecko/20080404 Firefox/2.0.0.14'

class Resolver:
    def __init__(self):
        self.name = 'MOVSHARE'

    def videoURL(self, url):
        print self.name + ' url -> ' + url
        try:
#           url = urllib2.build_opener(urllib2.HTTPRedirectHandler).open(url).url
            match=re.compile('http://www.movshare.net/video/(.+)').findall(url)
            if (len(match) == 0):
                match=re.compile('http://www.movshare.net/embed/(.+)/').findall(url)
            newURL = 'http://www.movshare.net/video/'+match[0]
            req = urllib2.Request(newURL)
            req.add_header('User-Agent', _UserAgent_)
            req.add_header('Referer', 'http://www.movshare.net/')
            page = urllib2.urlopen(req);response=page.read();page.close()
            link = ''.join(response.splitlines()).replace('\t','').replace('\'', '"')
            if re.search('Video hosting is expensive. We need you to prove', link):
                values = {'wm' : '1'}
                headers = {'User-Agent' : _UserAgent_ }
                data = urllib.urlencode(values)
                req = urllib2.Request(newURL, data, headers)
                page = urllib2.urlopen(req);response=page.read();page.close()
                link = ''.join(response.splitlines()).replace('\t','').replace('\'', '"')
            match=re.compile('<param name="src" value="(.+?)" />').findall(link)
            if (len(match) == 0):
                match=re.compile('flashvars.file="(.+?)"').findall(link)
            movielink = match[0]
            print self.name + '->' + movielink
            return movielink, ''
        except: pass
