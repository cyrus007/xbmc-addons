'''
    Khoj plugin for XBMC
    This is khoj.py
'''

import re, sys, os.path, datetime, urllib, urllib2
import xbmcgui, xbmcaddon
import urlresolver
from t0mm0.common.net import Net
from BeautifulSoup import BeautifulSoup
import util

try:
    from json import loads
except:
    from simplejson import loads
try:
    from sqlite3 import dbapi2 as sqlite
except:
    from pysqlite2 import dbapi2 as sqlite


pluginName = sys.modules['__main__'].__plugin__
mediaPath = os.path.join(xbmcaddon.Addon(id='plugin.video.khoj').getAddonInfo('path'), "resources/thumbnails")

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
    def __init__(self, path):
        print "[%s] Initializing... Khoj" % (pluginName)
        self.db = NumiDB(path)

    def getTitles(self, srchstr):
        """self.items=[{Title, url, Thumb, Plot},...]"""
        print "[%s:getTitles] search string = '%s'" % (pluginName, srchstr)
        content = self.db.searchTitle(srchstr)
        if "NOT IMPLEMENTED" in content:
            xbmcgui.Dialog().ok('Not implemented yet', "Fetching from this source has not been implemented yet.")
            return
        for movie in content:
            yield {'Title':str(movie['title']), 'url':str(movie['url']), 'Thumb':str(movie['banner']), 'key':str(movie['key'])}

    def getServers(self, key, url):
        """self.servers=[Server,...]"""
        print "[%s:getServers] url = '%s'" % (pluginName, url)
        content = Net().http_GET(url).content
        tree = BeautifulSoup(content)
#probably we should use ElementTree
#       title = tree.findtext('div.middle_movies/div.post/h2')
#       node  = tree.find('div.middle_movies/div.post/div')
        title = tree.find('div', {'class':'middle_movies'}).find('div', {'class':'post'}).find('h2').string
        node = tree.find('div', {'class':'middle_movies'}).find('div', {'class':'post'}); node = node.extract(); node = node.findAll('div')
        banner = node[2].p.img['src']
        if not self.db.getBanner(key) and banner and banner != '':
            self.db.setBanner(key, banner)
        splice = str(node[2])
        lines = splice.split('<br'); total = len(lines)
        if total < 3:
            return
        splices = splice.split('Online'); lines = splices[1].split('Server')
        total = len(lines); count = 1
        if total == 1:  #this means it did not find any server line
            r = re.findall('href="(https?://[^"]+)"', lines[0])
            if r:
                links = []
                for link in r:
                    links.append(link)
                yield self.Server(seq=1, urls=links)
        else:
            while count < total:
                r = re.findall('href="(https?://[^"]+)"', lines[count])
                if r:
                    links = []
                    for link in r:
                        links.append(link)
                    yield self.Server(seq=count, urls=links)
                count += 1


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

    def updateRangu(self, path):
        progDialog = xbmcgui.DialogProgress()
        progDialog.create('Initializing database...')
        progDialog.update(0, "Please wait for the process to retrieve video links.", 'Updating database :: ...')

        numidb = NumiDB(path)
        numidb.initDB(force=True)
        content = Net().http_GET("http://movies.rangu.com/hindi-movies-list-a-to-z").content
        tree = BeautifulSoup(content)
        links = str(tree.find('div', { 'class' : 'tabcontentstyle'}))
        r = re.findall('<a href="(https?://movies.rangu.com/[^"]+)">(.+)</a>', links)
        if r:
            done = 0; total = len(r)
            for link in r:
                url = link[0]; title = link[1]
                done += 1; percent = (done * 100)/total
                progString = 'Updating database :: [B]%s/%s[/B] into database.' % (done, total)
                progDialog.update(percent, "Please wait for the process to retrieve video links.", progString)
                if progDialog.iscanceled():
                    progDialog.close()
                numidb.addTitle(title, url)
            progDialog.close()
#           xbmcgui.Dialog().ok('Sucessfull updated the database', "Movies database has been re-initilized successfully.")
        else:
            print links
 
            

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
            self.dbconn.execute("""CREATE TABLE IF NOT EXISTS search_terms (
                                     key integer primary key,
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

class NumiDB:

    def __init__(self, dbconn):
        self.limit = 100
        try:
            self.dbconn = sqlite.connect(dbconn)
#           self.initDB()
        except Exception, e:
            print e
            pass

    def initDB(self, force=False):
        try:
            self.dbconn.execute("PRAGMA synchronous = OFF")
            self.dbconn.execute("PRAGMA default_synchronous = OFF")
            self.dbconn.execute("PRAGMA journal_mode = OFF")
            self.dbconn.execute("PRAGMA temp_store = MEMORY")
            self.dbconn.execute("PRAGMA encoding = \"UTF-8\"")
        except Exception, e:
            pass

        try:
            if force:
                self.dbconn.execute("""CREATE TABLE numi_titles (
                                     key integer primary key,
                                     title varchar NOT NULL,
                                     url varchar NOT NULL,
                                     banner varchar )""")
            else:
                self.dbconn.execute("""CREATE TABLE IF NOT EXISTS numi_titles (
                                     key integer primary key,
                                     title varchar NOT NULL,
                                     url varchar NOT NULL,
                                     banner varchar )""")
            self.dbconn.commit()
        except:
            pass

    def addTitle(self, title, url):
        try:
            self.dbconn.execute("""INSERT INTO numi_titles ( title, url ) VALUES ( ?, ? )""",
                                  (title, url))
            self.dbconn.commit()
        except sqlite.IntegrityError:
            pass
        except Exception, e:
            print e
            pass

    def setBanner(self, key, banner):
        try:
            cur = self.dbconn.cursor()
            cur.execute("""UPDATE numi_titles SET banner=? WHERE key=? """,
                                  (banner, key))
            self.dbconn.commit()
            if cur.rowcount == 0:
                print "[%s:addBanner] Banner update failed for title=%s and banner=%s" % (pluginName, title, banner)
        except Exception, e:
            print e
            pass

    def getBanner(self, key):
        banner = None
        try:
            cur = self.dbconn.cursor()
            cur.execute("""SELECT banner FROM numi_titles WHERE key=? LIMIT 1 """, (key,))
            if cur.rowcount < 1:
                return False
            else:
                for tuple in cur:
                    banner = tuple[0]
        except Exception, e:
            print e
            pass
        return banner

    def searchTitle(self, srchstr):
        srchlist = []
        try:
            cur = self.dbconn.cursor()
            cur.execute("""SELECT key,title,url,banner FROM numi_titles WHERE title LIKE ? ORDER BY title LIMIT ?""",
                                  ('%'+srchstr+'%', self.limit))
            for tuple in cur:
                srchlist.append({'key':tuple[0], 'title':tuple[1], 'url':tuple[2], 'banner':tuple[3]})
        except Exception, e:
            print e
            pass
        return srchlist
