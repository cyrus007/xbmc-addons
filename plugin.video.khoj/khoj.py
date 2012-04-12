'''
    Khoj plugin for XBMC
    This is khoj.py
'''

import re, sys, os.path, datetime, urllib, urllib2
import xbmcgui, xbmcaddon
import urlresolver
import util

try:
    from json import loads
except:
    from simplejson import loads
try:
    from sqlite3 import dbapi2 as sqlite
except:
    from pysqlite2 import dbapi2 as sqlite

#MAIN URLS
URLSEARCH = "http://khoj.heroku.com/search?str=%s"
URLGETVID = "http://khoj.heroku.com/getvids?url=%s"
RANGUSEARCH = "http://khoj.heroku.com/rangu/search?str=%s"
RANGUGETVID = "http://khoj.heroku.com/rangu/getvids?url=%s"
STTSEARCH = "http://khoj.heroku.com/stt/search?str=%s"
STTGETVID = "http://khoj.heroku.com/stt/getvids?url=%s"
BMSEARCH = "http://khoj.heroku.com/bm/search?str=%s"
BMGETVID = "http://khoj.heroku.com/bm/getvids?url=%s"

pluginName = sys.modules['__main__'].__plugin__
addonPath = xbmcaddon.Addon(id='plugin.video.khoj').getAddonInfo('path')
mediaPath = os.path.join(addonPath, "resources/thumbnails")

media = { 'youtube':'youtube.png', '180upload':'180upload.png', '2gbhosting':'2gbhosting.png', 'daclips':'logo.png',
          'dailymotion':'dailymotion.png', 'divxstage':'logo.png', 'ecostream':'logo.png', 'filebox':'logo.png',
          'filenuke':'logo.png', 'flashx':'logo.png', 'hostingbulk':'vidpe.png', 'hostingcup':'hostingcup.png',
          'jumbofiles':'logo.png', 'megaupload':'megaupload.png', 'megavideo':'megavideo.png', 'movdivx':'logo.png',
          'movpod':'logo.png', 'movshare':'movshare.png', 'nolimitvideo':'logo.png', 'novamov':'novamov.png',
          'ovfile':'ovfile.png', 'putlocker':'putlocker.png', 'rapidvideo':'rapidvideo.png', 'seeon':'seeon.png',
          'skyload':'logo.png', 'stagevu':'logo.png', 'stream2k':'stream2k.png', 'tubeplus':'tubeplus.png',
          'ufliq':'logo.png', 'uploadc':'logo.png', 'veeHD':'logo.png', 'veoh':'veoh.png', 'videobb':'videobb.png',
          'videoweed':'videoweed.png', 'videozer':'videozer.png', 'vidpe':'vidpe.png', 'vidstream':'logo.png',
          'vidxden':'logo.png', 'xvidstage':'xvidstage.png', 'youku':'logo.png', 'zalaa':'logo.png', 'google':'logo.png',
          'zshare':'zshare.png', 'vimeo':'vimeo.png' }

class Khoj:
    def __init__(self, homer):
        print "[%s] Initializing... Khoj" % (pluginName)
        if homer == '0':
            self.srchurl, self.vidurl = RANGUSEARCH, RANGUGETVID
        elif homer == '1':
            self.srchurl, self.vidurl = STTSEARCH, STTGETVID
        elif homer == '2':
            self.srchurl, self.vidurl = BMSEARCH, BMGETVID
        else:
            self.srchurl, self.vidurl = URLSEARCH, URLGETVID

    def getTitles(self, srchstr):
        """self.items=[{Title, url, Thumb, Plot},...]"""
        fullurl = self.srchurl % (urllib.quote_plus(srchstr))
        print "[%s:getTitles] url = '%s'" % (pluginName, fullurl)
        try:
            req = urllib2.Request(fullurl)
