"""
  Khoj - main routines
"""
import os.path, sys, urllib, xbmc, xbmcplugin, xbmcgui, xbmcaddon
import khoj

__settings__ = xbmcaddon.Addon(id='plugin.video.khoj')
getLS = __settings__.getLocalizedString
dbPath = xbmc.translatePath(os.path.join(__settings__.getAddonInfo('Profile'), 'numisearch.db'))

Khoj = khoj.Khoj()
DB = khoj.KhojDB(dbPath)


class updateArgs:

    def __init__(self, *args, **kwargs):
        for key, value in kwargs.iteritems():
            if value == 'None':
                kwargs[key] = None
            else:
                kwargs[key] = urllib.unquote_plus(kwargs[key])
        self.__dict__.update(kwargs)


class UI:

    def __init__(self):
        self.main = Main(checkMode = False)
        xbmcplugin.setContent(int(sys.argv[1]), 'movies')

    def endofdirectory(self, sortMethod = 'title'):
#       # set sortmethod to something xbmc can use
#       if sortMethod == 'title':
#           sortMethod = xbmcplugin.SORT_METHOD_LABEL
#       elif sortMethod == 'date':
#           sortMethod = xbmcplugin.SORT_METHOD_DATE
#       #Sort methods are required in library mode.
#       xbmcplugin.addSortMethod(int(sys.argv[1]), sortMethod)
        #If name is next or previous, then the script arrived here from a navItem, and won't to add to the heirarchy
        if self.main.args.name in [getLS(30020), getLS(30021)]:
            dontAddToHierarchy = True
        else:
            dontAddToHierarchy = False
        #let xbmc know the script is done adding items to the list.
        xbmcplugin.endOfDirectory(handle = int(sys.argv[1]), updateListing = dontAddToHierarchy)

    def addItem(self, info, isFolder=True):
        #Defaults in dict. Use 'None' instead of None so it is compatible for quote_plus in parseArgs
        info.setdefault('url', 'None')
        info.setdefault('Thumb', 'None')
        info.setdefault('Icon', info['Thumb'])
        #create params for xbmcplugin module
        u = sys.argv[0]+\
            '?url='+urllib.quote_plus(info['url'])+\
            '&mode='+urllib.quote_plus(info['mode'])+\
            '&name='+urllib.quote_plus(info['Title'].encode('ascii','ignore'))+\
            '&icon='+urllib.quote_plus(info['Thumb'])            
        #create list item
        if info['Title'].startswith(" "):
          title = info['Title'][1:]
        else:
          title = info['Title']  
        li=xbmcgui.ListItem(label = title, iconImage = info['Icon'], thumbnailImage = info['Thumb'])
        li.setInfo(type='Video', infoLabels=info)
        #for videos, replace context menu with queue and add to favorites
        if not isFolder:
#           li.setProperty("IsPlayable", "true")#let xbmc know this can be played, unlike a folder.
            #add context menu items to non-folder items.
            contextmenu = [(getLS(13347), 'Action(Queue)')]
            #replaceItems=True replaces the useless one with the two defined above.
            li.addContextMenuItems(contextmenu, replaceItems=True)
        #for folders, completely remove contextmenu, as it is totally useless.
        else:
            li.addContextMenuItems([], replaceItems=True)
        #add item to list
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=u, listitem=li, isFolder=isFolder)
        return ok

    def navItems(self, navItems, mode):
        if navItems['next']:
            self.addItem({'Title': getLS(30020), 'url':navItems['next'], 'mode':mode})
        if navItems['previous']:
            self.addItem({'Title': getLS(30021), 'url':navItems['previous'], 'mode':mode})

    def showSearch(self):
        self.addItem({'Title':getLS(30004), 'mode':'keyboard', 'Plot':getLS(30034)})  #search
