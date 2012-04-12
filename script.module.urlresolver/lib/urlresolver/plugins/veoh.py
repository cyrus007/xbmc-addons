"""
    urlresolver XBMC Addon
    Copyright (C) 2011 anilkuj

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

import re
from t0mm0.common.net import Net
from urlresolver import common
from urlresolver.plugnplay.interfaces import UrlResolver
from urlresolver.plugnplay.interfaces import PluginSettings
from urlresolver.plugnplay import Plugin

class VeohResolver(Plugin, UrlResolver, PluginSettings):
    implements = [UrlResolver, PluginSettings]
    name = "veoh"

    def __init__(self):
        p = self.get_setting('priority') or 100
        self.priority = int(p)
        self.net = Net()

    def get_media_url(self, host, media_id):
        print self.name + ': host %s media_id %s' %(host, media_id)

        html = self.net.http_GET("http://www.veoh.com/iphone/views/watch.php?id=" + media_id + "&__async=true&__source=waBrowse").content
        if not re.search('This video is not available on mobile', html):
            r = re.compile("watchNow\('(.+?)'").findall(html)
            if (len(r) > 0 ):
                return r[0]

        url = 'http://www.veoh.com/rest/video/'+media_id+'/details'
        html = self.net.http_GET(url).content
        file = re.compile('fullPreviewHashPath="(.+?)"').findall(html)
        if len(file) == 0:
            return False

        return file[0]

    def get_url(self, host, media_id):
        return 'http://veoh.com/watch/%s' % media_id


    def get_host_and_id(self, url):
        r = None
        video_id = None
        if 'permalinkId=' in url:
            r = re.match('veoh.com.+?permalinkId=(\w+)&*.*$', url)
        elif 'watch/' in url:
            r = re.match('(?:.+)watch/(.+)', url)
        elif 'videos/' in url:
            r = re.match('(?:.+)videos/(.+)', url)
            
        if r:
            video_id = r.groups()[-1]
        if video_id:
            return ('veoh.com', video_id)
        else:
            common.addon.log_error('veoh: video id not found')
            return False

    def valid_url(self, url, host):
        return re.search('www.veoh.com/.+?(watch|videos)?/.+',url) or re.search('www.veoh.com/.+?permalinkId=.+',url) or self.name in host

    def get_settings_xml(self):
        xml = PluginSettings.get_settings_xml(self)
        xml += '<setting label="This plugin calls the veoh addon - '
        xml += 'change settings there." type="lsep" />\n'
        return xml
