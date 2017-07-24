# -*- coding: utf-8 -*-
# ------------------------------------------------------------
# Canal (ultrapeliculashd) por Hernan_Ar_c
# ------------------------------------------------------------

import urlparse,urllib2,urllib,re
import os, sys

from core import logger
from core import config
from core import scrapertools
from core.item import Item
from core import servertools
from core import httptools
from core import tmdb

host = 'http://www.ultrapeliculashd.com'

tgenero = {"ACCIÓN":"https://s32.postimg.org/4hp7gwh9x/accion.png,",
           "ANIMACIÓN": "https://s32.postimg.org/rbo1kypj9/animacion.png",
           "AVENTURA": "https://s32.postimg.org/whwh56is5/aventura.png",
           "CIENCIA FICCIÓN": "https://s32.postimg.org/6hp3tsxsl/ciencia_ficcion.png",
           "COMEDIA":"https://s32.postimg.org/q7g2qs90l/comedia.png",
           "CRIMEN": "https://s14.postimg.org/5lez1j1gx/crimen.png",
           "DRAMA": "https://s32.postimg.org/e6z83sqzp/drama.png",
           "ESTRENOS": "https://s12.postimg.org/4zj0rbun1/estrenos.png",
           "FAMILIA": "https://s28.postimg.org/4wwzkt2f1/familiar.png",
           "FANTASÍA": "https://s32.postimg.org/pklrf01id/fantasia.png",
           "GUERRA": "https://s29.postimg.org/vqgjmozzr/guerra.png",
           "INFANTIL": "https://s32.postimg.org/i53zwwgsl/infantil.png",
           "MISTERIO": "https://s4.postimg.org/kd48bcxe5/misterio.png",
           "ROMANCE": "https://s31.postimg.org/y7vai8dln/romance.png",
           "SUSPENSO":"https://s31.postimg.org/kb629gscb/suspenso.png",
           "TERROR":"https://s32.postimg.org/ca25xg0ed/terror.png"
           }

thumbletras = {'#': 'https://s32.postimg.org/drojt686d/image.png',
               'a': 'https://s32.postimg.org/llp5ekfz9/image.png',
               'b': 'https://s32.postimg.org/y1qgm1yp1/image.png',
               'c': 'https://s32.postimg.org/vlon87gmd/image.png',
               'd': 'https://s32.postimg.org/3zlvnix9h/image.png',
               'e': 'https://s32.postimg.org/bgv32qmsl/image.png',
               'f': 'https://s32.postimg.org/y6u7vq605/image.png',
               'g': 'https://s32.postimg.org/9237ib6jp/image.png',
               'h': 'https://s32.postimg.org/812yt6pk5/image.png',
               'i': 'https://s32.postimg.org/6nbbxvqat/image.png',
               'j': 'https://s32.postimg.org/axpztgvdx/image.png',
               'k': 'https://s32.postimg.org/976yrzdut/image.png',
               'l': 'https://s32.postimg.org/fmal2e9yd/image.png',
               'm': 'https://s32.postimg.org/m19lz2go5/image.png',
               'n': 'https://s32.postimg.org/b2ycgvs2t/image.png',
               'o': 'https://s32.postimg.org/c6igsucpx/image.png',
               'p': 'https://s32.postimg.org/jnro82291/image.png',
               'q': 'https://s32.postimg.org/ve5lpfv1h/image.png',
               'r': 'https://s32.postimg.org/nmovqvqw5/image.png',
               's': 'https://s32.postimg.org/zd2t89jol/image.png',
               't': 'https://s32.postimg.org/wk9lo8jc5/image.png',
               'u': 'https://s32.postimg.org/w8s5bh2w5/image.png',
               'v': 'https://s32.postimg.org/e7dlrey91/image.png',
               'w': 'https://s32.postimg.org/fnp49k15x/image.png',
               'x': 'https://s32.postimg.org/dkep1w1d1/image.png',
               'y': 'https://s32.postimg.org/um7j3zg85/image.png',
               'z': 'https://s32.postimg.org/jb4vfm9d1/image.png'
               }


