#!/usr/bin/env python
# -*- coding: utf-8 -*-

############################################################################
####   IMPORTS                                                          ####
############################################################################
import urllib
import os
import random
import re
import sys
import time                as          reloj
from time import time
import funciones
import funcionesPartido
import constantes
import controllerPartido   as          obj
import controllerStatNormales   as     statNormal
import json
from datetime import date

############################################################################
####   PERMITE CAMBIAR DEL ASCII PREDETERMINADO A OTRAS CODIFICACIONES  ####
############################################################################
reload(sys)
sys.setdefaultencoding('utf-8')

############################################################################
####   CLASE PRINCIPAL                                                  ####
############################################################################

##  OBTENEMOS LA FECHA DE HOY - DIA MES AÑO
today = date.today()
dia = today.day-1
mes = today.month
year = today.year-1

##  VARIABLE PARA TENER UN CONTADOR DEL NUMERO DE PARTIDOS
numeroPartidosRegistrados = 0

##  SE CREA LA CARPETA DE LA TEMPORADA, SI NO EXISTE
#funciones.crearCarpetaTemporada(year)

##  VARIABLES DE TIEMPO PARA IR CONTROLANDO LO QUE TARDAMOS EN DESCARGAR
#   RECOGEMOS LA HORA A LA QUE ESTAMOS EN ESTE MOMENTO
tiempo = time()

#   NUMERO DE PARTIDOS QUE VAMOS DESCARGANDO ESTA TEMPORADA
cpt = sum([len(files) for r, d, files in os.walk('E:/TFG/python/eclipseWorkspace/NBAInfo/NBA/NBADATA/2021-2022/Insertados')])

numeroPartidosTemporada = cpt


##  RECOGEMOS LA PÁGINA DEL DIA SEÑALADO
partidosDelDia = funciones.devolverPaginaParse(
    constantes.URL_BASKETBALL_REFERENCES_BOXSCORES +
    "?month=" + str(mes) +
    "&day=" + str(dia) +
    "&year=" + str(funciones.devolverAnioCorrecto(year,mes)))

##  SACAMOS POR PANTALLA EL TITULO DE LA PÁGINA EN LA QUE ESTAMOS NAVEGANDO
print (partidosDelDia.title.text)

