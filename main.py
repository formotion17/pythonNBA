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
import urllib

from bs4 import BeautifulSoup
import constantes
import controllerPartido as obj
import controllerStatNormales as statNormal
import funciones
import funcionesPartido
import request
import time as reloj


############################################################################
####   PERMITE CAMBIAR DEL ASCII PREDETERMINADO A OTRAS CODIFICACIONES  ####
############################################################################
reload(sys)
sys.setdefaultencoding('utf-8')

############################################################################
####   FUNCIONES                                                        ####
############################################################################

def escribirArchivoTxt(paginaDescargada):
    ##  ESCRIBIMOS EN EL DOCUMENTO DE DESCARGAS:
    #   LA PÁGINA DESCARGADA
    #   UN INDICADOR QUE NOS DIRA EL TIEMPO QUE LLEVAMOS DESCARGANDO Y CUANTO TENEMOS QUE DESCONTAR
    funciones.escribirEnDocumento(descargarPaginaCompleta, paginaDescargada)
    funciones.escribirEnDocumento(descargarPaginaCompleta,
                                  '\n Tiempo descargando: ' + str(time() - tiempo) +
                                  ' - Restamos: ' + str(sumatorioRestaDeSegundos) + ' segundos\n')

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
    #   Archivo donde iremos guardando todas las páginas en las que
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
            
            ##  INSERTAMOS UNA MARCA DE TIEMPO  Y PARAMOS
            rn = random.randrange(2, 6)
            sumatorioRestaDeSegundos += rn
            reloj.sleep(rn)

            ##  RECOGEMOS LA PÁGINA DEL DIA SEÑALADO
            partidosDelDia = funciones.devolverPaginaParse(
                constantes.URL_BASKETBALL_REFERENCES_BOXSCORES +
                "?month=" + str(mes) +
                "&day=" + str(dia) +
                "&year=" + str(funciones.devolverAnioCorrecto(year,mes)))
            
            print partidosDelDia

            ##  ESCIBIR EN TXT LA PÁGINA DONDE ESTAN LOS PARTIDOS
            escribirArchivoTxt(partidosDelDia)
            
            ##  SACAMOS POR PANTALLA EL TITULO DE LA PÁGINA EN LA QUE ESTAMOS NAVEGANDO
            if not partidosDelDia:
                print (partidosDelDia.title.text)

            ##  RECORREMOS, SI HAY, LOS ENLACES LOS PARTIDOS JUGADOS ESE DÍA
            for matchDayUrl in partidosDelDia.findAll('td', {"class": "right gamelink"}):

                ##  SUMAMOS AL NÚMERO DE PARTIDOS QUE VAMOS REGISTRANDO
                numeroPartidosRegistrados   += 1
                numeroPartidosTemporada     += 1


                ##  INSERTAMOS UNA MARCA DE TIEMPO  Y PARAMOS
                rn = random.randrange(2, 6)
                sumatorioRestaDeSegundos += rn
                reloj.sleep(rn)

                ##  CREAMOS EL ARCHIVO DEL PARTIDO DONDE GUARDAREMOS LOS DATOS DEL PARTIDO
                partidoUnico = funciones.crearJsonPartido(year,str(matchDayUrl('a'))[21:-48],numeroPartidosTemporada)

                ##  RECOGEMOS Y PARSEAMOS LA PÁGINA DEL PARTIDO
                #   ES LA PÁGINA PRINCIPAL DEL PARTIDO
                boxScoreGame = funciones.devolverPaginaPartido(matchDayUrl)


                ##  SACAMOS POR PANTALLA EL TITULO DE LA PÁGINA EN LA QUE ESTAMOS NAVEGANDO
                print boxScoreGame.title.text
                print "Partidos de temporada: "+str(numeroPartidosTemporada)+". Número de partidos total descargados: "+str(numeroPartidosRegistrados)

                ##  ESCIBIR EN TXT LA PAGINA DEL PARTIDO EL BOXSCORE
                escribirArchivoTxt(boxScoreGame)

