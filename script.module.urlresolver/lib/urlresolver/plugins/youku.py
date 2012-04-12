'''
youku urlresolver plugin
Copyright (C) 2012 cyrus007

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program. If not, see <http://www.gnu.org/licenses/>.
'''

import re, random, urllib2
from t0mm0.common.net import Net
from urlresolver import common
from urlresolver.plugnplay.interfaces import UrlResolver
from urlresolver.plugnplay.interfaces import PluginSettings
from urlresolver.plugnplay import Plugin

class YoukuResolver(Plugin, UrlResolver, PluginSettings):
    implements = [UrlResolver, PluginSettings]
    name = "youku"

    def __init__(self):
        p = self.get_setting('priority') or 100
        self.priority = int(p)
        self.net = Net()

    def get_media_url(self, host, media_id):
        web_url = self.get_url(host, media_id)
        try:
            req = urllib2.Request(web_url)
            stream_url = urllib2.urlopen(req).geturl()
        except urllib2.URLError, e:
            common.addon.log_error(self.name + ': got http error %d fetching %s' %
                                    (e.code, web_url))
            return False
        print stream_url
        return stream_url

    def get_url(self, host, media_id):
        return 'http://player.youku.com/player.php/sid/%s' % media_id
        
        
    def get_host_and_id(self, url):
        r = re.search('//(?:.+)?(youku.com)/player.php/sid/(.+)', url)
        if r:
            return r.groups()
        else:
            return False


    def valid_url(self, url, host):
        return re.match('https?://(?:.+)?youku.com/(?:player.php/sid/|v_show/id_)(.+)', url) or 'youku' in host 
    