tcalidad = {'1080P':'https://s24.postimg.org/vto15vajp/hd1080.png','720P':'https://s28.postimg.org/wllbt2kgd/hd720.png',"HD":"https://s30.postimg.org/6vxtqu9sx/image.png"}

def mainlist(item):
    logger.info()

    itemlist = []
    
    itemlist.append( item.clone (title="Todas",
                                 action="lista",
                                 thumbnail='https://s12.postimg.org/iygbg8ip9/todas.png',
                                 fanart='https://s12.postimg.org/iygbg8ip9/todas.png',
                                 url = host+'/movies/'
                                 ))

    itemlist.append( item.clone (title="Generos",
                                 action="generos",
                                 url=host,
                                 thumbnail='https://s31.postimg.org/szbr0gmkb/generos.png',
                                 fanart='https://s31.postimg.org/szbr0gmkb/generos.png'
                                 ))
    
    itemlist.append( item.clone (title="Alfabetico",
                                 action="seccion",
                                 url=host,
                                 thumbnail='https://s31.postimg.org/c3bm9cnl7/a_z.png',
                                 fanart='https://s31.postimg.org/c3bm9cnl7/a_z.png',
                                 extra = 'alfabetico'
                                 ))

    itemlist.append( item.clone (title="Buscar",
                                 action="search",
                                 url=host+'/?s=',
                                 thumbnail='https://s31.postimg.org/qose4p13f/Buscar.png',
                                 fanart='https://s31.postimg.org/qose4p13f/Buscar.png'
                                 ))
    

    return itemlist

def lista (item):
    logger.info ()
	
    itemlist = []
    data = httptools.downloadpage(item.url).data
    data = re.sub(r'"|\n|\r|\t|&nbsp;|<br>|\s{2,}', "", data)
    if item.extra != 'buscar':
        patron = '<article id=post-.*? class=item movies><div class=poster><a href=(.*?)><img src=(.*?) '
        patron += 'alt=(.*?)>.*?quality>.*?<.*?<\/h3><span>(.*?)<\/span>'
    else:
        patron = '<article><div class=image>.*?<a href=(.*?)\/><img src=(.*?) alt=(.*?) \/>.*?year>(.*?)<\/span>'
    matches = re.compile(patron,re.DOTALL).findall(data)

    for scrapedurl, scrapedthumbnail, scrapedtitle, scrapedyear in matches:
        url = scrapedurl
        thumbnail = scrapedthumbnail
        contentTitle = re.sub(r'\d{4}','',scrapedtitle)
        contentTitle = contentTitle.replace('|','')
        contentTitle = contentTitle.strip(' ')
        title = scrapertools.decodeHtmlentities(contentTitle)
        year = scrapedyear
        fanart =''
        itemlist.append( Item(channel=item.channel, action="findvideos" , title=title , fulltitle=item.title, url=url, thumbnail=thumbnail, fanart = fanart, contentTitle=contentTitle, infoLabels={'year':year}))
    tmdb.set_infoLabels_itemlist(itemlist, seekTmdb =True)       
    #Paginacion

    if itemlist !=[]:
        actual_page_url = item.url
        next_page = scrapertools.find_single_match(data,'<div class=pag_b><a href=(.*?) >Siguiente<\/a>')
        import inspect
        if next_page !='':
           itemlist.append(Item(channel = item.channel, action = "lista", title = 'Siguiente >>>', url = next_page, thumbnail='https://s32.postimg.org/4zppxf5j9/siguiente.png'))
    return itemlist

