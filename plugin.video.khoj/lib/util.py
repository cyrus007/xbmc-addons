import re, urllib2
from xml.dom.minidom import parseString

def resolve_playlist(url):
    r = re.match('https?://(?:www.)(?:youtube.com|youtu.be)/(?:view_playlist\?)p[=/](?P<plid>[0-9A-Za-z_\-]+)', url)
    if r:
        found = r.group('plid')
    else:
        r = re.match('https?://(?:www.)(?:youtube.com|youtu.be)/watch\?feature=player_embedded(?P<list>.+)', url)
        if r:
            plid = r.group('list').split('list=')
            if (len(plid) > 0):
                found = plid[1]
    if r == False:
        return url
    if (len(found) > 16):
        found = found[2:18]
    print "found="+found
    req = urllib2.Request('http://gdata.youtube.com/feeds/api/playlists/'+found+'?v=2')
    response = urllib2.urlopen(req);page=response.read();response.close()
    dom = parseString(page)
    entries = dom.getElementsByTagName('entry')
    urls = []; notskip = False
    for entry in entries:
        link = entry.getElementsByTagName('media:player')[0].getAttribute('url')
        if link:
            urls.append(link)
    print urls
    return urls
