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


def devolverPaginaDescargada(year, tipo, numero):
    page = open("NBADATA/" + str(year) + "-" + str(year + 1) + "/" + str(numero) + "." + tipo + ".html", "r")
    return BeautifulSoup(page, "html.parser")

def contarArvhicosEnCarpeta(ruta):
    contenido = os.listdir(ruta)
    
    num_archivos = 0
    for elemento in contenido:
        num_archivos += 1
        
    return num_archivos/4



def devolverMes(mes):
    if 'Octo' in mes:
        return 10
    if 'Nove' in mes:
        return 11
    if "Dece" in mes:
        return 12
    if 'Jan' in mes:
        return 1
    if 'Febr' in mes:
        return 2
    if 'Mar' in mes:
        return 3
    if 'Apr' in mes:
        return 4
    if 'May' in mes:
        return 5
    if 'Jun' in mes:
        return 6
    if 'Jul' in mes:
        return 7
    if 'Augu' in mes:
        return 8
    if 'Septem' in mes:
        return 9

    
def crearJsonPartido(year, mes,dia,local,visitante,numero):
    return open(
        constantes.RAIZ + '/' + str(year) + '-' + str(year + 1) + '/' + funciones.devolverNumeroPartido(numero) + '_' +str(year)+''+str(mes)+''+str(dia)+''+
         local+''+visitante+'.json',
        'w')    
    
############################################################################
####   CLASE PRINCIPAL                                                  ####
############################################################################


##  VARIABLE PARA TENER UN CONTADOR DEL NUMERO DE PARTIDOS
numeroPartidosRegistrados = 0
##  VARIABLE QUE GUARDA LOS MESES QUE VAMOS A RECORRER
mesesTemporada = constantes.MESES_TEMPORADA

##  CREAMOS LA CARPETA RAIZ DONDE IREMOS GUARDANDO LAS TEMPORADAS SI NO EXISTE
##  SI EXISTE, NO HACE NADA0
funciones.crearCarpetaRaiz();

