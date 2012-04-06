
import sys
import os
import urllib
import re
import xbmc
from utilities import *
from song import *
import lyrics


__language__ = sys.modules[ "__main__" ].__language__
__title__ = __language__(30008)
__allow_exceptions__ = True


class XmlUtils :
    @staticmethod
    def removeComments(text):
        begin = text.split("<!--")
        if ( len(begin) > 1 ):
            end = str.join("", begin[1:]).split("-->")
            if ( len(end) > 1 ):
                return XmlUtils.removeComments(begin[0] + str.join("", end[1:]))
        return text


class LyricsFetcher:
    """ required: Fetcher Class for lyricindo """
    def __init__( self ):
        self.base_url = "http://indolyrics.heroku.com/"

    def get_lyrics_start(self, *args):
        lyricThread = threading.Thread(target=self.get_lyrics_thread, args=args)
        lyricThread.setDaemon(True)
        lyricThread.start()
    
    def get_lyrics_thread(self, song):
        print "SCRAPER-DEBUG-lyricsindo: LyricsFetcher.get_lyrics_thread %s" % (song)
        l = lyrics.Lyrics()
        l.song = song
        try:
            lyricText = self._fetch_lyrics( song )
            l.lyrics = lyricText
            l.source = __title__
            return l, None            
        except:
            print "%s::%s (%d) [%s]" % ( self.__class__.__name__, sys.exc_info()[ 2 ].tb_frame.f_code.co_name, sys.exc_info()[ 2 ].tb_lineno, sys.exc_info()[ 1 ])
            return None, __language__(30004) % (__title__)      

    def get_lyrics( self, artist, song ):
        """ *required: Returns song lyrics or a list of choices from artist & song """
        # format artist and song, check for exceptions
        artist = self._format_param( artist )
        song = self._format_param( song, False )
        # fetch lyrics
        lyrics = self._fetch_lyrics( song )
        # if no lyrics found try just artist for a list of songs
        if ( lyrics ): return lyrics
        else:
            return None
    
    def get_lyrics_from_list( self, item ):
        """ *required: Returns song lyrics from user selection - item[1]"""
        lyrics = self.get_lyrics( item[ 0 ], item[ 1 ] )
        return lyrics
        
    def _fetch_lyrics( self, song ):
        """ Fetch lyrics if available """
        try:
            url = self.base_url + "search/gi?title=%s" % (urllib.quote(song.title.lower()))
            print "Search url: %s" % (url)
            lyricText = urllib.urlopen(url).read()
            status = urllib.getcode()
            if (content.length == 0 || status <> 200):
                return None, __language__(30004) % (url)
            
#            lyricText = unicode(lyricText, 'utf8')
            lyricText = XmlUtils.removeComments(lyricText)
            if ( not lyricText ):
                return None, __language__(30002) % (song.title, song.artist) 

            return lyrics
        except:
            return None
        
    def _format_param( self, param, exception=True ):
        """ Converts param to the form expected by www.lyricwiki.org """
        # properly quote string for url
        result = urllib.quote( param )
        # replace any exceptions
        if ( exception and result in self.exceptions ):
            result = self.exceptions[ result ]
        return result
    
# used for testing only
debug = False
debugWrite = False
