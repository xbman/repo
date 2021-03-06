import util, urllib2 , os , xbmcaddon , urllib , xbmcgui , xbmcplugin , sqlite3


mysettings = xbmcaddon.Addon(id = 'plugin.video.YouNow')
getSetting = xbmcaddon.Addon().getSetting
langmode = int(mysettings.getSetting('lang_type'))
if langmode == 0:
    TheLang = 'en'
elif langmode == 1:
    TheLang = 'es'
elif langmode == 2:
    TheLang = 'me'
elif langmode == 3:
    TheLang = 'de'
elif langmode == 4:
    TheLang = 'fr'
elif langmode == 5:
    TheLang = 'pt'
elif langmode == 6:
    TheLang = 'tr'
elif langmode == 7:
    TheLang = 'ww'
younow = 'https://api.younow.com/php/api/younow/trendingUsers/locale=' + TheLang + '/numberOfRecords=50/startFrom='
younowtags = 'https://api.younow.com/php/api/younow/queue/locale=' + TheLang + '/numberOfRecords=50/startFrom='  # /tag=sumtag
#younowuser = 'https://api.younow.com/php/api/broadcast/info/curId=0/user='
youtags = 'https://api.younow.com/php/api/younow/popularTags/locale=' + TheLang

profile = mysettings.getAddonInfo('profile')
home = mysettings.getAddonInfo('path')
fanart = xbmc.translatePath(os.path.join(home, 'fanart.jpg'))
icon = xbmc.translatePath(os.path.join(home, 'icon.png'))
nexticon = xbmc.translatePath(os.path.join(home, 'next.png'))
refreshicon = xbmc.translatePath(os.path.join(home, 'clear.png'))
logos = xbmc.translatePath(os.path.join(home, 'icon.png')) # subfolder for logos
homemenu = xbmc.translatePath(os.path.join(home, 'resources', 'playlists'))

enable_clear_images = mysettings.getSetting('enable_clear_images')
enable_trending_users = mysettings.getSetting('enable_trending_users')
enable_trending_tags = mysettings.getSetting('enable_trending_tags')
enable_settings = mysettings.getSetting('enable_settings')
enable_custom_view = mysettings.getSetting('enable_custom_view')
menu_view = mysettings.getSetting('menu_view')
thumb_view = mysettings.getSetting('thumb_view')
#xbmc.executebuiltin("Container.SetViewMode(50)")

ClearImages = 'ClearImages'
NextPage = 'NextPage'
PageOne = 'PageOne'
Tagsz = 'Tagsz'
Categories = 'Categories'
Settings = 'Settings'
#xbmcplugin.setContent(int(sys.argv[1]), 'movies')

def searchUser(url,mode,top,pn,tag,v):
    try:
        keyb = xbmc.Keyboard('', '[COLOR yellow]Enter search text[/COLOR]')
        keyb.doModal()
        if (keyb.isConfirmed()):
            searchText = urllib.quote_plus(keyb.getText())
            user = str(searchText)
        TheUrl = younowuser + user
        tag = 'None'
        #buildMenu(TheUrl,url,mode,top,pn,tag,v)
        add_dir(TheUrl, PageOne, 0, 1, 'None', 2, icon, fanart)
    except:
        pass

def setView(content, viewType):
    # set content type so library shows more views and info
    if content:
        xbmcplugin.setContent(int(sys.argv[1]), content)
    if mysettings.getSetting('enable_custom_view') == 'true':
        xbmc.executebuiltin("Container.SetViewMode(%s)" % mysettings.getSetting(viewType) )

    # set sort methods - probably we don't need all of them
    xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_UNSORTED )
    xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_LABEL )
    #xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_VIDEO_RATING )
    #xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_DATE )
    #xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_PROGRAM_COUNT )
    #xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_VIDEO_RUNTIME )
    xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_GENRE )
    #xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_MPAA_RATING )


def get_params():
	param = []
	paramstring = sys.argv[2]
	if len(paramstring)>= 2:
		params = sys.argv[2]
		cleanedparams = params.replace('?', '')
		if (params[len(params)-1] == '/'):
			params = params[0:len(params)-2]
		pairsofparams = cleanedparams.split('&')
		param = {}
		for i in range(len(pairsofparams)):
			splitparams = {}
			splitparams = pairsofparams[i].split('=')
			if (len(splitparams)) == 2:
				param[splitparams[0]] = splitparams[1]
	return param


def playVideo(params):
        videoLink = params['video']
        url = params['Page']
        mode = params['Type']
        top = params['top']
        pn = params['pn']
        tag = params['tag']
        viewers = params['v']
        tg = params['tg']
        likes = params['likes']
        fans = params['fans']
        util.playMedia(params['title'], viewers, tg, likes, fans, params['image'], videoLink, 'Video')

