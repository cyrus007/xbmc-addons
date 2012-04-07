import urllib2
import os.path, re, sys
import xbmcaddon

pluginName = sys.modules['__main__'].__plugin__
addonPath = xbmcaddon.Addon(id='plugin.video.khoj').getAddonInfo('path')
mediaPath = os.path.join(addonPath, "thumbnails")


def getSource(url):
    if url == '':
        return 'Empty source'
    server = re.compile('http://.+?/').findall(url)
    #print '[getSource] ' + server[0]
#   if 'youtube' in server[0]:
#       return 'YOUTUBE', os.path.join(mediaPath, "youtube.png")
#   else:
#       return 'UNKNOWN', os.path.join(mediaPath, "logo.png")

def getScraper(url):
    if url == '':
        return
    server = re.compile('http://.+?/').findall(url)
    #print '[getScraper] ' + server[0]
#   if 'youtube' in server[0]:
#       import sources.youtube as scraper
#   else:
#       import sources.unknown as scraper
    return scraper.Resolver()

