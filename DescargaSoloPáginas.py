#!/usr/bin/env python
# -*- coding: utf-8 -*-

############################################################################
####   IMPORTS                                                          ####
############################################################################

import json
import os
import random
import re
import sys
from time import time
import urllib.request

from bs4 import BeautifulSoup
import constantes
import controllerPartido as obj
import controllerStatNormales as statNormal
import funciones
import funcionesPartido
#import request
import time as reloj
#from PIL.Image import BOX


############################################################################
####   PERMITE CAMBIAR DEL ASCII PREDETERMINADO A OTRAS CODIFICACIONES  ####
############################################################################
#reload(sys)
#sys.setdefaultencoding('utf-8')

############################################################################
####   FUNCIONES                                                        ####
############################################################################

def escribirArchivoTxt(paginaDescargada):
    ##  ESCRIBIMOS EN EL DOCUMENTO DE DESCARGAS:
    #   LA P�GINA DESCARGADA
    #   UN INDICADOR QUE NOS DIRA EL TIEMPO QUE LLEVAMOS DESCARGANDO Y CUANTO TENEMOS QUE DESCONTAR
    funciones.escribirEnDocumento(descargarPaginaCompleta, paginaDescargada)
    funciones.escribirEnDocumento(descargarPaginaCompleta,
                                  '\n Tiempo descargando: ' + str(time() - tiempo) +
                                  ' - Restamos: ' + str(sumatorioRestaDeSegundos) + ' segundos\n')
    
def crearArchivoDescarga(partido,pagina,year):
    return open(
        constantes.RAIZ+'/' + str(year) + '-' + str(year + 1) + '/' + str(partido) + '.' +pagina+ '.html',
        'a')

def escribirEnDocumento(archivo,texto):
    archivo.write(str(texto))

############################################################################
####   CLASE PRINCIPAL                                                  ####
############################################################################

##  VARIABLE PARA TENER UN CONTADOR DEL NUMERO DE PARTIDOS
numeroPartidosRegistrados   =   0
##  VARIABLE QUE GUARDA LOS MESES QUE VAMOS A RECORRER
mesesTemporada = constantes.MESES_TEMPORADA

##  CREAMOS LA CARPETA RAIZ DONDE IREMOS GUARDANDO LAS TEMPORADAS SI NO EXISTE
##  SI EXISTE, NO HACE NADA0
funciones.crearCarpetaRaiz();


##  BUCLE PARA IR RECORRIENDO TEMPORADAS
for year in range(constantes.TEMPORADA_INICIAL,constantes.TEMPORADA_FINAL):

    ##  SE CREA LA CARPETA DE LA TEMPORADA, SI NO EXISTE
    funciones.crearCarpetaTemporada(year)

    ##  CREAMOS EL TXT PARA IR GUARDANDO DATOS
    #   Archivo donde iremos guardando todas las p�ginas en las que
    #   navegaremos para saber cuanto descargamos realmente.
    descargarPaginaCompleta = funciones.crearArchivoTxtTemporada(year)

    ##  VARIABLES DE TIEMPO PARA IR CONTROLANDO LO QUE TARDAMOS EN DESCARGAR
    #   RECOGEMOS LA HORA A LA QUE ESTAMOS EN ESTE MOMENTO
    tiempo = time()
    #   NUMERO DE SEGUNDOS QUE RETAREMOS POR LAS PARADAS AUTOMATICAS
    sumatorioRestaDeSegundos    =   0
    #   NUMERO DE PARTIDOS QUE VAMOS DESCARGANDO ESTA TEMPORADA
    numeroPartidosTemporada     =   0

    ##  BUCLE PARA IR RECORRIENDO LOS MESES DE LA TEMPORADA
    for mes in mesesTemporada:

        ##  BUCLE PARA IR RECCORIENDO LOS DIAS DEL MES
        for dia in range(1, 32):
            
            print (constantes.URL_BASKETBALL_REFERENCES_BOXSCORES +"?month=" + str(mes) +"&day=" + str(dia) +"&year=" + str(funciones.devolverAnioCorrecto(year,mes)))

            ##  RECOGEMOS LA P�GINA DEL DIA SE�ALADO
            partidosDelDia = funciones.devolverPaginaParse(
                constantes.URL_BASKETBALL_REFERENCES_BOXSCORES +
                "?month=" + str(mes) +
                "&day=" + str(dia) +
                "&year=" + str(funciones.devolverAnioCorrecto(year,mes)))

            ##  ESCIBIR EN TXT LA P�GINA DONDE ESTAN LOS PARTIDOS
            escribirArchivoTxt(partidosDelDia)
            
            
            ##  SACAMOS POR PANTALLA EL TITULO DE LA P�GINA EN LA QUE ESTAMOS NAVEGANDO
            if not partidosDelDia:
                print (partidosDelDia.title.text)

            ##  RECORREMOS, SI HAY, LOS ENLACES LOS PARTIDOS JUGADOS ESE D�A
            for matchDayUrl in partidosDelDia.findAll('td', {"class": "right gamelink"}):
                print (matchDayUrl)

                ##  SUMAMOS AL N�MERO DE PARTIDOS QUE VAMOS REGISTRANDO
                numeroPartidosRegistrados   += 1
                numeroPartidosTemporada     += 1


                ##  INSERTAMOS UNA MARCA DE TIEMPO  Y PARAMOS
                rn = random.randrange(1, 2)
                sumatorioRestaDeSegundos += rn
                reloj.sleep(rn)

                ##  RECOGEMOS Y PARSEAMOS LA P�GINA DEL PARTIDO
                #   ES LA P�GINA PRINCIPAL DEL PARTIDO
                boxScoreGame = funciones.devolverPaginaPartido(matchDayUrl)
                
                paginaBox = crearArchivoDescarga(numeroPartidosTemporada,'a',year)
                escribirEnDocumento(paginaBox,boxScoreGame)
                paginaBox.close()

                ##  ESCIBIR EN TXT LA PAGINA DEL PARTIDO EL BOXSCORE
                escribirArchivoTxt(boxScoreGame)