############################################################################
####  ESTAMOS EN LA PÁGINA PRINCIPAL DEL BOXSCORE                       ####
############################################################################
                print "ENTRAMOS EN LA PÁGINA PRINCIPAL DEL BOXSCORE"

                ##  CREAMOS LA VARIABLE DE PARTIDO
                partido=obj.partido()

                ##  RECOGEMOS LA ASISTENCIA DE PUBLICO DEL PARTIDO
                partido.asistencia = funcionesPartido.devolverAsistenciaPartido(boxScoreGame)

                ##  RELLENAMOS FECHA, ESTADIO Y UBICACIÓN EN LA VARIABLE PARTIDO
                partido.rellenarFechaUbicacion(
                    str(dia),
                    str(mes),
                    str(funciones.devolverAnioCorrecto(year,mes)),
                    funcionesPartido.horarioUbicacion(str(boxScoreGame.find_all("div", class_="scorebox_meta"))),
                    funcionesPartido.devolverAsistenciaPartido(boxScoreGame)
                )

                ##  NAVEGAMOS POR LA PÁGINA RECOGIENDO DIFERENTES COSAS
                for stats in boxScoreGame.findAll('div', {"class": "scorebox"}):

                    ##  RECOGEMOS:
                    #   TANTEO LOCAL Y VISITANTE
                    #   BALANCE DE VITORIAS Y DERROTAS  DE LOCAL Y VISITANTE
                    contador = 0
                    playIn = funciones.esPartidoPlayIn(dia,mes,funciones.devolverAnioCorrecto(year,mes))
                    if playIn:
                        print "ES PARTIDO DE PLAY IN"
                        for resultado in stats.findAll('div'):
                            ##  RECOGEMOS EL TANTEO DEL EQUIPO VISITANTE
                            if contador == 4:
                                partido.equipoVisitante.tanteo = str(resultado.text)
                            ##  RECOGEMOS EL TANTEO DEL EQUIPO LOCAL
                            if contador == 8:
                                partido.equipoLocal.tanteo = str(resultado.text)
    
                            if contador > 8:
                                break
                            contador = contador + 1

                    else:
                        for resultado in stats.findAll('div'):
                            ##  RECOGEMOS EL TANTEO DEL EQUIPO VISITANTE
                            if contador == 4:
                                partido.equipoVisitante.tanteo = str(resultado.text)
    
                            ##  RECOGEMOS EL BALANCE DE VICTORIAS - DERROTAS DEL EQUIPO VISITANTE
                            if contador == 5:
                                partidosJugadosVisitante = str(resultado.text).split('-')
                                partido.equipoVisitante.victorias = partidosJugadosVisitante[0]
                                partido.equipoVisitante.derrotas = partidosJugadosVisitante[1]
    
                            ##  RECOGEMOS EL TANTEO DEL EQUIPO LOCAL
                            if contador == 11:
                                partido.equipoLocal.tanteo = str(resultado.text)
    
                            ##  RECOGEMOS EL BALANCE DE VICTORIAS - DERROTAS DEL EQUIPO LOCAL
                            if contador == 12:
                                partidosJugadorLocal = str(resultado.text).split('-')
                                partido.equipoLocal.victorias=partidosJugadorLocal[0]
                                partido.equipoLocal.derrotas = partidosJugadorLocal[1]
    
                            if contador > 12:
                                break
                            contador = contador + 1

                    ##  RECOGEMOS EL NOMBRE DE LOS EQUIPOS VISITANTE Y LOCAL
                    teams = []
                    nombre = stats('a')
                    for nombre in stats.findAll('strong'):
                        teams.append(str(nombre.find('a').text))
                    partido.equipoVisitante.nombre = teams[0]
                    partido.equipoLocal.nombre = teams[1]

                    ##  RECOGEMOS EL NOMBRE ABREVIADO DE LOS EQUIPOS VISITANTE Y LOCAL
                    abre=[]
                    equipos = stats('strong')
                    partido.equipoLocal.nombreAbreviado = str(equipos[1])[25:28].lower()
                    partido.equipoVisitante.nombreAbreviado = str(equipos[0])[25:28].lower()

                    ##  RECOGEMOS SI ES UN PARTIDO DE PLAYOFF O NO
                    #   DESDE EL MES 10 11 12 1 2 3 NUNCA VA A SER PLAYOFF
                    #   SI ESTAMOS EN MESES 4 5 6 7 Y SI EL NÚMERO ES MENOR O IGUAL A 7, ESTAMOS EN PLAYOFF
                    #   SI ESTAMOS EN EL AÑO 2020 LOS PLAYOFF VAN DEL 17 AGOSTO AL 11 DE OCTUBRE
                    # if year ==2020:
                    #     if mes >3 and mes <12:
                    #         if int(partido.equipoLocal.victorias) + int(partido.equipoLocal.derrotas) <= 7:
                    #             partido.playOff = True
                    #         else:
                    #             partido.playOff = False
                    #     else:
                    #         partido.playOff = False
                    # else:
                    if mes > 3 and mes < 10:
                        if playIn:
                            partido.playOff = False
                        else:
                            if int(partido.equipoLocal.victorias) + int(partido.equipoLocal.derrotas) <=7:
                                partido.playOff = True
                            else:
                                partido.playOff = False
                    else:
                        partido.playOff = False

                    print partido.equipoVisitante.nombre + " "+str(partido.equipoVisitante.tanteo) + " - " + str(partido.equipoLocal.tanteo) + " " +partido.equipoLocal.nombre
                    print "Patido de PlayOff: "+str(partido.playOff)

                    ## RECOGEMOS LAS ESTADISTICAS NORMALES  DE LOS JUGADORES DEL PARTIDO DE LA PAGINA DE BOXSCORE
                    partido.equipoLocal = funcionesPartido.devolverStadisticasNormalesJugadores(partido.equipoLocal,boxScoreGame)
                    partido.equipoVisitante = funcionesPartido.devolverStadisticasNormalesJugadores(partido.equipoVisitante,boxScoreGame)

                    ## RECOGEMOS LAS ESTADISTICAS AVANZADAS  DE LOS JUGADORES DEL PARTIDO DE LA PAGINA DE BOXSCORE
                    partido.equipoLocal = funcionesPartido.devolverStadisticasAvanzadas(partido.equipoLocal,boxScoreGame,partido.equipoLocal.jugadores)
                    partido.equipoVisitante = funcionesPartido.devolverStadisticasAvanzadas(partido.equipoVisitante, boxScoreGame,partido.equipoVisitante.jugadores)


