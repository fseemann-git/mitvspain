# -*- coding: utf-8 -*-
#------------------------------------------------------------
# mitvspain - XBMC Plugin
# Canal para trailers de ecartelera
# 
#------------------------------------------------------------

import re
import urlparse

from core import config
from core import logger
from core import scrapertools
from core.item import Item

DEBUG = config.get_setting("debug")

def mainlist(item):
    logger.info("mitvspain.channels.ecarteleratrailers mainlist")
    itemlist=[]

    if item.url=="":
        item.url="http://www.ecartelera.com/videos/"

    # ------------------------------------------------------
    # Descarga la página
    # ------------------------------------------------------
    data = scrapertools.cachePage(item.url)
    #logger.info(data)

    # ------------------------------------------------------
    # Extrae las películas
    # ------------------------------------------------------
    patron  = '<div class="viditem"[^<]+'
    patron += '<div class="fimg"><a href="([^"]+)"><img alt="([^"]+)" src="([^"]+)"/><p class="length">([^<]+)</p></a></div[^<]+'
    patron += '<div class="fcnt"[^<]+'
    patron += '<h4><a[^<]+</a></h4[^<]+'
    patron += '<p class="desc">([^<]+)</p>'

    matches = re.compile(patron,re.DOTALL).findall(data)
    if DEBUG: scrapertools.printMatches(matches)

    for scrapedurl,scrapedtitle,scrapedthumbnail,duration,scrapedplot in matches:

        title = scrapedtitle + " ("+duration+")"
        url = scrapedurl
        thumbnail = scrapedthumbnail
        plot = scrapedplot.strip()

        if (DEBUG): logger.info("title=["+title+"], url=["+url+"], thumbnail=["+thumbnail+"]")
        itemlist.append( Item(channel=item.channel, action="play" , title=title , url=url, thumbnail=thumbnail, fanart=thumbnail, plot=plot, server="directo", folder=False))

    # ------------------------------------------------------
    # Extrae la página siguiente
    # ------------------------------------------------------
    patron = '<a href="([^"]+)">Siguiente</a>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    if DEBUG:
        scrapertools.printMatches(matches)

    for match in matches:
        scrapedtitle = "Pagina siguiente"
        scrapedurl = match
        scrapedthumbnail = ""
        scrapeddescription = ""

        # Añade al listado de XBMC
        itemlist.append( Item(channel=item.channel, action="mainlist" , title=scrapedtitle , url=scrapedurl, thumbnail=scrapedthumbnail, plot=scrapedplot, server="directo", folder=True, viewmode="movie_with_plot"))

    return itemlist

# Reproducir un vídeo
def play(item):
    logger.info("mitvspain.channels.ecarteleratrailers play")
    itemlist=[]
    # Descarga la página
    data = scrapertools.cachePage(item.url)
    logger.info(data)

    # Extrae las películas
    patron  = '<source src="([^"]+)"'
    matches = re.compile(patron,re.DOTALL).findall(data)

    if len(matches)>0:
        url = urlparse.urljoin(item.url,matches[0])
        logger.info("mitvspain.channels.ecarteleratrailers url="+url)
        itemlist.append( Item(channel=item.channel, action="play" , title=item.title , url=url, thumbnail=item.thumbnail, plot=item.plot, server="directo", folder=False))

    return itemlist
