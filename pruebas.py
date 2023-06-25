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

partidosDelDia = funciones.devolverPaginaParse("https://www.basketball-reference.com/boxscores/?month=06&day=16&year=2022")
 
##  SACAMOS POR PANTALLA EL TITULO DE LA P�GINA EN LA QUE ESTAMOS NAVEGANDO
print (partidosDelDia.title.text)

##  RECORREMOS, SI HAY, LOS ENLACES LOS PARTIDOS JUGADOS ESE D�A
for matchDayUrl in partidosDelDia.findAll('td', {"class": "right gamelink"}):
    ##  RECOGEMOS Y PARSEAMOS LA P�GINA DEL PARTIDO
    #   ES LA P�GINA PRINCIPAL DEL PARTIDO
    boxScoreGame = funciones.devolverPaginaPartido(matchDayUrl)

    ##  SACAMOS POR PANTALLA EL TITULO DE LA P�GINA EN LA QUE ESTAMOS NAVEGANDO
    print boxScoreGame.title.text
    
    print "ENTRAMOS EN LA P�GINA PRINCIPAL DEL BOXSCORE"

    ##  CREAMOS LA VARIABLE DE PARTIDO
    partido=obj.partido()

    ##  RECOGEMOS LA ASISTENCIA DE PUBLICO DEL PARTIDO
    print str(funcionesPartido.devolverAsistenciaPartido(boxScoreGame))
    
     ##  NAVEGAMOS POR LA PÁGINA RECOGIENDO DIFERENTES COSAS
    for stats in boxScoreGame.findAll('div', {"class": "scorebox"}):
        ##  RECOGEMOS:
        #   TANTEO LOCAL Y VISITANTE
        #   BALANCE DE VITORIAS Y DERROTAS  DE LOCAL Y VISITANTE0
        contador = 0
        playIn = funciones.esPartidoPlayIn(16,06,funciones.devolverAnioCorrecto(2022,06))
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