############################################################################
####  ENTRAMOS EN LA PÁGINA PARA DESCARGAR LAS                          ####
####  ESTADISTICAS POR CUARTO DE CADA EQUIPO                            ####
############################################################################

                ##  INSERTAMOS UNA MARCA DE TIEMPO  Y PARAMOS
                rn = random.randrange(2, 6)
                sumatorioRestaDeSegundos += rn
                reloj.sleep(rn)

                print "ENTRAMOS EN LA PÁGINA DE JUGADA A JUGADA"

                ## RECOGEMOS Y PARSEAMOS LA PAGINA DE PLAY BY PLAY DEL PARTIDO
                playbyplay = funciones.devolverPaginaPlayByPlay(matchDayUrl)
                ## Utilizamos esta función si recogemos el partido desde local
                #playbyplay = funciones.devolverPaginaPlayByPlayLOCAL()

                ##  ESCIBIR EN TXT LA PAGINA DEL PARTIDO PLAY BY PLAY
                escribirArchivoTxt(playbyplay)

                ##  RECOGEMOS LAS ESTADISTICAS POR CUARTO DE CADA JUGADOR
                partido = funcionesPartido.devolverPlayByPlayJugadores(partido,playbyplay,str(matchDayUrl('a'))[21:-17],numeroPartidosTemporada)

                ##  RECOGEMOS DATOS ESTADISTICOS DE CADA EQUIPO
                partido = funcionesPartido.recogerLideratosPartido(str(playbyplay),partido)


