#!/usr/bin/env python
# -*- coding: utf-8 -*-

from        time             import      time
from        bs4              import      BeautifulSoup
import      time             as          reloj
import      urllib
import      os
import      random
import      re
import      constantes


############################################################################
####  CLASE QUE TENEMOS FUNCIONES CON ITERACION A LAS PAGINAS           ####
####  Y LOS ARCHIVOS                                                    ####
############################################################################

##  DEVOLVEMOS LA PAGINA PRINCIPAL PARSEADA
def devolverPaginaPartido(urlPagina):
    print (constantes.URL_BASKETBALL_REFERENCES + str(urlPagina('a'))[10:-43])
    return devolverPaginaParse(constantes.URL_BASKETBALL_REFERENCES + str(urlPagina('a'))[10:-43])

##  DEVOLVEMOS LA PAGINA PLAY BY PLAY PARSEADA
def devolverPaginaPlayByPlay(urlPagina):
    print (constantes.URL_BASKETBALL_REFERENCES_PLAYBYPLAY + str(urlPagina('a'))[21:-43])
    return devolverPaginaParse(constantes.URL_BASKETBALL_REFERENCES_PLAYBYPLAY + str(urlPagina('a'))[21:-43])

##  DEVOLVEMOS LA PAGINA PLAY BY PLAY PARSEADA DEL LOCAL
def devolverPaginaPlayByPlayLOCAL():
    return devolverPaginaParseLOCAL()

##  DEVOLVEMOS LA PAGINA DE CARTA DE TIRO PARSEADA
def devolverPaginaCartaTiro(urlPagina):
    print (constantes.URL_BASKETBALL_REFERENCES_CARTA_TIRO + str(urlPagina('a'))[21:-43])
    return devolverPaginaParse(constantes.URL_BASKETBALL_REFERENCES_CARTA_TIRO + str(urlPagina('a'))[21:-43])

##  DEVOLVEMOS LA PAGINA DE MAS MENOS PARSEADA
def devolverPaginaMasMenos(urlPagina):
    print (constantes.URL_BASKETBALL_REFERENCES_PLUS_MINUS + str(urlPagina('a'))[21:-43])
    return devolverPaginaParse(constantes.URL_BASKETBALL_REFERENCES_PLUS_MINUS + str(urlPagina('a'))[21:-43])

##  DEVOLVEMOS EL TIPO DE PARSEO QUE QUEREMOS PARA LA PAGINA
##  EN ESTE CASO DE TIPO HTML
def devolverPaginaParse(urlPagina):
    page = urllib.urlopen(urlPagina)
    return BeautifulSoup(page,"html.parser")

##  DEVOLVEMOS EL TIPO DE PARSEO QUE QUEREMOS PARA LA PAGINA
##  EN ESTE CASO DE TIPO HTML
def devolverPaginaParseLOCAL():
    page = open("partidoGolden.html","r")
    return BeautifulSoup(page,"html.parser")

##  CREAMOS LA CARPETA RAIZ DE LA BASE DE DATOS
def crearCarpetaRaiz():
    if not os.path.exists(constantes.RAIZ):
        os.makedirs(constantes.RAIZ)

##  CREAMOS LA CARPETA DE LA TAMPORADA SI NO EXISTE
def crearCarpetaTemporada(year):
    if not os.path.exists(constantes.RAIZ+'/' + str(year) + '-' + str(year + 1)):
        os.makedirs(constantes.RAIZ+'/' + str(year) + '-' + str(year + 1))


##  CREAMOS EL ARCHIVO TXT DONDE GUARDAREMOS LAS PAGINAS QUE NOS DESCARGAMOS
##  LO CREAMOS EN MODO 'a' POR SI SE NOS PARA LA DESCARGA Y TENEMOS QUE RETOMARLA
def crearArchivoTxtTemporada(year):
    return open(
        constantes.RAIZ+'/' + str(year) + '-' + str(year + 1) + '/sizePartidosTemporada' + str(year) + '-' + str(year + 1) + '.txt',
        'a')

## CREAMOS EL ARHCIVO JSON DONDE GUARDAREMOS LOS DATOS DE LOS PARTIDOS
def crearJsonPartido(year,url,numero):
    print (url)
    return open(
        constantes.RAIZ+'/' + str(year) + '-' + str(year + 1) + '/'+devolverNumeroPartido(numero)+ '_' + url + '.json',
        'w')