#       self.addItem({'Title':'Test', 'mode':'test'})                                 #test
        for srch_string in DB.getHistory():
            self.addItem({'Title':srch_string, 'mode':'history', 'Plot':getLS(30034)})#history
        self.endofdirectory()

    def keyboard(self):
        keyboard = xbmc.Keyboard('', getLS(30001))
        keyboard.doModal()
        if (keyboard.isConfirmed() == False):
            return
        search_string = keyboard.getText()
        if len(search_string) == 0:
            return
        DB.add(search_string.strip())
        self.searchResults(search_string.strip())

    def searchResults(self, srch_str):
        for srchItem in Khoj.getTitles(srch_str, self.main.settings['scraper']):
            srchItem['mode'] = 'links'
            self.addItem(srchItem, isFolder = True)
        self.endofdirectory()

    def showLinks(self):
        for server in Khoj.getServers(self.main.args.url, self.main.settings['scraper']):
            if len(server.links) > 1:
                combolink = server.getComboLink()
                combolink['mode'] = 'playVideo'
                self.addItem(combolink, isFolder = False)
            for link in server.getLinks():
                link['mode'] = 'playVideo'
                self.addItem(link, isFolder = False)
        #end the list
        self.endofdirectory()

    def playVideo(self, title):
        errorCode, videos = Khoj.getVideoDetails(self.main.args.url, title)
        print videos['url']
        if (len(videos['url']) == 0):
#           popup = xbmcgui.Dialog()
#           popup.ok('Error with Video', "Malformed video playlist.", "Try other sources.")
            return True
        elif (len(videos['url']) > 1):
            playlist = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
            playlist.clear()
            for link in videos['url']:
                    print link
                    li=xbmcgui.ListItem(label = title, path = link,
                                iconImage = self.main.args.icon,
                                thumbnailImage = self.main.args.icon)
                    li.setInfo(type = 'Video', infoLabels = {'Title':title, 'url':link})
                    playlist = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
                    playlist.add(url = link, listitem = li)
            xbmcPlayer = xbmc.Player()
            xbmcPlayer.play(playlist)
            if not xbmcPlayer.isPlayingVideo():
                popup = xbmcgui.Dialog()
                popup.ok('Invalid video playlist', "Video in playlist were removed due to copyright issue.", "Try other sources.")
        else:
            link = videos['url'][0]
            li=xbmcgui.ListItem(label = title, path = link,
                            iconImage = self.main.args.icon,
                            thumbnailImage = self.main.args.icon)
            li.setInfo(type = 'Video', infoLabels = {'Title':title, 'Plot': videos['Plot'], 'url':link})
            xbmcPlayer = xbmc.Player()
            xbmcPlayer.play(link)
            if not xbmcPlayer.isPlayingVideo():
                popup = xbmcgui.Dialog()
                popup.ok('Invalid video playlist', "Video was removed due to copyright issue.", "Try other sources.")
#           xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, li)

class Main:

    def __init__(self, checkMode = True):
        self.user = None
        self.parseArgs()
        self.getSettings()
        if checkMode:
            self.checkMode()

    def parseArgs(self):
        # call updateArgs() with our formatted argv to create the self.args object
        if (sys.argv[2]):
            exec "self.args = updateArgs(%s')" % (sys.argv[2][1:].replace('&', "',").replace('=', "='"))
        else:
            # updateArgs will turn the 'None' into None.
            # Don't simply define it as None because unquote_plus in updateArgs will throw an exception.
            # This is a pretty ugly solution, but fuck it :(
            self.args = updateArgs(mode = 'None', url = 'None', name = 'None')

    def getSettings(self):
        self.settings = dict()
        if (not __settings__.getSetting('scraper')):
            __settings__.openSettings()
        self.settings['scraper'] = __settings__.getSetting('scraper')

    def checkMode(self):
        mode = self.args.mode
        title = self.args.name
        if mode is None:
            UI().showSearch()
        elif mode == 'playVideo':
            UI().playVideo(title)
        elif mode == 'search':
            UI().showSearch()
        elif mode == 'keyboard':
            UI().keyboard()
        elif mode == 'links':
            UI().showLinks()
        elif mode == 'history':
            UI().searchResults(title)
