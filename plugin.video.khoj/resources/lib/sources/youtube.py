import urllib, urllib2, re
try:
    from urlparse import parse_qs
except ImportError:
    from cgi import parse_qs
from util import cleanup_url

_UserAgent_ = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.8.1.14) Gecko/20080404 Firefox/2.0.0.14'

class Resolver:
    def __init__(self):
        self.name = 'YOUTUBE'

    def videoURL(self, url):
        print self.name + ' url: ' + url
        if len(url) == 0:
            return '', 'Empty URL'
        try:
            match = re.compile('http://www.youtube.com/p/(.+)$').findall(url)
            if (len(match) == 0):
                match = re.compile('http://www.youtube.com/view_play_list\?p=(.+)$').findall(url)
                if (len(match) == 0): #regular video
                    match = re.compile('http://www.youtube.com/embed/(.+)$').findall(url)
                    if (len(match) == 0):
                        match = re.compile('http://www.youtube.com/watch\?v=(.+)$').findall(url)
                    if (len(match) == 0):
                        match = re.compile('http://www.youtube.com/v/(.+)$').findall(url)
                    video_id = match[0].split('?')
                    if (len(video_id) > 0):
                        match[0] = video_id[0]
                    movielink, error = self.resolveURL(match[0])
                    return movielink, error

#           #playlist
            pl_id = match[0].split('?')
            if (len(pl_id) > 0):
                match[0] = pl_id[0]
            links = []; newlink = []; page = 1
            while True:
                newURL = "http://www.youtube.com/view_play_list?p=%s&page=%s&gl=US&hl=en" % (match[0], page)
                req = urllib2.Request(newURL)
                req.add_header('User-Agent', _UserAgent_)
                req.add_header('Referer', 'http://www.youtube.com/')
                page = urllib2.urlopen(req);response=page.read();page.close()
                ids_in_page = []
                for link in re.finditer(r'/watch\?v=(.*?)&', response):
                    if link.group(1) and link.group(1) not in ids_in_page:
                        ids_in_page.append(link.group(1))
                links.extend(ids_in_page)
                if re.search(r'(?m)>\s*Next\s*</a>', response) is None:
                    break
                page += 1
            print links
            for id in links:
                movielink, error = self.resolveURL(id)
                if error == '':
                    newlink.append(movielink)
                else:
                    return '', error
            return newlink, ''
        except: pass

    def resolveURL(self, vidid):
#       url = urllib2.build_opener(urllib2.HTTPRedirectHandler).open(url).url
        newURL = "http://www.youtube.com/get_video_info?video_id=%s" % (vidid)
        req = urllib2.Request(newURL)
        req.add_header('User-Agent', _UserAgent_)
        req.add_header('Referer', 'http://www.youtube.com/')
        page = urllib2.urlopen(req);response=page.read();page.close()
        info = parse_qs(response)
        if info['status'][0] != 'ok':
            error = info['reason'][0]
            try:
                match = error.split('<br')
                error = match[0]
            except:
                pass
            print error
            return '', error
        title    = info['title'][0]
        video_id = info['video_id'][0]
        fmt_list = info['fmt_list'][0]
        length_seconds = info['length_seconds'][0]
        stream_map = info['url_encoded_fmt_stream_map'][0]
        streams = parse_qs(stream_map)
        movielink = streams['url'][0]
        print self.name + '->' + movielink
        return movielink, ''