def crearJsonPartidosDiarios(year,url,numero):
    return open(
        'E:/TFG/python/eclipseWorkspace/NBAInfo/NBA/NBADATA/' + str(year) + '-' + str(year + 1) + '/'+devolverNumeroPartido(numero)+ '_' + url + '.json',
        'w')

## CREAMOS EL ARHCIVO JSON DONDE GUARDAREMOS LOS DATOS DE LOS PARTIDOS
def crearTxtId(year):
    return open(
        'E:/Programacion/pruebasMaven/NBAMongo/nuevosId.txt',
        'a')

## CREAMOS EL ARHCIVO JSON DONDE GUARDAREMOS LOS DATOS DE LOS PARTIDOS
def crearJsonPartidoUnico(year,url,numero):
    return open(
        'G:/TFG/python_modulos/venv/funciones/NBA_Scraping_TFG/'+constantes.RAIZ+'/' + str(year) + '-' + str(year + 1) + '/'+devolverNumeroPartido(numero)+ '_' + url + '.json',
        'w')

##  FUNCION RANDOM QUE NOS DEVUELVE UN NUMERO ENTRE EL LIMITE INFERIOR Y SUPERIOR
##  ESTO NOS PERMITE NO SATURAR EL SERVIDOR AL QUE ESTAMOS LLAMANDO Y ASI
##  EVITAR POSIBLES BANEOS
def parada():
    rn = random.randrange(constantes.SLEEP_LIMITE_INFERIOR, constantes.SLEEP_LIMITE_SUPERIOR)
    reloj.sleep(rn)


##  FUNCION PARA GUARDAR LOS DATOS EN UN ARCHIVO
def escribirEnDocumento(archivo,texto):
    archivo.write(str(texto))
    archivo.write('\n')

##  FUNCION QUE NOS DEVUELVE EL A�O DE LA TEMPORADA DEPENDIENDO DEL MES EN EL QUE ESTEMOS
#   EJ. SI ESTAMOS EN LA TEMPORADA 2003/2004, EN EL BUCLE DEL A�O ESTAMOS EN EL 2003
#   SI LOS MESE SON 10,11 O 12, DEVOLVEREMOS EL 2003
#   EN CAMBIO SI EL MES ESTA ENTRE 1,2,3,4,5,6 O 7 DEVOLVERA UN A�O MAS, EN ESTE CASO 2004
def devolverAnioCorrecto(year,mes):
    # if year == 2019 and (mes == 9 or mes == 10):
    #     return 2020
    #
    # if year == 2020:
    #     return year
    # else:
    if mes>9:
        return year
    else:
        return year+1

##  DEVOLEMOS EL NUMERO DE PARTIDO, SIEMPRE CON 4 DIGITOS
def devolverNumeroPartido(numero):
    if numero <10:
        return '000'+str(numero)
    elif numero <100:
        return '00'+str(numero)
    elif numero <1000:
        return '0'+str(numero)
    else:
        return str(numero)

##  CREAMOS EL ARCHIVO TXT DONDE GUARDAREMOS EL BOXSCORE DEL PATIDO
def crearArchivoBoxscorePartido(partido,url,numero):
    return open(constantes.RAIZ+'/' +partido.year +'-' +str(int(partido.year)+1) +'/'+devolverNumeroPartido(numero)+ '_' + url + ' Boxscore.txt','a')

def crearPDFBoxscorePartido(partido,t,d):
    c = canvas.Canvas(constantes.RAIZ+'/' +partido.year +'-' +str(int(partido.year)+1) +'/'+ partido.year +' ' + partido.mes +' ' + partido.dia +' ' + partido.equipoLocal.nombreAbreviado.upper() +' ' + partido.equipoVisitante.nombreAbreviado.upper() + ' Boxscore.pdf'
                      ,pagesize=landscape(A4))
    c.drawString(150,200,"Merry had a little lamb")
    c.save()
    
def esPartidoPlayIn(dia,mes,year):
    if year == 2021 and mes == 5 and (dia == 18 or dia == 19 or dia == 20 or dia == 21):
        return True
    if year == 2020 and mes == 8 and dia == 15:
        return True
    
    return False

def yearUbicacion(year):
    if year <2000:
        return 1
    return 0
def puntosNulos(puntos):
    if puntos is None:
        return 0
    return puntos