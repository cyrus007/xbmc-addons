import urllib2, re

class Resolver:
    def __init__(self):
        self.name = 'RANGU'

    def videoURL(self, url):
        print self.name + ' url -> ' + url
        try:
            req = urllib2.Request(url)
            req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.8.1.14) Gecko/20080404 Firefox/2.0.0.14')
            req.add_header('Referer', 'http://www.rangu.com/')
            page = urllib2.urlopen(req);response=page.read();page.close()
            video_id = re.compile('googleplayer\.swf\?docId=(.+?)"').findall(response)
            if len(video_id) == 0:
                print 'Error: no error message'
                return '', 'ERROR'
            else:
                url = 'http://video.google.com/googleplayer.swf?docId='+video_id[0]
                movielink = urllib2.build_opener(urllib2.HTTPRedirectHandler).open(url).url
                print 'Success: ' + movielink
                return movielink, ''
        except: pass