##  RECORREMOS, SI HAY, LOS ENLACES LOS PARTIDOS JUGADOS ESE DÍA
for matchDayUrl in partidosDelDia.findAll('td', {"class": "right gamelink"}):

    ##  SUMAMOS AL NÚMERO DE PARTIDOS QUE VAMOS REGISTRANDO
    numeroPartidosRegistrados += 1
    numeroPartidosTemporada += 1

    ##  INSERTAMOS UNA MARCA DE TIEMPO  Y PARAMOS
    rn = random.randrange(2, 6)
    reloj.sleep(rn)

    ##  CREAMOS EL ARCHIVO DEL PARTIDO DONDE GUARDAREMOS LOS DATOS DEL PARTIDO
    #partidoUnico = funciones.crearJsonPartido(year,str(matchDayUrl('a'))[21:-48],numeroPartidosTemporada)
    partidoUnico = funciones.crearJsonPartidosDiarios(year, str(matchDayUrl('a'))[21:-48], numeroPartidosTemporada)

    ##  RECOGEMOS Y PARSEAMOS LA PÁGINA DEL PARTIDO
    #   ES LA PÁGINA PRINCIPAL DEL PARTIDO
    boxScoreGame = funciones.devolverPaginaPartido(matchDayUrl)

    ##  SACAMOS POR PANTALLA EL TITULO DE LA PÁGINA EN LA QUE ESTAMOS NAVEGANDO
    print (boxScoreGame.title.text)

    ############################################################################
    ####  ESTAMOS EN LA PÁGINA PRINCIPAL DEL BOXSCORE                       ####
    ############################################################################
    print ("ENTRAMOS EN LA PÁGINA PRINCIPAL DEL BOXSCORE")

    ##  CREAMOS LA VARIABLE DE PARTIDO
    partido = obj.partido()

    ##  RECOGEMOS LA ASISTENCIA DE PUBLICO DEL PARTIDO
    funcionesPartido.devolverAsistenciaPartido(boxScoreGame)

    ##  RELLENAMOS FECHA, ESTADIO Y UBICACIÓN EN LA VARIABLE PARTIDO
    partido.rellenarFechaUbicacion(
        str(dia),
        str(mes),
        str(funciones.devolverAnioCorrecto(year, mes)),
        funcionesPartido.horarioUbicacion(str(boxScoreGame.find_all("div", class_="scorebox_meta"))),
        funcionesPartido.devolverAsistenciaPartido(boxScoreGame)
    )

    ##  NAVEGAMOS POR LA PÁGINA RECOGIENDO DIFERENTES COSAS
    for stats in boxScoreGame.findAll('div', {"class": "scorebox"}):

        ##  RECOGEMOS:
        #   TANTEO LOCAL Y VISITANTE
        #   BALANCE DE VITORIAS Y DERROTAS  DE LOCAL Y VISITANTE
        contador = 0
        playIn = funciones.esPartidoPlayIn(dia,mes,year)
        if playIn:
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
        abre = []
        equipos = stats('strong')
        partido.equipoLocal.nombreAbreviado = str(equipos[1])[25:28].lower()
        partido.equipoVisitante.nombreAbreviado = str(equipos[0])[25:28].lower()

        ##  RECOGEMOS SI ES UN PARTIDO DE PLAYOFF O NO
        #   DESDE EL MES 10 11 12 1 2 3 NUNCA VA A SER PLAYOFF
        #   SI ESTAMOS EN MESES 4 5 6 7 Y SI EL NÚMERO ES MENOR O IGUAL A 7, ESTAMOS EN PLAYOFF
        if mes > 3 and mes < 10:
            if int(partido.equipoLocal.victorias) + int(partido.equipoLocal.derrotas) <= 7:
                partido.playOff = True
            else:
                partido.playOff = False
        else:
            partido.playOff = False
        print (partido.equipoVisitante.nombre + " " + str(partido.equipoVisitante.tanteo) + " - " + str(
            partido.equipoLocal.tanteo) + " " + partido.equipoLocal.nombre)
        print ("Patido de PlayOff: " + str(partido.playOff))

        ## RECOGEMOS LAS ESTADISTICAS NORMALES  DE LOS JUGADORES DEL PARTIDO DE LA PAGINA DE BOXSCORE
        partido.equipoLocal = funcionesPartido.devolverStadisticasNormalesJugadores(partido.equipoLocal, boxScoreGame)
        partido.equipoVisitante = funcionesPartido.devolverStadisticasNormalesJugadores(partido.equipoVisitante,
                                                                                        boxScoreGame)

        ## RECOGEMOS LAS ESTADISTICAS AVANZADAS  DE LOS JUGADORES DEL PARTIDO DE LA PAGINA DE BOXSCORE
        partido.equipoLocal = funcionesPartido.devolverStadisticasAvanzadas(partido.equipoLocal, boxScoreGame,
                                                                            partido.equipoLocal.jugadores)
        partido.equipoVisitante = funcionesPartido.devolverStadisticasAvanzadas(partido.equipoVisitante, boxScoreGame,
                                                                                partido.equipoVisitante.jugadores)

    ############################################################################
    ####  ENTRAMOS EN LA PÁGINA PARA DESCARGAR LAS                          ####
    ####  ESTADISTICAS POR CUARTO DE CADA EQUIPO                            ####
    ############################################################################

    ##  INSERTAMOS UNA MARCA DE TIEMPO  Y PARAMOS
    rn = random.randrange(2, 6)
    reloj.sleep(rn)

    print ("ENTRAMOS EN LA PÁGINA DE JUGADA A JUGADA")

    ## RECOGEMOS Y PARSEAMOS LA PAGINA DE PLAY BY PLAY DEL PARTIDO
    playbyplay = funciones.devolverPaginaPlayByPlay(matchDayUrl)

    ##  RECOGEMOS LAS ESTADISTICAS POR CUARTO DE CADA JUGADOR
    partido = funcionesPartido.devolverPlayByPlayJugadores(partido,playbyplay,str(matchDayUrl('a'))[21:-17],numeroPartidosTemporada)

    ##  RECOGEMOS DATOS ESTADISTICOS DE CADA EQUIPO
    partido = funcionesPartido.recogerLideratosPartido(str(playbyplay), partido)

    ############################################################################
    ####  ENTRAMOS EN LA PÁGINA PARA DESCARGAR LA                           ####
    ####  CARTA DE TIRO DE CADA JUGADOR DE CADA EQUIPO                      ####
    ############################################################################

    #  INSERTAMOS UNA MARCA DE TIEMPO  Y PARAMOS
    rn = random.randrange(2, 6)
    reloj.sleep(rn)

    print ("ENTRAMOS EN LA PÁGINA DE CARTA DE TIRO")

    ## RECOGEMOS Y PARSEAMO S LA PAGINA DE CARTA DE TIROS DEL PARTIDO
    shootChart = funciones.devolverPaginaCartaTiro(matchDayUrl)


    ##  RECOGEMOS LA CARTA DE TIROS DEL EQUIPO LOCAL
    partido.equipoLocal = funcionesPartido.devolverPosicionTirosJugadores(partido.equipoLocal, shootChart)
    ##  RECOGEMOS LA CARTA DE TIROS DEL EQUIPO VISITANTE
    partido.equipoVisitante = funcionesPartido.devolverPosicionTirosJugadores(partido.equipoVisitante, shootChart)

    ############################################################################
    ####  ENTRAMOS EN LA PÁGINA PARA DESCARGAR LOS                          ####
    ####  +/- POR CUARTO DE CADA JUGADOR EN CADA CUARTO                     ####
    ############################################################################

    ##  INSERTAMOS UNA MARCA DE TIEMPO  Y PARAMOS
    rn = random.randrange(2, 6)
    reloj.sleep(rn)

    print ("ENTRAMOS EN LA PÁGINA DE +/-")

    ## RECOGEMOS Y PARSEAMOS LA PAGINA DE MAS MENOS DEL PARTIDO
    masMenosPagina = funciones.devolverPaginaMasMenos(matchDayUrl)

    ##  RECOGEMOS EL +/- DE CADA JUGADOR DEL PARTIDO
    partido = funcionesPartido.devolverMasMenosJugadores(partido, masMenosPagina)

    ## RECOGEMOS TANTEOS DE CADA CUARTO DE CADA EQUIPO
    partido = funcionesPartido.recogerCuartosPartido(masMenosPagina, year, partido)

    ############################################################################
    ####  COMPLETAMOS LAS ESTADISTICAS COMPLETAS DE CADA JUGADOR Y EQUIPO   ####
    ############################################################################

    ##  COMPLETAMOS ESTADISTICAS NORMALES
    partido = funcionesPartido.completarFullBoxscoreJugador(partido)
    partido = funcionesPartido.completarFullBoxScoreLocal(partido)
    partido = funcionesPartido.completarFullBoxScoreVisitante(partido)

    ##  COMPLETAMOS ESTADISTICAS AVANZADAS
    partido.equipoVisitante = funcionesPartido.completarEstadisticaAvanzada(partido.equipoVisitante)
    partido.equipoLocal = funcionesPartido.completarEstadisticaAvanzada(partido.equipoLocal)

    ############################################################################
    ####  GUARDAMOS EL PARTIDO EN UN ARCHIVO JSON                           ####
    ############################################################################

    ##  GUARDAMOS LOS DATOS DEL PARTIDO EN EL ARCHIVO JSON
    partidoUnico.write(partido.toJSON())
    partidoUnico.close()

    archivoId = funciones.crearTxtId(year)

    for jugador in partido.equipoVisitante.jugadores:
        archivoId.write(jugador.id + '\n')
    for jugador in partido.equipoLocal.jugadores:
        archivoId.write(jugador.id + '\n')
    archivoId.close()

    print ("Fin partido")