##  BUCLE PARA IR RECORRIENDO TEMPORADAS
for year in range(constantes.TEMPORADA_INICIAL, constantes.TEMPORADA_FINAL):

    #   NUMERO DE SEGUNDOS QUE RETAREMOS POR LAS PARADAS AUTOMATICAS
    sumatorioRestaDeSegundos = 0
    #   NUMERO DE PARTIDOS QUE VAMOS DESCARGANDO ESTA TEMPORADA
    numeroPartidosTemporada = 0

    
    ##  BUCLE PARA IR RECORRIENDO LOS PARTIDOS DE LA TEMPORADA
    for archivo in range(1, contarArvhicosEnCarpeta("NBADATA/" + str(year) + "-" + str(year + 1))+1):

        ##  SUMAMOS AL NUMERO DE PARTIDOS QUE VAMOS REGISTRANDO
        numeroPartidosRegistrados += 1
        numeroPartidosTemporada += 1
                
        ##  RECOGEMOS Y PARSEAMOS LA P�GINA DEL PARTIDO
        #   ES LA PAGINA PRINCIPAL DEL PARTIDO
        boxScoreGame = devolverPaginaDescargada(year, 'a', archivo)
    
        ##  SACAMOS POR PANTALLA EL TITULO DE LA PAGINA EN LA QUE ESTAMOS NAVEGANDO
        print boxScoreGame.title.text
        
        # Encontrar el elemento contenedor para obtener dia y mes
        scorebox_meta = boxScoreGame.find('div', class_='scorebox_meta')
        
        dia = scorebox_meta.find('div').text.split(',')[1].strip().split(' ') [1]
        mes = devolverMes(scorebox_meta.find('div').text.split(',')[1].strip().split(' ') [0])
        
        print "    Partidos de temporada: " + str(numeroPartidosTemporada) + ". Numero de partidos total descargados: " + str(numeroPartidosRegistrados)
    
        ############################################################################
        ####  ESTAMOS EN LA P�GINA PRINCIPAL DEL BOXSCORE                       ####
        ############################################################################
        print "    ENTRAMOS EN LA P�GINA PRINCIPAL DEL BOXSCORE"
    
        ##  CREAMOS LA VARIABLE DE PARTIDO
        partido = obj.partido()
    
        ##  RECOGEMOS LA ASISTENCIA DE PUBLICO DEL PARTIDO
        partido.asistencia = funcionesPartido.devolverAsistenciaPartido(boxScoreGame)
    
        ##  RELLENAMOS FECHA, ESTADIO Y UBICACION
        partido.rellenarFechaUbicacion(
            str(dia),
            str(mes),
            str(funciones.devolverAnioCorrecto(year, mes)),
            funcionesPartido.horarioUbicacion(str(boxScoreGame.find_all("div", class_="scorebox_meta"))),
            funcionesPartido.devolverAsistenciaPartido(boxScoreGame)
        )
    
        ##  NAVEGAMOS POR LA PAGINA RECOGIENDO DIFERENTES COSAS
        for stats in boxScoreGame.findAll('div', {"class": "scorebox"}):
    
            ##  RECOGEMOS:
            #   TANTEO LOCAL Y VISITANTE
            #   BALANCE DE VITORIAS Y DERROTAS  DE LOCAL Y VISITANTE
            contador = 0
            playIn = funciones.esPartidoPlayIn(dia, mes, funciones.devolverAnioCorrecto(year, mes))
            if playIn:
                print "    ES PARTIDO DE PLAY IN"
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
                        partido.equipoLocal.victorias = partidosJugadorLocal[0]
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
            #   SI ESTAMOS EN MESES 4 5 6 7 Y SI EL N�MERO ES MENOR O IGUAL A 7, ESTAMOS EN PLAYOFF
            #   SI ESTAMOS EN EL A�O 2020 LOS PLAYOFF VAN DEL 17 AGOSTO AL 11 DE OCTUBRE
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
                    if int(partido.equipoLocal.victorias) + int(partido.equipoLocal.derrotas) <= 7:
                        partido.playOff = True
                    else:
                        partido.playOff = False
            else:
                partido.playOff = False
    
            print "    "+partido.equipoVisitante.nombre + " " + str(partido.equipoVisitante.tanteo) + " - " + str(partido.equipoLocal.tanteo) + " " + partido.equipoLocal.nombre
            print "    Patido de PlayOff: " + str(partido.playOff)
    
            ## RECOGEMOS LAS ESTADISTICAS NORMALES  DE LOS JUGADORES DEL PARTIDO DE LA PAGINA DE BOXSCORE
            partido.equipoLocal = funcionesPartido.devolverStadisticasNormalesJugadores(partido.equipoLocal, boxScoreGame)
            partido.equipoVisitante = funcionesPartido.devolverStadisticasNormalesJugadores(partido.equipoVisitante, boxScoreGame)
    
            ## RECOGEMOS LAS ESTADISTICAS AVANZADAS  DE LOS JUGADORES DEL PARTIDO DE LA PAGINA DE BOXSCORE
            partido.equipoLocal = funcionesPartido.devolverStadisticasAvanzadas(partido.equipoLocal, boxScoreGame, partido.equipoLocal.jugadores)
            partido.equipoVisitante = funcionesPartido.devolverStadisticasAvanzadas(partido.equipoVisitante, boxScoreGame, partido.equipoVisitante.jugadores)
    
        ############################################################################
        ####  ENTRAMOS EN LA PAGINA PARA DESCARGAR LAS                          ####
        ####  ESTADISTICAS POR CUARTO DE CADA EQUIPO                            ####
        ############################################################################
    
        print "    ENTRAMOS EN LA P�GINA DE JUGADA A JUGADA"
    
        ## RECOGEMOS Y PARSEAMOS LA PAGINA DE PLAY BY PLAY DEL PARTIDO
        playbyplay = devolverPaginaDescargada(year, 'b', archivo)
        
        errorPagina = playbyplay.select('h1')[0].text.strip()
        
        if '    Page Not Found (404 error)' !=errorPagina:
            ##  RECOGEMOS LAS ESTADISTICAS POR CUARTO DE CADA JUGADOR
            partido = funcionesPartido.devolverPlayByPlayJugadores(partido, playbyplay, '', numeroPartidosTemporada)
        
            ##  RECOGEMOS DATOS ESTADISTICOS DE CADA EQUIPO
            partido = funcionesPartido.recogerLideratosPartido(str(playbyplay), partido)
    
        ############################################################################
        ####  ENTRAMOS EN LA P�GINA PARA DESCARGAR LA                           ####
        ####  CARTA DE TIRO DE CADA JUGADOR DE CADA EQUIPO                      ####
        ############################################################################
    
        print "    ENTRAMOS EN LA P�GINA DE CARTA DE TIRO"
    
        ## RECOGEMOS Y PARSEAMO S LA PAGINA DE CARTA DE TIROS DEL PARTIDO
        shootChart = devolverPaginaDescargada(year, 'c', archivo)
        
        errorPagina = shootChart.select('h1')[0].text.strip()
        
        if '    Page Not Found (404 error)' !=errorPagina:
            ##  RECOGEMOS LA CARTA DE TIROS DEL EQUIPO LOCAL
            partido.equipoLocal = funcionesPartido.devolverPosicionTirosJugadores(partido.equipoLocal, shootChart)
            ##  RECOGEMOS LA CARTA DE TIROS DEL EQUIPO VISITANTE
            partido.equipoVisitante = funcionesPartido.devolverPosicionTirosJugadores(partido.equipoVisitante, shootChart)
            
            partido.equipoLocal.jugadores = funcionesPartido.completarCartaTiro(partido.equipoLocal.jugadores)
            partido.equipoVisitante.jugadores = funcionesPartido.completarCartaTiro(partido.equipoVisitante.jugadores)
    
        ############################################################################
        ####  ENTRAMOS EN LA P�GINA PARA DESCARGAR LOS                          ####
        ####  +/- POR CUARTO DE CADA JUGADOR EN CADA CUARTO                     ####
        ############################################################################
    
        print "    ENTRAMOS EN LA P�GINA DE +/-"
    
        ## RECOGEMOS Y PARSEAMOS LA PAGINA DE MAS MENOS DEL PARTIDO
        masMenosPagina = devolverPaginaDescargada(year, 'd', archivo)
        
        errorPagina = masMenosPagina.select('h1')[0].text.strip()
        
        if '    Page Not Found (404 error)' !=errorPagina:
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
            
        ##  CREAMOS EL ARCHIVO DEL PARTIDO DONDE GUARDAREMOS LOS DATOS DEL PARTIDO
        partidoUnico = crearJsonPartido(year, mes, dia, partido.equipoLocal.nombreAbreviado,partido.equipoVisitante.nombreAbreviado, numeroPartidosTemporada)
            
        ##  GUARDAMOS LOS DATOS DEL PARTIDO EN EL ARCHIVO JSON
        partidoUnico.write(partido.toJSON())
        partidoUnico.close()
    
        print "Fin del partido partido"
        print "********************************************************"
        print " "