def add_dir(name, url, top, pn, tag, v, mode, iconimage, fanart):
    u = sys.argv[0] + "?url=" + urllib.quote_plus(url) + "&top=" + str(top) + "&pn=" + str(pn) + "&tag=" + str(tag) + "&v=" + str(v) + "&mode=" + str(mode) + "&name=" + urllib.quote_plus(name) + "&iconimage=" + urllib.quote_plus(iconimage)
    ok = True
    liz = xbmcgui.ListItem(name, iconImage = "DefaultFolder.png", thumbnailImage = iconimage)
    fanart = fanart
    liz.setArt({'fanart': fanart})
    liz.setInfo(type="Video", infoLabels={ "Title": name, "plot": name })
    ok = xbmcplugin.addDirectoryItem(handle = int(sys.argv[1]), url = u, listitem = liz, isFolder = True)
    return ok

def add_dir2(name, url, mode, iconimage, fanart):
    u = sys.argv[0] + "?url=" + urllib.quote_plus(url) + "&mode=" + str(mode) + "&name=" + urllib.quote_plus(name) + "&iconimage=" + urllib.quote_plus(iconimage)
    ok = True
    liz = xbmcgui.ListItem(name, iconImage = "DefaultFolder.png", thumbnailImage = iconimage)
    fanart = fanart
    liz.setArt({'fanart': fanart})
    liz.setInfo(type="Video", infoLabels={ "Title": name, "plot": name })
    ok = xbmcplugin.addDirectoryItem(handle = int(sys.argv[1]), url = u, listitem = liz, isFolder = False)
    return ok

def main():
    if getSetting("enable_clear_images") == 'true':
        add_dir2('[COLOR indianred][B]Clear Younow Images[/B][/COLOR]', ClearImages, 2, refreshicon, fanart)
    if getSetting("enable_trending_users") == 'true':
        add_dir('[COLOR seagreen][B]Trending[B][/COLOR] [COLOR yellowgreen][B] Users[/B][/COLOR]', PageOne, 0, 1, 'None', 0, 2, icon, fanart)
    if getSetting("enable_trending_tags") == 'true':
        add_dir('[COLOR seagreen][B]Trending[B][/COLOR] [COLOR yellowgreen][B] Tags[/B][/COLOR]', Categories, 0, 1, 'None', 0, 2, icon, fanart)
    if getSetting("enable_settings") == 'true':
        add_dir2('[COLOR slategray]Settings[/COLOR]', Settings, 3, icon, fanart)
    setView('movies', 'menu_view')

def start(url,mode,top,pn,tag,v):
    if 'PageOne' in url:
        if mysettings.getSetting("auto_clear") == "true":
            clean_database(False)
        TheUrl = younow + str(top)
        buildMenu(TheUrl,url,mode,top,pn,tag,v)
    elif 'NextPage' in url:
        params = get_params()
        top = params['top']
        TheUrl = younow + top
        buildMenu(TheUrl,url,mode,top,pn,tag,v)
    elif 'Categories' in url:
        if mysettings.getSetting("auto_clear") == "true":
            clean_database(False)
        params = get_params()
        v = params['v']
        TheUrl = youtags
        getTags(TheUrl)
    elif 'Tagsz' in url:
        params = get_params()
        tag = params['tag']
        top = params['top']
        pn = params['pn']
        v = params['v']
        TheUrl = younowtags + top + '/' + 'tag=' + tag
        buildMenu(TheUrl,url,mode,top,pn,tag,v)
    elif 'ClearImages' in url:
        clean_database(showdialog=True)

def clean_database(showdialog=True):
    conn = sqlite3.connect(xbmc.translatePath("special://database/Textures13.db"))
    try:
        with conn:
            list = conn.execute("SELECT id, cachedurl FROM texture WHERE url LIKE '%%%s%%';" % ".younow.com")
            for row in list:
                conn.execute("DELETE FROM sizes WHERE idtexture LIKE '%s';" % row[0])
                try: os.remove(xbmc.translatePath("special://thumbnails/" + row[1]))
                except: pass
            conn.execute("DELETE FROM texture WHERE url LIKE '%%%s%%';" % ".younow.com")
            if showdialog:
                util.notifyClear('Finished','YouNow images cleared.')
    except:
        pass

def getTags(TheUrl):
    response = urllib2.urlopen(TheUrl)
    params = get_params()
    totalusers = 0
    if response and response.getcode() == 200:
        content = response.read()
        gets = util.extractAll(content, 'tag', 'isEp')
        for getit in gets:
            totalusers = totalusers + 1
            params['tag'] = util.extract(getit, '":"', '","viewers"')
            params['viewers'] = util.extract(getit, '"viewers":', ',"live"')
            params['live'] = util.extract(getit, '"live":', ',"')
            tag = params['tag']
            viewers = params['viewers']
            live = params['live']
            add_dir('Trending Tags #[COLOR greenyellow][B]' + str(tag) + '[/B][/COLOR]' + ' Live:(' + str(live) + ')', Tagsz, 0, 1, tag, 0, 2, icon, fanart)
        #util.endListing()
    else:
        util.showError(ADDON_ID, 'Could not open URL %s to create menu' % (url))
    setView('movies', 'menu_view')

