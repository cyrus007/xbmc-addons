import urllib2, re
from util import parseValue

_UserAgent_ = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.8.1.14) Gecko/20080404 Firefox/2.0.0.14'

class Resolver:
    def __init__(self):
        self.name = 'HOSTING-CUP'

    def videoURL(self, url):
        print self.name + ' url -> ' + url
        try:
#           url = urllib2.build_opener(urllib2.HTTPRedirectHandler).open(url).url
            vidid=re.compile('http://www.hostingcup.com/(.+?)').findall(url)
            if (len(vidid) == 0):
                return '', 'Error extracting video_id from URL'
            newURL = "http://vidpe.com/%s" % vidid[0]
            req = urllib2.Request(url)
            req.add_header('User-Agent', _UserAgent_)
            req.add_header('Referer', 'http://www.hostingcup.net/')
            page = urllib2.urlopen(req);response=page.read();page.close()
            link = ''.join(response.splitlines()).replace('\t','')
            params = re.compile("return p\}\(\'(.+?)\',36,(.+?),\'(.+?)\'").findall(link)
            result = parseValue(params[0][0], 36, int(params[0][1]), params[0][2].split('|'))
            result = result.replace('\\','').replace('"','\'')
            movielink = re.compile("s1.addVariable\(\'file\',\'(.+?)\'\);").findall(result)[0]
            print self.name + '->' + movielink
            return movielink, ''
        except: pass
