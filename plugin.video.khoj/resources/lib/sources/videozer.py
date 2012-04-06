import re, urllib2, base64
try:
    from json import loads
except:
    from simplejson import loads

_UserAgent_ =  'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.8.1.14) Gecko/20080404 Firefox/2.0.0.14'

class Resolver:
    def __init__(self):
        self.name = 'VIDEOZER'

    def videoURL(self, url):
        print self.name + ' url: ' + url
        try:
            video_id = re.compile('embed/(.+)').findall(url)
            if len(video_id) == 0:
                return '', 'ERROR getting the videoid.'
            newURL = 'http://www.videozer.com/player_control/settings.php?v=' + video_id[0]
            req = urllib2.Request(newURL)
            req.add_header('User-Agent', _UserAgent_)
            req.add_header('Referer', 'http://www.videozer.com/')
            page = urllib2.urlopen(req);response=page.read();page.close()
            settings = loads(response)['cfg']
            movielink = str(base64.b64decode(settings['environment']['token1']))
            print self.name + '->' + movielink
            return movielink, ''
        except: pass