def buildMenu(TheUrl,url,mode,top,pn,tag,v):
    params = get_params()
    totalusers = 0
    pn = params['pn']
    #v = params['v']
    #tag = params['tag']
    top = params['top']
    response = urllib2.urlopen(TheUrl)
    if response and response.getcode() == 200:
        content = response.read()
        #videos = util.extractAll(content, 'broadcastId', 'tags')
        videos = util.extractAll(content, '{"userId":"', '}')
        for video in videos:
            totalusers = totalusers + 1
            #top = int(top) + 50
            params = {'play':1}
            params['video'] = 'rtmp://pullstream.younow.8686c.com/live/Stream-' + util.extract(video, '"broadcastId":"', '","username":"')
            #params['image'] = 'https://ynassets.younow.com/broadcastdynamic/live/' + util.extract(video, '":"', '","username"') + '/' + util.extract(video, '":"', '","username"') + '.jpg'
            params['image'] = 'https://ynassets.younow.com/broadcastdynamic/live/' + util.extract(video, '"broadcastId":"', '","username":"') + '/' + util.extract(video, '"broadcastId":"', '","username":"') + '.jpg'
            params['title'] = util.extract(video, '","username":"', '\"')
            params['Page'] = url
            params['Type'] = mode
            params['top'] = top
            params['pn'] = pn
            params['tag'] = tag
            params['tg'] = util.extract(video, '"tags":["', '"],"broadcastId')
            params['v'] = util.extract(video, '","viewers":"', '","likes":"')
            params['likes'] = util.extract(video, '"likes":"', '","tags":')
            params['fans'] = util.extract(video, '"totalFans":', ',"position"')
            link = util.makeLink(params)
            util.addMenuItem2(params['title'], params['v'], params['tg'], params['likes'], params['fans'], link, params['image'], params['image'], False)
        #util.endListing()
    else:
        util.showError(ADDON_ID, 'Could not open URL %s to create menu' % (url))
    if totalusers >= 48 and tag == 'None':
        top = int(top) + 50
        pn = int(pn) + 1
        wp = int(pn) - 1
        add_dir('[COLOR slategray]P' + str(wp) + '[/COLOR] [COLOR greenyellow][B]Next Page[/B][/COLOR][COLOR olive][B]>>[/B][/COLOR][COLOR olivedrab][B]' + str(pn) + '[/B][/COLOR]', NextPage, top, pn, tag, v, 2, nexticon, fanart)
    else:
        if totalusers >= 48 and tag != 'None':
            top = int(top) + 50
            pn = int(pn) + 1
            wp = int(pn) - 1
            tag = params['tag']
            add_dir('[COLOR slategray]P' + str(wp) + ' [COLOR greenyellow][B]Next Page[/B][/COLOR][COLOR olive][B]>>[/B][/COLOR][COLOR olivedrab][B]' + str(pn) + '[/B][/COLOR]', Tagsz, top, pn, tag, v, 2, nexticon, fanart)
    if totalusers == 0:
        add_dir('[COLOR=darkkhaki]No Results:[/COLOR] ' + str(tag), Categories, 0, 1, tag, 0, 2, icon, fanart)
    setView('movies', 'thumb_view')

def settings():
    xbmcaddon.Addon().openSettings()

def test():
    params = get_params()
    url = None
    name = None
    mode = None
    iconimage = None
    top = '0'
    pn = '1'
    v = '0'
    tag = 'None'
    try:
        url = urllib.unquote_plus(params["url"])
    except:
        pass
    try:
        name = urllib.unquote_plus(params["name"])
    except:
        pass
    try:
        top = str(params["top"])
    except:
        pass
    try:
        pn = str(params["pn"])
    except:
        pass
    try:
        tag = str(params["tag"])
    except:
        pass
    try:
        v = str(params["v"])
    except:
        pass
    try:
        mode = int(params["mode"])
    except:
        pass
    try:
        iconimage = urllib.unquote_plus(params["iconimage"])
    except:
        pass
    if mode == None or url == None or len(url) < 1:
        main()
    elif mode == 1:
        searchUser(url,mode,top,pn,tag,v)
    elif mode == 2:
        start(url,mode,top,pn,tag,v)
    elif mode == 3:
        settings()
    elif mode == 4:
        searchTags(url,mode,top,pn,tag,v)



parameters = util.parseParameters()
if 'play' in parameters:
    params = get_params()
    mode = params['Type']
    url = params['Page']
    #totalusers = params['Num']
    #url = None
    #mode = None
    try:
	    url = urllib.unquote_plus(params["url"])
    except:
	    pass
    try:
	    mode = int(params["mode"])
    except:
	    pass
    playVideo(parameters)
else:
    test()



xbmcplugin.endOfDirectory(int(sys.argv[1]))