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
    if 'youtube' in server[0]:
        return 'YOUTUBE', os.path.join(mediaPath, "youtube.png")
    elif 'dailymotion' in server[0]:
        return 'DAILYMOTION', os.path.join(mediaPath, "dailymotion.png")
    elif 'hostingcup' in server[0]:
        return 'HOSTINGCUP', os.path.join(mediaPath, "logo.png")
    elif 'hostingbulk' in server[0]:
        return 'HOSTINGBULK', os.path.join(mediaPath, "logo.png")
    elif 'megavideo' in server[0]:
        return 'MEGAVIDEO', os.path.join(mediaPath, "megavideo.gif")
    elif 'veoh' in server[0]:
        return 'VEOH', os.path.join(mediaPath, "veoh.png")
    elif 'vimeo' in server[0]:
        return 'VIMEO', os.path.join(mediaPath, "vimeo.png")
    elif 'veevr' in server[0]:
        return 'VEEVR', os.path.join(mediaPath, "logo.png")
    elif 'videobb' in server[0]:
        return 'VIDEOBB', os.path.join(mediaPath, "videobb.jpg")
    elif 'videozer' in server[0]:
        return 'VIDEOZER', os.path.join(mediaPath, "videozer.jpg")
    elif 'videoweed' in server[0]:
        return 'VIDEOWEED', os.path.join(mediaPath, "videoweed.jpg")
    elif 'novamov' in server[0]:
        return 'NOVAMOV', os.path.join(mediaPath, "novamov.jpg")
    elif 'movshare' in server[0]:
        return 'MOVSHARE', os.path.join(mediaPath, "movshare.png")
    elif 'zshare' in server[0]:
        return 'Z-SHARE', os.path.join(mediaPath, "zshare.png")
    elif 'rangu' in server[0]:
        return 'RANGU', os.path.join(mediaPath, "logo.png")
    elif 'youku' in server[0]:
        return 'UNKNOWN', os.path.join(mediaPath, "logo.png")
    elif 'rajshri' in server[0]:
        return 'UNKNOWN', os.path.join(mediaPath, "logo.png")
    else:
        return 'UNKNOWN', os.path.join(mediaPath, "logo.png")

def getScraper(url):
    if url == '':
        return
    server = re.compile('http://.+?/').findall(url)
    #print '[getScraper] ' + server[0]
    if 'youtube' in server[0]:
        import sources.youtube as scraper
    elif 'dailymotion' in server[0]:
        import sources.dailymo as scraper
    elif 'megavideo' in server[0]:
        import sources.megavid as scraper
    elif 'veoh' in server[0]:
        import sources.veoh as scraper
    elif 'vimeo' in server[0]:
        import sources.vimeo as scraper
    elif 'videobb' in server[0]:
        import sources.videobb as scraper
    elif 'videozer' in server[0]:
        import sources.videozer as scraper
    elif 'videoweed' in server[0]:
        import sources.videoweed as scraper
    elif 'rangu' in server[0]:
        import sources.rangu as scraper
    elif 'novamov' in server[0]:
        import sources.novamov as scraper
    elif 'movshare' in server[0]:
        import sources.movshare as scraper
    elif 'hostingcup' in server[0]:
        import sources.hostingcup as scraper
    elif 'hostingbulk' in server[0]:
        import sources.unknown as scraper
    elif 'veevr' in server[0]:
        import sources.unknown as scraper
    elif 'zshare' in server[0]:
        import sources.zshare as scraper
    else:
        import sources.unknown as scraper
    return scraper.Resolver()