############################################################################
####  ENTRAMOS EN LA P�GINA PARA DESCARGAR LAS                          ####
####  ESTADISTICAS POR CUARTO DE CADA EQUIPO                            ####
############################################################################

                ##  INSERTAMOS UNA MARCA DE TIEMPO  Y PARAMOS
                rn = random.randrange(1, 2)
                sumatorioRestaDeSegundos += rn
                reloj.sleep(rn)

                print ("ENTRAMOS EN LA P�GINA DE JUGADA A JUGADA")

                ## RECOGEMOS Y PARSEAMOS LA PAGINA DE PLAY BY PLAY DEL PARTIDO
                playbyplay = funciones.devolverPaginaPlayByPlay(matchDayUrl)
                
                paginaPlayByPlay = crearArchivoDescarga(numeroPartidosTemporada,'b',year)
                escribirEnDocumento(paginaPlayByPlay,playbyplay)
                paginaPlayByPlay.close()

                
                ##  ESCIBIR EN TXT LA PAGINA DEL PARTIDO PLAY BY PLAY
                escribirArchivoTxt(playbyplay)

############################################################################
####  ENTRAMOS EN LA P�GINA PARA DESCARGAR LA                           ####
####  CARTA DE TIRO DE CADA JUGADOR DE CADA EQUIPO                      ####
############################################################################

                #  INSERTAMOS UNA MARCA DE TIEMPO  Y PARAMOS
                rn = random.randrange(1, 2)
                sumatorioRestaDeSegundos += rn
                reloj.sleep(rn)

                print ("ENTRAMOS EN LA P�GINA DE CARTA DE TIRO")

                ## RECOGEMOS Y PARSEAMO S LA PAGINA DE CARTA DE TIROS DEL PARTIDO
                shootChart = funciones.devolverPaginaCartaTiro(matchDayUrl)
                
                paginaShot = crearArchivoDescarga(numeroPartidosTemporada,'c',year)
                escribirEnDocumento(paginaShot,shootChart)
                paginaShot.close()


                ##  ESCIBIR EN TXT LA PAGINA DEL PARTIDO SHOOT CHART
                escribirArchivoTxt(shootChart)

############################################################################
####  ENTRAMOS EN LA P�GINA PARA DESCARGAR LOS                          ####
####  +/- POR CUARTO DE CADA JUGADOR EN CADA CUARTO                     ####
############################################################################

                ##  INSERTAMOS UNA MARCA DE TIEMPO  Y PARAMOS
                rn = random.randrange(1, 2)
                sumatorioRestaDeSegundos += rn
                reloj.sleep(rn)

                print ("ENTRAMOS EN LA P�GINA DE +/-")

                ## RECOGEMOS Y PARSEAMOS LA PAGINA DE MAS MENOS DEL PARTIDO
                masMenosPagina = funciones.devolverPaginaMasMenos(matchDayUrl)
                
                
                paginaMasMenos = crearArchivoDescarga(numeroPartidosTemporada,'d',year)
                escribirEnDocumento(paginaMasMenos,masMenosPagina)
                paginaMasMenos.close()

                ##  ESCIBIR EN TXT LA PAGINA DEL PARTIDO MAS/MENOS
                escribirArchivoTxt(masMenosPagina)

                print ("Fin del partido partido")
                print ("********************************************************")
                print (" ")