def generos(item):
    
    logger.info()
    itemlist = []
    data = httptools.downloadpage(item.url).data
    data = re.sub(r'"|\n|\r|\t|&nbsp;|<br>|\s{2,}', "", data)
    patron = '<li class=cat-item cat-item-.*?><a href=(.*?) >(.*?)<\/a> <i>(.*?)<\/i><\/li>'
    matches = re.compile(patron,re.DOTALL).findall(data)

    for scrapedurl, scrapedtitle, cantidad in matches:
        thumbnail =''
        fanart= ''
        if scrapedtitle in tgenero:
            thumbnail = tgenero[scrapedtitle]
        title = scrapedtitle+' ('+cantidad+')'
        url = scrapedurl
        if scrapedtitle not in ['PRÓXIMAMENTE', 'EN CINE']:
            itemlist.append(item.clone(action="lista",
                                       title=title,
                                       fulltitle=item.title,
                                       url=url,
                                       thumbnail=thumbnail,
                                       fanart = fanart
                                       ))
    return itemlist

def seccion(item):
    
    logger.info()
    itemlist = []
    data = httptools.downloadpage(item.url).data
    data = re.sub(r'"|\n|\r|\t|&nbsp;|<br>|\s{2,}', "", data)
    if item.extra == 'year':
        patron = '<li><a href=(.*?\/fecha-estreno.*?)>(.*?)<\/a>'
    else:
        patron = '<li><a href=(.*?) >(.*?)<\/a><\/li>'
    matches = re.compile(patron,re.DOTALL).findall(data)

    for scrapedurl, scrapedtitle in matches:
        thumbnail =''
        if scrapedtitle.lower() in thumbletras:
            thumbnail = thumbletras[scrapedtitle.lower()]
        fanart= ''
        title = scrapedtitle
        url = scrapedurl

        itemlist.append( Item(channel=item.channel, action="lista" , title=title , fulltitle=item.title, url=url, thumbnail=thumbnail, fanart = fanart))
    return itemlist

def findvideos(item):
    logger.info()
    itemlist=[]
    data = httptools.downloadpage(item.url).data
    data = re.sub(r'"|\n|\r|\t|&nbsp;|<br>|\s{2,}', "", data)

    patron = '<iframe class=metaframe rptss src=(.*?) frameborder=0 allowfullscreen><\/iframe>'
    matches = matches = re.compile(patron,re.DOTALL).findall(data)
    for videoitem in matches:
        itemlist.extend(servertools.find_video_items(data=videoitem))

    for videoitem in itemlist:
        videoitem.channel = item.channel
        videoitem.action ='play'
        videoitem.thumbnail = servertools.guess_server_thumbnail(videoitem.server)
        videoitem.infoLabels = item.infoLabels
        videoitem.title = item.contentTitle+' ('+videoitem.server+')'
        if 'youtube' in videoitem.url:
            videoitem.title = '[COLOR orange]Trailer en Youtube[/COLOR]'

    if config.get_library_support() and len(itemlist) > 0 and item.extra !='findvideos':
        itemlist.append(Item(channel=item.channel, title='[COLOR yellow]Añadir esta pelicula a la biblioteca[/COLOR]', url=item.url,
                             action="add_pelicula_to_library", extra="findvideos", contentTitle = item.contentTitle))
    return itemlist

def search(item,texto):
    logger.info()
    texto = texto.replace(" ","+")
    item.url = item.url+texto
    try:
        if texto != '':
            item.extra = 'buscar'
            return lista(item)
        else:
            return []
    except:
        import sys
        for line in sys.exc_info():
            logger.error("%s" % line)
        return []


def newest(categoria):
  logger.info()
  itemlist = []
  item = Item()
  item.extra = 'estrenos/'
  try:
      if categoria == 'peliculas':
          item.url = host+'/category/estrenos/'
          
      elif categoria == 'infantiles':
          item.url = host+'/category/infantil/'

      itemlist = lista(item)
      if itemlist[-1].title == 'Siguiente >>>':
              itemlist.pop()
  except:
      import sys
      for line in sys.exc_info():
          logger.error("{0}".format(line))
      return []

  return itemlist


