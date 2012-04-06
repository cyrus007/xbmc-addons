import urllib2, re
from xml.dom.minidom import parse, parseString

class Resolver:
    def __init__(self):
        self.name = 'VEOH'

    def videoURL(self, url):
        print self.name + ' url -> ' + url
        try:
            video_id = re.compile('permalinkId=v(.+)').findall(url)
            if len(video_id) == 0:
                video_id = re.compile('/v(.+)').findall(url)
            newURL = 'http://www.veoh.com/rest/v2/execute.xml?method=veoh.video.findByPermalink&permalink=v'+video_id[0]+'&apiKey=E97FCECD-875D-D5EB-035C-8EF241F184E2'
            req = urllib2.Request(newURL)
            req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.8.1.14) Gecko/20080404 Firefox/2.0.0.14')
            req.add_header('Referer', 'http://www.veoh.com/')
            page = urllib2.urlopen(req);response=page.read();page.close()
            domObj = parseString(response)
            if len(domObj.getElementsByTagName("error")) > 0:
                print 'Error: ' + domObj.getElementsByTagName("error")[0].getAttribute('errorMessage')
                return '', domObj.getElementsByTagName("error")[0].getAttribute('errorMessage')
            else:
                url = domObj.getElementByTagName("video")[0].getAttribute("ipodUrl")
                movielink = urllib2.build_opener(urllib2.HTTPRedirectHandler).open(url).url
                print 'Success: ' + movielink
                return movielink, ''
        except: pass