#           req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
            req.add_header('User-Agent', 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.7 (KHTML, like Gecko) Chrome/16.0.912.36 Safari/535.7')
            content=urllib2.urlopen(req).read()
            if "NOT IMPLEMENTED" in content:
                xbmcgui.Dialog().ok('Not implemented yet', "Fetching from this source has not been implemented yet.")
                return
            json_data = loads(content)
            for movie in json_data:
#               if movie['plot'] == None:
#                   movie['Plot'] = ''
#               if movie['plotoutline'] == None:
#                   movie['PlotOutline'] = ''
#               if movie['cast'] == None:
#                   movie['Cast'] = ''
#               if movie['duration'] == None:
#                   movie['Duration'] = ''
#               if movie['resolution'] == None:
#                   movie['VideoResolution'] = ''
                yield {'Title':movie['title'], 'url':movie['url'], 'Thumb':movie['img']}
        except urllib2.HTTPError, e:
            print e.code
            print e.msg
            print e.headers
            print e.fp.read()
        except urllib2.URLError, e:
            print e.reason
            print e.msg
            print e.headers
            print e.fp.read()

    def getServers(self, svrurl):
        """self.servers=[Server,...]"""
        fullurl = self.vidurl % (urllib.quote_plus(svrurl))
        print "[%s:getServers] url = '%s'" % (pluginName, fullurl)
        try:
            req = urllib2.Request(fullurl)
#           req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
            req.add_header('User-Agent', 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.7 (KHTML, like Gecko) Chrome/16.0.912.36 Safari/535.7')
            content=urllib2.urlopen(req).read()
            if "NOT IMPLEMENTED" in content:
                xbmcgui.Dialog().ok('Not implemented yet', "Fetching from this source has not been implemented yet.")
                return
            json_data = loads(content)
            for source in json_data['servers']:
                yield self.Server(seq=source['no'], urls=source['links'])
        except urllib2.HTTPError, e:
            print e.code
            print e.msg
            print e.headers
            print e.fp.read()

    def getVideoDetails(self, url, title):
        """self.videoDetails={Title,Plot,urls},errorcode"""
        print "[%s:getVideoDetails] url = '%s'" % (pluginName, url)
        videourls = []
#       if scraper == None:
#           popup = xbmcgui.Dialog().ok('VIDEO Source not implemented', "This video source has not been implemented yet.", "Try other sources.")
#           return 3, {'Title':'Error', 'Plot':'', 'url':[]}
        if ':;' in url:
            links = url.split(':;')
            total = len(links); done = 0
            progDialog = xbmcgui.DialogProgress()
            progDialog.create('Loading playlist...')
            progString = 'Videos loaded :: [B]%s/%s[/B] into XBMC playlist.' % (done, total)
            progDialog.update(0, "Please wait for the process to retrieve video links.", progString)
            for link in links:
                scraper = urlresolver.HostedMediaFile(url=link, title=title)
                done += 1; percent = (done * 100)/total
                if scraper:
                    vidurl = scraper.resolve()
                    if isinstance(vidurl, list):
                        videourls.extend(vidurl)
                    else:
                        videourls.append(vidurl)
                    progString = 'Videos loaded :: [B]%s/%s[/B] into XBMC playlist.' % (done, total)
                    progDialog.update(percent, "Please wait for the process to retrieve video links.", progString)
                    if progDialog.iscanceled():
                        progDialog.close()
                        return 3, {'Title':'Error', 'Plot':'', 'url':[]}
                else:
                    progDialog.close()
                    xbmcgui.Dialog().ok('Video number %s has errors.' % (done), "Try other sources.")
                    return 3, {'Title':'Error', 'Plot':'', 'url':[]}
            progDialog.close()
            return 0, {'Title':'Video', 'Plot':'', 'url':videourls}
        else:
            urls = util.resolve_playlist(url)
            if isinstance(urls, list):
                for transurl in urls:
                    scraper = urlresolver.HostedMediaFile(url=transurl, title=title)
                    if scraper:
                        vidurl = scraper.resolve()
                        if vidurl:
                            videourls.append(vidurl)
                            print vidurl
                        else:
                            xbmcgui.Dialog().ok('Unsucessful', "Cannot get all videos of playlist.", "Try other sources.")
                            return 3, {'Title':'Error', 'Plot':'', 'url':[]}
                    else:
                        xbmcgui.Dialog().ok('Not Implemented', "Cannot handle this playlist source.", "Try other sources.")
                        return 3, {'Title':'Error', 'Plot':'', 'url':[]}
                return 0, {'Title':'Video', 'Plot':'', 'url':videourls}
            else:
                scraper = urlresolver.HostedMediaFile(url=url, title=title)
                if scraper:
                    vidurl = scraper.resolve()
                    if vidurl:
                        videourls.append(vidurl)
                        return 0, {'Title':'Video', 'Plot':'', 'url':videourls}
                    else:
                        xbmcgui.Dialog().ok('Unsucessful', "Cannot get the video.", "Try other sources.")
                        return 3, {'Title':'Error', 'Plot':'', 'url':[]}
                else:
                    xbmcgui.Dialog().ok('Not Implemented', "Cannot handle this video source.", "Try other sources.")
                    return 3, {'Title':'Error', 'Plot':'', 'url':[]}

    class Server:

        def __init__(self, seq, urls):
            self.sequence = seq
            self.links = []
            for link in urls:
                self.links.append(link)
            if len(urls) > 0:
              self.resolver = urlresolver.HostedMediaFile(url=urls[0])
              if self.resolver:
                  self.name = self.resolver.get_name()
                  self.thumb = os.path.join(mediaPath, media[self.name])
              else:
                  r = re.match('https?://(.+?)/', urls[0])
                  domain = r.groups()[0].replace('www.', '')
                  self.name = domain + '-UNKNOWN'
                  self.thumb = os.path.join(mediaPath, "logo.png")

        def getLinks(self):
            for index, link in enumerate(self.links):
                title = 'Source #' + str(self.sequence) + ' (' + self.name + ') - Part #' + str(index+1)
                yield {'url':link, 'Title':title, 'Thumb':self.thumb}

        def getComboLink(self):
            title = '[B]Source #' + str(self.sequence) + ' (' + str(self.name) + ')[/B] [I]Directplay playlist of following ' + str(len(self.links)) + ' videos[/I]'
            url = ''
            for link in self.links:
                if url == '':
                  url = url + link
                else:
                  url = url + ':;' + link
            return {'url':url, 'Title':title, 'Thumb':self.thumb}

class KhojDB:

    def __init__(self, dbconn):
        try:
            self.dbconn = sqlite.connect(dbconn)
            self.initDB()
        except Exception, e:
            print e
            pass

    def initDB(self):
        try:
            self.dbconn.execute("PRAGMA synchronous = OFF")
            self.dbconn.execute("PRAGMA default_synchronous = OFF")
            self.dbconn.execute("PRAGMA journal_mode = OFF")
            self.dbconn.execute("PRAGMA temp_store = MEMORY")
            self.dbconn.execute("PRAGMA encoding = \"UTF-8\"")
        except Exception, e:
            pass

        try:
            self.dbconn.execute("""CREATE TABLE search_terms (
                                     key varchar primary key,
                                     value varchar,
                                     stamp timestamp )""")
        except:
            pass

    def add(self, srchstr):
        try:
            self.dbconn.execute("""INSERT INTO search_terms ( value, stamp )
                                      VALUES ( ?, ? )""",
                                  (srchstr, datetime.datetime.now()))
            self.dbconn.commit()
        except sqlite.IntegrityError:
            pass
        except Exception, e:
            print e
            pass

    def getHistory(self):
        srchlist = []
        try:
            cur = self.dbconn.cursor()
            cur.execute("SELECT DISTINCT value FROM search_terms ORDER BY stamp DESC LIMIT 15")
            for tuple in cur:
                srchlist.append(tuple[0])
        except Exception, e:
            print e
            pass
        return srchlist