############################################################################
####  ENTRAMOS EN LA PÁGINA PARA DESCARGAR LA                           ####
####  CARTA DE TIRO DE CADA JUGADOR DE CADA EQUIPO                      ####
############################################################################

                #  INSERTAMOS UNA MARCA DE TIEMPO  Y PARAMOS
                rn = random.randrange(2, 6)
                sumatorioRestaDeSegundos += rn
                reloj.sleep(rn)

                print "ENTRAMOS EN LA PÁGINA DE CARTA DE TIRO"

                ## RECOGEMOS Y PARSEAMO S LA PAGINA DE CARTA DE TIROS DEL PARTIDO
                shootChart = funciones.devolverPaginaCartaTiro(matchDayUrl)

                ##  ESCIBIR EN TXT LA PAGINA DEL PARTIDO SHOOT CHART
                escribirArchivoTxt(shootChart)

                ##  RECOGEMOS LA CARTA DE TIROS DEL EQUIPO LOCAL
                partido.equipoLocal = funcionesPartido.devolverPosicionTirosJugadores(partido.equipoLocal,shootChart)
                ##  RECOGEMOS LA CARTA DE TIROS DEL EQUIPO VISITANTE
                partido.equipoVisitante = funcionesPartido.devolverPosicionTirosJugadores(partido.equipoVisitante,shootChart)

############################################################################
####  ENTRAMOS EN LA PÁGINA PARA DESCARGAR LOS                          ####
####  +/- POR CUARTO DE CADA JUGADOR EN CADA CUARTO                     ####
############################################################################

                ##  INSERTAMOS UNA MARCA DE TIEMPO  Y PARAMOS
                rn = random.randrange(2, 6)
                sumatorioRestaDeSegundos += rn
                reloj.sleep(rn)

                print "ENTRAMOS EN LA PÁGINA DE +/-"

                ## RECOGEMOS Y PARSEAMOS LA PAGINA DE MAS MENOS DEL PARTIDO
                masMenosPagina = funciones.devolverPaginaMasMenos(matchDayUrl)

                ##  ESCIBIR EN TXT LA PAGINA DEL PARTIDO MAS/MENOS
                escribirArchivoTxt(masMenosPagina)

                ##  RECOGEMOS EL +/- DE CADA JUGADOR DEL PARTIDO
                partido = funcionesPartido.devolverMasMenosJugadores(partido,masMenosPagina)

                ## RECOGEMOS TANTEOS DE CADA CUARTO DE CADA EQUIPO
                partido = funcionesPartido.recogerCuartosPartido(masMenosPagina,year,partido)

############################################################################
####  COMPLETAMOS LAS ESTADISTICAS COMPLETAS DE CADA JUGADOR Y EQUIPO   ####
############################################################################

                ##  COMPLETAMOS ESTADISTICAS NORMALES
                partido = funcionesPartido.completarFullBoxscoreJugador(partido)
                partido = funcionesPartido.completarFullBoxScoreLocal(partido)
                partido = funcionesPartido.completarFullBoxScoreVisitante(partido)

                ##  COMPLETAMOS ESTADISTICAS AVANZADAS
                partido.equipoVisitante=funcionesPartido.completarEstadisticaAvanzada(partido.equipoVisitante)
                partido.equipoLocal = funcionesPartido.completarEstadisticaAvanzada(partido.equipoLocal)

############################################################################
####  GUARDAMOS EL PARTIDO EN UN ARCHIVO JSON                           ####
############################################################################

                ##  GUARDAMOS LOS DATOS DEL PARTIDO EN EL ARCHIVO JSON
                partidoUnico.write(partido.toJSON())
                partidoUnico.close()

                print "Fin del partido partido"
                print "********************************************************"
                print " "
