#!/usr/bin/env python
# -*- coding: utf-8 -*-

from    bs4                 import      BeautifulSoup
import  urllib
import  os
import  random
import  re
import  funciones
import  constantes
import  re
import  sys
from    prettytable             import  PrettyTable
import  controllerPartido       as      obj
import  controllerJugador       as      objJugador
import     controllerStatNormales    as      cuarto
import  controllerCartaTiro     as      tiro
import  controllerCuarto        as      cuar

############################################################################
####  CLASE DONDE TENDREMOS LAS FUNCIONES PARA DESGRANAR LOS PARTIDOS   ####
############################################################################

reload(sys)
sys.setdefaultencoding('utf8')


############################################################################
####  FUNCION QUE DEVUELVE LA ASISTENCIA A UN PARTIDO                   ####
############################################################################
def devolverAsistenciaPartido(soup):
    try:
        return int(str(soup.find("strong", text="Attendance: ").next_sibling.strip().encode('utf-8')).replace(",", ""))
    except AttributeError as error:
        return int(str(soup.find("strong", text="Attendance:").next_sibling.strip().encode('utf-8')).replace(",", ""))
    except:
        return 15000;


#########################################################################################
####  FUNCIONES PARA RECOGER EL TANTEO POR CUARTDOS DEL PARTIDO DE CADA EQUIPO       ####
#########################################################################################
def recogerCuartosPartido(partido, year, partidoEntero):

    partidoEntero.equipoVisitante.tanteoCuartos = devolverCuartos(partidoEntero.equipoVisitante, partidoEntero.numeroCuartos)
    partidoEntero.equipoLocal.tanteoCuartos = devolverCuartos(partidoEntero.equipoLocal, partidoEntero.numeroCuartos)

    return partidoEntero


def devolverCuartos(equipo, numeroCuartos):
    primerCuarto = 0
    segundoCuarto = 0
    tercerCuarto = 0
    cuartoCuarto = 0
    primerOver = 0
    segundoOver = 0
    tercerOver = 0
    cuartoOver = 0
    quintoOver = 0
    sextoOver = 0

    for jugador in equipo.jugadores:
        primerCuarto = primerCuarto + funciones.puntosNulos(jugador.cuarto1.puntos)
        segundoCuarto = segundoCuarto + funciones.puntosNulos(jugador.cuarto2.puntos)
        tercerCuarto = tercerCuarto + funciones.puntosNulos(jugador.cuarto3.puntos)
        cuartoCuarto = cuartoCuarto + funciones.puntosNulos(jugador.cuarto4.puntos)
        if numeroCuartos == 5:
            primerOver = primerOver + funciones.puntosNulos(jugador.over1.puntos)
        if numeroCuartos == 6:
            primerOver = primerOver + funciones.puntosNulos(jugador.over1.puntos)
            segundoOver = segundoOver + funciones.puntosNulos(jugador.over2.puntos)
        if numeroCuartos == 7:
            primerOver = primerOver + funciones.puntosNulos(jugador.over1.puntos)
            segundoOver = segundoOver + funciones.puntosNulos(jugador.over2.puntos)
            tercerOver = tercerOver + funciones.puntosNulos(jugador.over3.puntos)
        if numeroCuartos == 8:
            primerOver = primerOver + funciones.puntosNulos(jugador.over1.puntos)
            segundoOver = segundoOver + funciones.puntosNulos(jugador.over2.puntos)
            tercerOver = tercerOver + funciones.puntosNulos(jugador.over3.puntos)
            cuartoOver = cuartoOver + funciones.puntosNulos(jugador.over4.puntos)
        if numeroCuartos == 9:
            primerOver = primerOver + funciones.puntosNulos(jugador.over1.puntos)
            segundoOver = segundoOver + funciones.puntosNulos(jugador.over2.puntos)
            tercerOver = tercerOver + funciones.puntosNulos(jugador.over3.puntos)
            cuartoOver = cuartoOver + funciones.puntosNulos(jugador.over4.puntos)
            quintoOver = quintoOver + funciones.puntosNulos(jugador.over5.puntos)

    cuartos = {}

    for i in range (0, numeroCuartos):
        if i == 0:
            cuartos["primero"] = str(primerCuarto)
        if i == 1:
            cuartos["segundo"] = str(segundoCuarto)
        if i == 2:
            cuartos["tercero"] = str(tercerCuarto)
        if i == 3:
            cuartos["cuarto"] = str(cuartoCuarto)
        if i == 4:
            cuartos["OT1"] = str(primerOver)
        if i == 5:
            cuartos["OT2"] = str(segundoOver)
        if i == 6:
            cuartos["OT3"] = str(tercerOver)
        if i == 7:
            cuartos["OT4"] = str(cuartoOver)
        if i == 8:
            cuartos["OT5"] = str(quintoOver)

    return cuartos

# def devolverCuartos(resul_Cuartos,partidoEntero):
    cuartosVisitante = {}
    cuartosLocal = {}
    numeroCuartosVisitante = resul_Cuartos.__len__() / 2
    visitante = resul_Cuartos[0:numeroCuartosVisitante]
    local = resul_Cuartos[numeroCuartosVisitante:resul_Cuartos.__len__()]

    for i in range(0, visitante.__len__()):
        if i == 0:
            cuartosVisitante["primero"] = visitante[i]
        if i == 1:
            cuartosVisitante["segundo"] = visitante[i]
        if i == 2:
            cuartosVisitante["tercero"] = visitante[i]
        if i == 3:
            cuartosVisitante["cuarto"] = visitante[i]
        if i == 4:
            cuartosVisitante["OT1"] = visitante[i]
        if i == 5:
            cuartosVisitante["OT2"] = visitante[i]
        if i == 6:
            cuartosVisitante["OT3"] = visitante[i]
        if i == 7:
            cuartosVisitante["OT4"] = visitante[i]
        if i == 8:
            cuartosVisitante["OT5"] = visitante[i]

    for i in range(0, local.__len__()):
        if i == 0:
            cuartosLocal["primero"] = local[i]
        if i == 1:
            cuartosLocal["segundo"] = local[i]
        if i == 2:
            cuartosLocal["tercero"] = local[i]
        if i == 3:
            cuartosLocal["cuarto"] = local[i]
        if i == 4:
            cuartosLocal["OT1"] = local[i]
        if i == 5:
            cuartosLocal["OT2"] = local[i]
        if i == 6:
            cuartosLocal["OT3"] = local[i]
        if i == 7:
            cuartosLocal["OT4"] = local[i]
        if i == 8:
            cuartosLocal["OT5"] = local[i]

    partidoEntero.equipoVisitante.tanteoCuartos = cuartosVisitante
    partidoEntero.equipoLocal.tanteoCuartos = cuartosLocal

    return partidoEntero


############################################################################
####  FUNCIONES QUE NOS DEVUELVE LA HORA Y LA UBICACION DEL PARTIDO     ####
############################################################################
def horarioUbicacion(cadena):
    horaUbi = []
    cadena = cadena.split('<div>')
    num = 1
    for o in cadena:
        mirar = o.split(",")
        # print str(mirar.__len__())
        for j in mirar:
            # print str(num)
            # print j
            if num == 2:
               horaUbi.append(horarioJson(j))
            if num == 5:
                horaUbi.append(j)
            if num == 6:
                if "href" not in j:
                    horaUbi.append(j)
            if num == 7:
                horaUbi.append((str(j).partition('<'))[0])
            num += 1
            # print horaUbi
    return horaUbi


def horarioJson(hora):
    horario = "T"
    if "PM" in hora:
        horario += str(int(hora.split(":")[0]) + 12) + ":"
        horario += str(hora.split(":")[1])[0:2]
    else:
        horario += str(rellenarFecha(hora.split(":")[0])) + ":"
        horario += str(hora.split(":")[1])[0:2]
    return horario + ":00.881Z"


def rellenarFecha(fech):
    fech = int(fech)
    if fech < 10:
        # print str('0'+str(fech))
        return str('0' + str(fech))
    return str(fech)


###########################################################################################
####  FUNCION QUE NOS DEVUELVE SI UN JUGADOR NO HAY JUGADO O SI TENEMOS TIEMPOS EXTRA  ####
###########################################################################################
def revisarMinutos(minutos):
    if minutos == '':
        return 0
    elif minutos == 'Did Not Play':
        return 0
    elif minutos == 'Player Suspended':
        return 0
    elif minutos == 'Did Not Dress':
        return 0
    elif minutos == 'Not With Team':
        return 0
    elif minutos == '240':  # Tiempo de juego normal
        return 240
    elif minutos == '265':  # 1 Tiempo extra
        return 265
    elif minutos == '290':  # 2 Tiempos extra
        return 290
    elif minutos == '315':  # 3 Tiempos extra
        return 315
    elif minutos == '340':  # 4 Tiempos extra
        return 340
    elif minutos == '365':  # 5 Tiempos extra
        return 365
    elif minutos == '390':  # 6 Tiempos extra
        return 390
    elif minutos == '415':  # 7 Tiempos extra
        return 415
    return calcularSegundos(devolverCorrecto(minutos))


def calcularSegundos(minutos):
    min, seg = minutos.split(':')
    # print 'minutos: '+str(min)+' - Segundos: '+str(seg
    return int(min) * 60 + int(seg)


############################################################################
####  FUNCION PARA DEVOLVER UN VALOR CORRECTAMENTE                      ####
############################################################################
def devolverCorrecto(valor):
    valor = str(valor).replace('\xc4\x80', 'A').replace('\xc4\x81', 'a').replace('\xc4\x82', 'A').replace('\xc4\x83', 'a').replace('\xc4\x84', 'A').replace('\xc4\x85', 'a').replace('\xc4\x86', 'C').replace('\xc4\x87', 'c').replace('\xc4\x88', 'C').replace('\xc4\x89', 'c').replace('\xc4\x8a', 'C').replace('\xc4\x8b', 'c').replace('\xc4\x8c', 'C').replace('\xc4\x8d', 'c').replace('\xc4\x8e', 'D').replace('\xc4\x8f', 'd').replace('\xc4\x90', 'D').replace('\xc4\x91', 'd').replace('\xc4\x92', 'E').replace('\xc4\x93', 'e').replace('\xc4\x94', 'E').replace('\xc4\x95', 'e').replace('\xc4\x96', 'E').replace('\xc4\x97', 'e').replace('\xc4\x98', 'E').replace('\xc4\x99', 'e').replace('\xc4\x9a', 'E').replace('\xc4\x9b', 'e').replace('\xc4\x9c', 'G').replace('\xc4\x9d', 'g').replace('\xc4\x9e', 'G').replace('\xc4\x9f', 'g').replace('\xc4\xa0', 'G').replace('\xc4\xa1', 'g').replace('\xc4\xa2', 'G').replace('\xc4\xa3', 'g').replace('\xc4\xa4', 'H').replace('\xc4\xa5', 'h').replace('\xc4\xa6', 'H').replace('\xc4\xa7', 'h').replace('\xc4\xa8', 'I').replace('\xc4\xa9', 'i').replace('\xc4\xaa', 'I').replace('\xc4\xab', 'i').replace('\xc4\xac', 'I').replace('\xc4\xad', 'i').replace('\xc4\xae', 'I').replace('\xc4\xaf', 'i').replace('\xc4\xb0', 'I').replace('\xc4\xb1', 'i').replace('\xc4\xb2', 'IJ').replace('\xc4\xb3', 'ij').replace('\xc4\xb4', 'J').replace('\xc4\xb5', 'j').replace('\xc4\xb6', 'K').replace('\xc4\xb7', 'k').replace('\xc4\xb8', 'k').replace('\xc4\xb9', 'L').replace('\xc4\xba', 'l').replace('\xc4\xbb', 'L').replace('\xc4\xbc', 'l').replace('\xc4\xbd', 'L').replace('\xc4\xbe', 'l').replace('\xc4\xbf', 'L').replace('\xc5\x80', 'l').replace('\xc5\x81', 'L').replace('\xc5\x82', 'l').replace('\xc5\x83', 'N').replace('\xc5\x84', 'n').replace('\xc5\x85', 'N').replace('\xc5\x86', 'n').replace('\xc5\x87', 'N').replace('\xc5\x88', 'ñ').replace('\xc5\x89', 'n').replace('\xc5\x8a', 'Ŋ').replace('\xc5\x8b', 'ŋ').replace('\xc5\x8c', 'O').replace('\xc5\x8d', 'o').replace('\xc5\x8e', 'O').replace('\xc5\x8f', 'o').replace('\xc5\x90', 'O').replace('\xc5\x91', 'o').replace('\xc5\x92', 'Q').replace('\xc5\x93', 'q').replace('\xc5\x94', 'R').replace('\xc5\x95', 'r').replace('\xc5\x96', 'R').replace('\xc5\x97', 'r').replace('\xc5\x98', 'R').replace('\xc5\x99', 'r').replace('\xc5\x9a', 'S').replace('\xc5\x9b', 's').replace('\xc5\x9c', 'S').replace('\xc5\x9d', 's').replace('\xc5\x9e', 'S').replace('\xc5\x9f', 's').replace('\xc5\xa0', 'S').replace('\xc5\xa1', 's').replace('\xc5\xa2', 'T').replace('\xc5\xa3', 't').replace('\xc5\xa4', 'T').replace('\xc5\xa5', 't').replace('\xc5\xa6', 'T').replace('\xc5\xa7', 't').replace('\xc5\xa8', 'U').replace('\xc5\xa9', 'u').replace('\xc5\xaa', 'U').replace('\xc5\xab', 'u').replace('\xc5\xac', 'U').replace('\xc5\xad', 'u').replace('\xc5\xae', 'U').replace('\xc5\xaf', 'u').replace('\xc5\xb0', 'U').replace('\xc5\xb1', 'u').replace('\xc5\xb2', 'V').replace('\xc5\xb3', 'v').replace('\xc5\xb4', 'W').replace('\xc5\xb5', 'w').replace('\xc5\xb6', 'Y').replace('\xc5\xb7', 'y').replace('\xc5\xb8', 'Y').replace('\xc5\xb9', 'Z').replace('\xc5\xba', 'z').replace('\xc5\xbb', 'Z').replace('\xc5\xbc', 'z').replace('\xc5\xbd', 'Z').replace('\xc5\xbe', 'z').replace('\xc5\xbf', 'f').replace('\xc6\x80', 'b').replace('\xc6\x81', 'B').replace('\xc6\x82', 'B').replace('\xc6\x83', 'b').replace('\xc6\x84', 'b').replace('\xc6\x85', 'b').replace('\xc6\x86', 'C').replace('\xc6\x87', 'C').replace('\xc6\x88', 'c').replace('\xc6\x89', 'D').replace('\xc6\x8a', 'D').replace('\xc6\x8b', 'D').replace('\xc6\x8c', 'd').replace('\xc6\x8d', 'd').replace('\xc6\x8e', 'E').replace('\xc6\x8f', 'E').replace('\xc6\x90', 'E').replace('\xc6\x91', 'F').replace('\xc6\x92', 'f').replace('\xc6\x93', 'G').replace('\xc6\x94', 'Y').replace('\xc6\x95', 'y').replace('\xc6\x96', 'I').replace('\xc6\x97', 'I').replace('\xc6\x98', 'K').replace('\xc6\x99', 'k').replace('\xc6\x9a', 'j').replace('\xc6\x9b', 'y').replace('\xc6\x9c', 'W').replace('\xc6\x9d', 'N').replace('\xc6\x9e', 'n').replace('\xc6\x9f', 'O').replace('\xc6\xa0', 'O').replace('\xc6\xa1', 'o').replace('\xc6\xa2', 'Q').replace('\xc6\xa3', 'q').replace('\xc6\xa4', 'P').replace('\xc6\xa5', 'p').replace('\xc6\xa6', 'k').replace('\xc6\xa7', 'S').replace('\xc6\xa8', 's').replace('\xc6\xa9', 'E').replace('\xc6\xaa', 'l').replace('\xc6\xab', 't').replace('\xc6\xac', 'T').replace('\xc6\xad', 't').replace('\xc6\xae', 'T').replace('\xc6\xaf', 'U').replace('\xc6\xb0', 'u').replace('\xc6\xb1', 'O').replace('\xc6\xb2', 'U').replace('\xc6\xb3', 'Y').replace('\xc6\xb4', 'y').replace('\xc6\xb5', 'Z').replace('\xc6\xb6', 'z').replace('\xc6\xb7', 'Z').replace('\xc6\xb8', 'E').replace('\xc6\xb9', 'e').replace('\xc6\xba', 'z').replace('\xc6\xbb', 'z').replace('\xc6\xbc', '5').replace('\xc6\xbd', '5').replace('\xc6\xbe', 'z').replace('\xc6\xbf', 'D').replace('\xc7\x80', '|').replace('\xc7\x81', '|').replace('\xc7\x82', '#').replace('\xc7\x83', '!').replace('\xc7\x84', 'Dl').replace('\xc7\x85', 'Dz').replace('\xc7\x86', 'dz').replace('\xc7\x87', 'w').replace('\xc7\x88', 'Lj').replace('\xc7\x89', 'lj').replace('\xc7\x8a', 'Nj').replace('\xc7\x8b', 'Nj').replace('\xc7\x8c', 'nj').replace('\xc7\x8d', 'A').replace('\xc7\x8e', 'a').replace('\xc7\x8f', 'I').replace('\xc7\x90', 'i').replace('\xc7\x91', 'O').replace('\xc7\x92', 'o').replace('\xc7\x93', 'U').replace('\xc7\x94', 'u').replace('\xc7\x95', 'U').replace('\xc7\x96', 'u').replace('\xc7\x97', 'U').replace('\xc7\x98', 'u').replace('\xc7\x99', 'U').replace('\xc7\x9a', 'u').replace('\xc7\x9b', 'U').replace('\xc7\x9c', 'u').replace('\xc7\x9d', 'e').replace('\xc7\x9e', 'A').replace('\xc7\x9f', 'a').replace('\xc7\xa0', 'A').replace('\xc7\xa1', 'a').replace('\xc7\xa2', 'AE').replace('\xc7\xa3', 'ae').replace('\xc7\xa4', 'G').replace('\xc7\xa5', 'g').replace('\xc7\xa6', 'G').replace('\xc7\xa7', 'g').replace('\xc7\xa8', 'K').replace('\xc7\xa9', 'k').replace('\xc7\xaa', 'Q').replace('\xc7\xab', 'q').replace('\xc7\xac', 'O').replace('\xc7\xad', 'o').replace('\xc7\xae', 'z').replace('\xc7\xaf', 'z').replace('\xc7\xb0', 'J').replace('\xc7\xb1', 'Dl').replace('\xc7\xb2', 'Dz').replace('\xc7\xb3', 'dz').replace('\xc7\xb4', 'G').replace('\xc7\xb5', 'ǵ').replace('\xc7\xb6', 'Hu').replace('\xc7\xb7', 'D').replace('\xc7\xb8', 'Ñ').replace('\xc7\xb9', 'ñ').replace('\xc7\xba', 'A').replace('\xc7\xbb', 'a').replace('\xc7\xbc', 'AE').replace('\xc7\xbd', 'ae').replace('\xc7\xbe', 'O').replace('\xc7\xbf', 'o').replace('\xc2\x80', '').replace('\xc2\x81', '').replace('\xc2\x82', '').replace('\xc2\x83', '').replace('\xc2\x84', '').replace('\xc2\x85', '').replace('\xc2\x86', '').replace('\xc2\x87', '').replace('\xc2\x88', '').replace('\xc2\x89', '').replace('\xc2\x8a', '').replace('\xc2\x8b', '').replace('\xc2\x8c', '').replace('\xc2\x8d', '').replace('\xc2\x8e', '').replace('\xc2\x8f', '').replace('\xc2\x90', '').replace('\xc2\x91', '').replace('\xc2\x92', '').replace('\xc2\x93', '').replace('\xc2\x94', '').replace('\xc2\x95', '').replace('\xc2\x96', '').replace('\xc2\x97', '').replace('\xc2\x98', '').replace('\xc2\x99', '').replace('\xc2\x9a', '').replace('\xc2\x9b', '').replace('\xc2\x9c', '').replace('\xc2\x9d', '').replace('\xc2\x9e', '').replace('\xc2\x9f', '').replace('\xc2\xa0', '').replace('\xc2\xa1', 'i').replace('\xc2\xa2', '').replace('\xc2\xa3', '').replace('\xc2\xa4', '').replace('\xc2\xa5', '').replace('\xc2\xa6', '|').replace('\xc2\xa7', '').replace('\xc2\xa8', '').replace('\xc2\xa9', '').replace('\xc2\xaa', 'ª').replace('\xc2\xab', '<').replace('\xc2\xac', '.').replace('\xc2\xad', '').replace('\xc2\xae', '').replace('\xc2\xaf', '-').replace('\xc2\xb0', 'º').replace('\xc2\xb1', '').replace('\xc2\xb2', '').replace('\xc2\xb3', '').replace('\xc2\xb4', '').replace('\xc2\xb5', '').replace('\xc2\xb6', '').replace('\xc2\xb7', '.').replace('\xc2\xb8', ',').replace('\xc2\xb9', '').replace('\xc2\xba', '').replace('\xc2\xbb', '>').replace('\xc2\xbc', '1/4').replace('\xc2\xbd', '1/2').replace('\xc2\xbe', '3/4').replace('\xc2\xbf', '¿').replace('\xc3\x80', 'A').replace('\xc3\x81', 'A').replace('\xc3\x82', 'A').replace('\xc3\x83', 'A').replace('\xc3\x84', 'A').replace('\xc3\x85', 'A').replace('\xc3\x86', 'AE').replace('\xc3\x87', 'C').replace('\xc3\x88', 'E').replace('\xc3\x89', 'E').replace('\xc3\x8a', 'E').replace('\xc3\x8b', 'E').replace('\xc3\x8c', 'I').replace('\xc3\x8d', 'I').replace('\xc3\x8e', 'I').replace('\xc3\x8f', 'I').replace('\xc3\x90', 'D').replace('\xc3\x91', 'Ñ').replace('\xc3\x92', 'O').replace('\xc3\x93', 'O').replace('\xc3\x94', 'O').replace('\xc3\x95', 'O').replace('\xc3\x96', 'O').replace('\xc3\x97', 'x').replace('\xc3\x98', 'Q').replace('\xc3\x99', 'U').replace('\xc3\x9a', 'U').replace('\xc3\x9b', 'U').replace('\xc3\x9c', 'U').replace('\xc3\x9d', 'Y').replace('\xc3\x9e', 'y').replace('\xc3\x9f', 'b').replace('\xc3\xa0', 'a').replace('\xc3\xa1', 'a').replace('\xc3\xa2', 'a').replace('\xc3\xa3', 'a').replace('\xc3\xa4', 'a').replace('\xc3\xa5', 'a').replace('\xc3\xa6', 'ae').replace('\xc3\xa7', 'ç').replace('\xc3\xa8', 'e').replace('\xc3\xa9', 'e').replace('\xc3\xaa', 'e').replace('\xc3\xab', 'e').replace('\xc3\xac', 'i').replace('\xc3\xad', 'i').replace('\xc3\xae', 'i').replace('\xc3\xaf', 'i').replace('\xc3\xb0', 'o').replace('\xc3\xb1', 'ñ').replace('\xc3\xb2', 'o').replace('\xc3\xb3', 'o').replace('\xc3\xb4', 'o').replace('\xc3\xb5', 'o').replace('\xc3\xb6', 'o').replace('\xc3\xb7', '/').replace('\xc3\xb8', 'o').replace('\xc3\xb9', 'u').replace('\xc3\xba', 'u').replace('\xc3\xbb', 'u').replace('\xc3\xbc', 'u').replace('\xc3\xbd', 'y').replace('\xc3\xbe', 'p').replace('\xc3\xbf', 'y')
    valor = valor.replace("+", " ")
    valor = valor.replace('ć', 'c')
    valor = valor.replace('ê', 'e')
    return valor


############################################################################
####  FUNCION PARA DEVOLVER UN 0 SI EL DATO VIENE VACIO                 ####
############################################################################
def revisarDato(dato):
    if dato == '':
        return 0
    else:
        return dato


######################################################################################
####  FUNCION QUE DEVUELVE LAS ESTADISTICAS NORMALES DE LOS JUGADORES Y EQUIPOS   ####
######################################################################################
def devolverStadisticasNormalesJugadores(equipo, pagina):
    equipo.jugadores = []
    # #  RECOGEMOS LOS JUGADORES DEPENDIENDO DEL EEQUIPO QUE ESTAMOS
    jugadores = pagina.findAll('div', {"id": "all_box-" + equipo.nombreAbreviado.upper() + "-game-basic"})
    continuar = True
    for jugador in jugadores:
        if continuar:
            continuar = False
            campos = jugador.findAll('tr')
            r = -2
            for campo in campos:
                i = 0
                r += 1
                for resultado in campo.findAll('td'):
                    # # REVISAMOS, SI TENENEMOS 0 SEGUNDOS, SIGNIFICA QUE ES UN JUGADOR QUE NO HA JUGADO
                    if i == 0:
                        segundos = revisarMinutos(resultado.text)

                    if segundos == 0:
                        indice = campo.find('a')
                        id = str(indice['href']).split('/')[3][:-5]

                        sinJugar = objJugador.jugador(str(id))
                        nombreJugador = str(devolverCorrecto(campo.find('th').text)).split()

                        if len(nombreJugador) == 2:
                            sinJugar.nombre = nombreJugador[0]
                            sinJugar.apellido = nombreJugador[1]
                        elif len(nombreJugador) == 3:
                            sinJugar.nombre = nombreJugador[0]
                            sinJugar.apellido = nombreJugador[1] + " " + nombreJugador[2]
                        elif len(nombreJugador) == 4:
                            sinJugar.nombre = nombreJugador[0]
                            sinJugar.apellido = nombreJugador[1] + " " + nombreJugador[2] + " " + nombreJugador[3]

                        sinJugar.inicio = False
                        # equipo.jugadores.append(sinJugar)
                        sinJugar.boxscore("TotalPartido")
                        equipo.insertarJugador(sinJugar)

                    # #  ESTADISTICAS DEL EQUIPO
                    if str(campo.find('th').text) == 'Team Totals':
                        if i == 0: equipo.estadisticaNormal.cuarto = "Partido"
                        if i == 1: equipo.estadisticaNormal.tirosCampoMetidos = int(revisarDato(resultado.text))
                        if i == 2: equipo.estadisticaNormal.tirosCampoIntentados = int(revisarDato(resultado.text))
                        if i == 3: equipo.estadisticaNormal.tirosCampoPorcentaje = float(revisarDato(resultado.text))
                        if i == 4: equipo.estadisticaNormal.triplesMetidos = int(revisarDato(resultado.text))
                        if i == 5: equipo.estadisticaNormal.triplesIntentados = int(revisarDato(resultado.text))
                        if i == 6: equipo.estadisticaNormal.triplesPorcentaje = float(revisarDato(resultado.text))
                        if i == 7: equipo.estadisticaNormal.tirosLibresMetidos = int(revisarDato(resultado.text))
                        if i == 8: equipo.estadisticaNormal.tirosLibresIntentados = int(revisarDato(resultado.text))
                        if i == 9: equipo.estadisticaNormal.tirosLibresPorcentaje = float(revisarDato(resultado.text))
                        if i == 10: equipo.estadisticaNormal.reboteOfensivo = int(revisarDato(resultado.text))
                        if i == 11: equipo.estadisticaNormal.reboteDefensivo = int(revisarDato(resultado.text))
                        if i == 12: equipo.estadisticaNormal.totalRebotes = int(revisarDato(resultado.text))
                        if i == 13: equipo.estadisticaNormal.asistencias = int(revisarDato(resultado.text))
                        if i == 14: equipo.estadisticaNormal.robos = int(revisarDato(resultado.text))
                        if i == 15: equipo.estadisticaNormal.tapones = int(revisarDato(resultado.text))
                        if i == 16: equipo.estadisticaNormal.perdidas = int(revisarDato(resultado.text))
                        if i == 17: equipo.estadisticaNormal.faltasPersonales = int(revisarDato(resultado.text))
                        if i == 18: equipo.estadisticaNormal.puntos = int(revisarDato(resultado.text))
                    else:  # # ESTADISTICAS DEL LOS JUGADORES QUE HAN JUGADO ALGUN MINUTO
                        if i == 0:
                            indice = campo.find('a')
                            id = str(indice['href']).split('/')[3][:-5]

                            jugando = objJugador.jugador(str(id))
                            nombreJugador = str(devolverCorrecto(campo.find('th').text)).split()
                            jugando.boxscore("Total PArtido")

                            if len(nombreJugador) == 2:
                                jugando.nombre = nombreJugador[0]
                                jugando.apellido = nombreJugador[1]
                            elif len(nombreJugador) == 3:
                                jugando.nombre = nombreJugador[0]
                                jugando.apellido = nombreJugador[1] + " " + nombreJugador[2]
                            elif len(nombreJugador) == 4:
                                jugando.nombre = nombreJugador[0]
                                jugando.apellido = nombreJugador[1] + " " + nombreJugador[2] + " " + nombreJugador[3]
                            if r < 6:
                                jugando.inicio = True
                            else:
                                jugando.inicio = False

                            jugando.segundos = int(segundos)
                        if i == 1: jugando.boxscore.tirosCampoMetidos = int(revisarDato(resultado.text))
                        if i == 2: jugando.boxscore.tirosCampoIntentados = int(revisarDato(resultado.text))
                        if i == 3: jugando.boxscore.tirosCampoPorcentaje = float(revisarDato(resultado.text))
                        if i == 4: jugando.boxscore.triplesMetidos = int(revisarDato(resultado.text))
                        if i == 5: jugando.boxscore.triplesIntentados = int(revisarDato(resultado.text))
                        if i == 6: jugando.boxscore.triplesPorcentaje = float(revisarDato(resultado.text))
                        if i == 7: jugando.boxscore.tirosLibresMetidos = int(revisarDato(resultado.text))
                        if i == 8: jugando.boxscore.tirosLibresIntentados = int(revisarDato(resultado.text))
                        if i == 9: jugando.boxscore.tirosLibresPorcentaje = float(revisarDato(resultado.text))
                        if i == 10: jugando.boxscore.reboteOfensivo = int(revisarDato(resultado.text))
                        if i == 11: jugando.boxscore.reboteDefensivo = int(revisarDato(resultado.text))
                        if i == 12: jugando.boxscore.totalRebotes = int(revisarDato(resultado.text))
                        if i == 13: jugando.boxscore.asistencias = int(revisarDato(resultado.text))
                        if i == 14: jugando.boxscore.robos = int(revisarDato(resultado.text))
                        if i == 15: jugando.boxscore.tapones = int(revisarDato(resultado.text))
                        if i == 16: jugando.boxscore.perdidas = int(revisarDato(resultado.text))
                        if i == 17: jugando.boxscore.faltasPersonales = int(revisarDato(resultado.text))
                        if i == 18: jugando.boxscore.puntos = int(revisarDato(resultado.text))
                        if i == 19:
                            jugando.boxscore.masMenos = int(revisarDato(resultado.text))
                            equipo.insertarJugador(jugando)
                    i += 1
    return equipo


#################################################################################################
####  FUNCION QUE NOS DEVUELVE LAS ESTADISTICAS AVANZADAS DE JUGADORES Y EQUIPOS             ####
#################################################################################################
def devolverStadisticasAvanzadas(equipo, pagina, jugadoresEquipo):
    # #  RECOGEMOS LOS JUGADORES DEPENDIENDO DEL EQUIPO
    jugadores = pagina.findAll('div', {"id": "all_box-" + equipo.nombreAbreviado.upper() + "-game-advanced"})
    for jugador in jugadores:
        campos = jugador.findAll('tr')
        for campo in campos:
            i = 0
            for resultado in campo.findAll('td'):

                # #  ESTADISTICAS DEL EQUIPO
                if str(campo.find('th').text) == 'Team Totals':
                    # print "Posición: "+str(i) +". "+str(revisarDato(resultado.text))
                    if i == 1: equipo.estadisticaAvanzada.trueShootPer = float(revisarDato(resultado.text))
                    if i == 2: equipo.estadisticaAvanzada.effectiveGoalPer = float(revisarDato(resultado.text))
                    if i == 3: equipo.estadisticaAvanzada.threePointRate = float(revisarDato(resultado.text))
                    if i == 4: equipo.estadisticaAvanzada.freeThrowRate = float(revisarDato(resultado.text))
                    if i == 5: equipo.estadisticaAvanzada.offensiveReboundPer = float(revisarDato(resultado.text))
                    if i == 6: equipo.estadisticaAvanzada.defensiveReboundPer = float(revisarDato(resultado.text))
                    if i == 7: equipo.estadisticaAvanzada.totalReboundPer = float(revisarDato(resultado.text))
                    if i == 8: equipo.estadisticaAvanzada.assistPercentage = float(revisarDato(resultado.text))
                    if i == 9: equipo.estadisticaAvanzada.stealPercentage = float(revisarDato(resultado.text))
                    if i == 10: equipo.estadisticaAvanzada.blockPercentage = float(revisarDato(resultado.text))
                    if i == 11: equipo.estadisticaAvanzada.turnoverPercentage = float(revisarDato(resultado.text))
                    if i == 12: equipo.estadisticaAvanzada.usagePercentage = float(revisarDato(resultado.text))
                    if i == 13: equipo.estadisticaAvanzada.offensiveRating = float(revisarDato(resultado.text))
                    if i == 14: equipo.estadisticaAvanzada.defensiveRating = float(revisarDato(resultado.text))
                else:  # # ESTADISTICAS DEL LOS JUGADORES QUE HAN JUGADO ALGUN MINUTO
                    # print "Posición: " + str(i) + ". " + str(revisarDato(resultado.text))

                    if i == 0:
                        indice = campo.find('a')
                        id = str(indice['href']).split('/')[3][:-5]
                        posicion = devolverposicionJugadorAvanzada(id, jugadoresEquipo)

                    if i == 1: equipo.jugadores[posicion].estadisticaAvanzada.trueShootPer = float(revisarDato(resultado.text))
                    if i == 2: equipo.jugadores[posicion].estadisticaAvanzada.effectiveGoalPer = float(revisarDato(resultado.text))
                    if i == 3: equipo.jugadores[posicion].estadisticaAvanzada.threePointRate = float(revisarDato(resultado.text))
                    if i == 4: equipo.jugadores[posicion].estadisticaAvanzada.freeThrowRate = float(revisarDato(resultado.text))
                    if i == 5: equipo.jugadores[posicion].estadisticaAvanzada.offensiveReboundPer = float(revisarDato(resultado.text))
                    if i == 6: equipo.jugadores[posicion].estadisticaAvanzada.defensiveReboundPer = float(revisarDato(resultado.text))
                    if i == 7: equipo.jugadores[posicion].estadisticaAvanzada.totalReboundPer = float(revisarDato(resultado.text))
                    if i == 8: equipo.jugadores[posicion].estadisticaAvanzada.assistPercentage = float(revisarDato(resultado.text))
                    if i == 9: equipo.jugadores[posicion].estadisticaAvanzada.stealPercentage = float(revisarDato(resultado.text))
                    if i == 10: equipo.jugadores[posicion].estadisticaAvanzada.blockPercentage = float(revisarDato(resultado.text))
                    if i == 11: equipo.jugadores[posicion].estadisticaAvanzada.turnoverPercentage = float(revisarDato(resultado.text))
                    if i == 12: equipo.jugadores[posicion].estadisticaAvanzada.usagePercentage = float(revisarDato(resultado.text))
                    if i == 13: equipo.jugadores[posicion].estadisticaAvanzada.offensiveRating = float(revisarDato(resultado.text))
                    if i == 14: equipo.jugadores[posicion].estadisticaAvanzada.defensiveRating = float(revisarDato(resultado.text))
                i += 1
    return equipo


def devolverposicionJugadorAvanzada(id, jugadores):
    for i in range(len(jugadores)):
        if id == jugadores[i].id:
            return i


################################################################################
####  FUNCION QUE NOS DEVUELVE LA PAGINA DE TIROS DE UN EQUIPO              ####
################################################################################
def devolverPosicionTirosJugadores(equipo, pagina):
    for i in range(len(equipo.jugadores)):

        selector = '.tooltip.p-' + equipo.jugadores[i].id
        cont = 0
        equipo.jugadores[i].listaTiros = []

        nombreLen = equipo.jugadores[i].apellido.split()

        nombre = equipo.jugadores[i].nombre

        # ('Tim' == nombre and len(nombreLen) == 1 and 'Hardaway' == nombreLen[0]) or
        # or ('Kelly' == nombre and len(nombreLen) == 1 and 'Oubre' == nombreLen[0])
        # or ('Glenn' == nombre and len(nombreLen) == 1 and 'Robinson' == nombreLen[0])
        # ('Larry' == nombre and len(nombreLen) == 1 and 'Nance' == nombreLen[0])

        if False:
            for div in pagina.select(selector):
                jugada = tiro.tiros()

                # # POSICION DEL TIRO
                posicion = str(div['style'])
                jugada.meterPosicionTop(posicion.split(';')[0].split(':')[1].replace('px', ''))
                jugada.meterPosicionLeft(posicion.split(';')[1].split(':')[1].replace('px', ''))

                # # SITUACION DE TIRO
                parte = str(div['tip']).split('<br>')
                # print parte
                seleccion = 0

                for x in parte:
                    detalle = x.split()
                    seguir = False
                    for x in parte:
                        detalle = x.split()
                        seguir = False
                        for y in detalle:
                            seleccion += 1
                            # print y + " " + str(seleccion)
                            if seleccion == 1: jugada.meterCuarto(y)
                            if seleccion == 2: jugada.meterTipoCuarto(y)
                            if seleccion == 3: jugada.meterTiempoRestante(y[:-2])
                            if seleccion == 7:
                                if 'made' in y:
                                    jugada.meterDentro(True)
                                else:
                                    jugada.meterDentro(False)
                            if seleccion == 8:
                                if '2' in y:
                                    jugada.meterTipo("2")
                                else:
                                    jugada.meterTipo("3")
                            if seleccion == 11:
                                jugada.meterDistancia(int(y))
                            if seleccion == 14:
                                if 'now' not in y:
                                    jugada.meterSituacion(y)
                                    seguir = True
                            if seleccion == 15 and seguir == True:
                                jugada.meterTanteo(y)
                            elif seleccion != 14 and seleccion != 16:
                                jugada.meterSituacion(y)
                            if seleccion == 16: jugada.meterTanteo(y)
                equipo.jugadores[i].meterCartaTiro(jugada)
        elif 'Nene' == nombre and len(nombreLen) == 1:
            # print 'Entramos ya que estamos con Nene Hilario'
            for div in pagina.select(selector):
                jugada = tiro.tiros()

                # # POSICION DEL TIRO
                posicion = str(div['style'])
                jugada.meterPosicionTop(posicion.split(';')[0].split(':')[1].replace('px', ''))
                jugada.meterPosicionLeft(posicion.split(';')[1].split(':')[1].replace('px', ''))

                # # SITUACION DE TIRO
                parte = str(div['tip']).split('<br>')
                # print parte
                seleccion = 0

                for x in parte:
                    detalle = x.split()
                    seguir = False
                    # print parte
                    for y in detalle:
                        y = devolverCorrecto(y)
                        seleccion += 1
                        # print y + " " + str(seleccion)
                        if seleccion == 1: jugada.meterCuarto(y)
                        if seleccion == 2: jugada.meterTipoCuarto(y)
                        if seleccion == 3: jugada.meterTiempoRestante(y[:-2])
                        if 'Hilário' not in detalle:
                            if seleccion == 9:
                                jugada.meterDistancia(int(y))
                            if seleccion == 6:
                                if 'made' in y:
                                    jugada.meterDentro(True)
                                else:
                                    jugada.meterDentro(False)
                            if seleccion == 7:
                                if '2' in y:
                                    jugada.meterTipo("2")
                                else:
                                    jugada.meterTipo("3")
                            if seleccion > 9:
                                jugada.meterTanteo(y)
                        else:
                            if seleccion == 10:
                                jugada.meterDistancia(int(y))
                            if seleccion == 7:
                                if 'made' in y:
                                    jugada.meterDentro(True)
                                else:
                                    jugada.meterDentro(False)
                            if seleccion == 8:
                                if '2' in y:
                                    jugada.meterTipo("2")
                                else:
                                    jugada.meterTipo("3")
                            if seleccion > 10:
                                jugada.meterTanteo(y)
                        # if seleccion == 13:
                        #     if 'now' not in y:
                        #         jugada.meterSituacion(y)
                        #         seguir = True
                        # if seleccion == 13 and seguir == True:
                        #     jugada.meterTanteo(y)
                        # elif seleccion != 12 and seleccion != 14:
                        #     jugada.meterSituacion(y)
                        # if seleccion == 14: jugada.meterTanteo(y)
                equipo.jugadores[i].meterCartaTiro(jugada)
        else:
            # #  MIRAMOS EL TAMAÑO DEL NOMBRE Y APELLIDO DEL JUGADOR YA QUE LAS POSICIONES VARIAN SEGUN EL TAMAÑO
            # print nombreLen
            if len(nombreLen) == 1:
                # print 'Nombre Len = 1'
                for div in pagina.select(selector):
                    jugada = tiro.tiros()

                    # # POSICION DEL TIRO
                    posicion = str(div['style'])
                    jugada.meterPosicionTop(posicion.split(';')[0].split(':')[1].replace('px', ''))
                    jugada.meterPosicionLeft(posicion.split(';')[1].split(':')[1].replace('px', ''))

                    # # SITUACION DE TIRO
                    parte = str(div['tip']).split('<br>')
                    # print parte
                    seleccion = 0
                    extra = 0
                    # print parte[1]
                    if ("Jr." in parte[1] and "Jr. Smith" not in parte[1]) or "III" in parte[1] or "II" in parte[1] or "Sr." in parte[1] or "IV" in parte[1] or "Lemorris Garris" in parte[1]:
                        extra = extra + 1
                    if "Faverani" in nombreLen:
                        extra = extra + 1
                    # print nombreLen
                    # print parte

                    for x in parte:
                        # print parte
                        detalle = x.split()
                        seguir = False
                        for y in detalle:
                            y = devolverCorrecto(y)
                            seleccion += 1
                            # print y + " " + str(seleccion)
                            if seleccion == 1: jugada.meterCuarto(y)
                            if seleccion == 2: jugada.meterTipoCuarto(y)
                            if seleccion == 3: jugada.meterTiempoRestante(y[:-2])
                            if seleccion == (7 + extra):
                                if 'made' in y: jugada.meterDentro(True)
                                else: jugada.meterDentro(False)
                            if seleccion == (8 + extra):
                                if '2' in y: jugada.meterTipo("2")
                                else: jugada.meterTipo("3")
                            if seleccion == (10 + extra):
                                # print str(10+extra)
                                jugada.meterDistancia(int(y))
                            if seleccion > 10:
                                jugada.meterTanteo(y)
                            # if seleccion == (13+extra):
                            #     if 'now' not in y:
                            #         jugada.meterSituacion(y)
                            #         seguir = True
                            # if seleccion == (14+extra) and seguir == True:
                            #     jugada.meterTanteo(y)
                            # elif seleccion != (13+extra) and seleccion != (15+extra):
                            #     jugada.meterSituacion(y)
                            # if seleccion == (15+extra): jugada.meterTanteo(y)
                    equipo.jugadores[i].meterCartaTiro(jugada)
            elif len(nombreLen) == 2:
                # print 'Nombre Len = 2'
                for div in pagina.select(selector):
                    jugada = tiro.tiros()

                    # # POSICION DEL TIRO
                    posicion = str(div['style'])
                    jugada.meterPosicionTop(posicion.split(';')[0].split(':')[1].replace('px', ''))
                    jugada.meterPosicionLeft(posicion.split(';')[1].split(':')[1].replace('px', ''))

                    # # SITUACION DE TIRO
                    parte = str(div['tip']).split('<br>')
                    # print parte
                    seleccion = 0
                    # print parte
                    extra = 0
                    if ("Jr." in parte[1] and "Jr. Smith" not in parte[1]) or "III" in parte[1] or "II" in parte[1] or "Sr." in parte[1]or "IV" in parte[1] or "Peace" in parte[1] or 'Negro' in parte[1]:
                        extra = extra + 1
                    if "Faverani" in nombreLen or "Exel" in nombreLen or "Horn" in nombreLen or "Ramos" in nombreLen or "Navarro" in nombreLen or "Colo" in nombreLen or "McAdoo" in nombreLen or "Silva" in nombreLen:
                        extra = extra + 1

                    for x in parte:
                        detalle = x.split()
                        seguir = False
                        for y in detalle:
                            seleccion += 1
                            # print y + " " + str(seleccion)
                            if seleccion == 1: jugada.meterCuarto(y)
                            if seleccion == 2: jugada.meterTipoCuarto(y)
                            if seleccion == 3: jugada.meterTiempoRestante(y[:-2])
                            if seleccion == 7:
                                if 'made' in y:
                                    jugada.meterDentro(True)
                                else:
                                    jugada.meterDentro(False)
                            if seleccion == 8:
                                if '2' in y:
                                    jugada.meterTipo("2")
                                else:
                                    jugada.meterTipo("3")
                            if seleccion == (10 + extra):
                                # print y
                                if "from" in y:
                                    extra += 1
                                else:
                                    jugada.meterDistancia(int(y))
                            if seleccion > 10:
                                jugada.meterTanteo(y)
                            # if seleccion == 14:
                            #     if 'now' not in y:
                            #         jugada.meterSituacion(y)
                            #         seguir = True
                            # if seleccion == 15 and seguir == True:
                            #     jugada.meterTanteo(y)
                            # elif seleccion != 14 and seleccion != 16:
                            #     jugada.meterSituacion(y)
                            # if seleccion == 16: jugada.meterTanteo(y)
                    equipo.jugadores[i].meterCartaTiro(jugada)
            elif len(nombreLen) == 3:
                # print 'Nombre Len = 3'
                # print "NOMBRE LEN = 3"
                for div in pagina.select(selector):
                    jugada = tiro.tiros()

                    # # POSICION DEL TIRO
                    posicion = str(div['style'])
                    jugada.meterPosicionTop(posicion.split(';')[0].split(':')[1].replace('px', ''))
                    jugada.meterPosicionLeft(posicion.split(';')[1].split(':')[1].replace('px', ''))

                    # # SITUACION DE TIRO
                    parte = str(div['tip']).split('<br>')
                    # print parte
                    seleccion = 0
                    # print parte

                    for x in parte:
                        detalle = x.split()
                        seguir = False
                        for y in detalle:
                            seleccion += 1
                            # print y + " " + str(seleccion)
                            if seleccion == 1: jugada.meterCuarto(y)
                            if seleccion == 2: jugada.meterTipoCuarto(y)
                            if seleccion == 3: jugada.meterTiempoRestante(y[:-2])
                            if seleccion == 7:
                                if 'made' in y:
                                    jugada.meterDentro(True)
                                else:
                                    jugada.meterDentro(False)
                            if seleccion == 8:
                                if '2' in y:
                                    jugada.meterTipo("2")
                                else:
                                    jugada.meterTipo("3")
                            if seleccion == 12:
                                # print str(y)
                                jugada.meterDistancia(int(y))
                            if seleccion > 12:
                                jugada.meterTanteo(y)
                            # if seleccion == 15:
                            #     if 'now' not in y:
                            #         jugada.meterSituacion(y)
                            #         seguir = True
                            # if seleccion == 16 and seguir == True:
                            #     jugada.meterTanteo(y)
                            # elif seleccion != 15 and seleccion != 17:
                            #     jugada.meterSituacion(y)
                            # if seleccion == 17: jugada.meterTanteo(y)
                    equipo.jugadores[i].meterCartaTiro(jugada)
    return equipo


#################################################################################################
####  FUNCION QUE NOS DEVUELVE LAS ESTADISTICAS POR CUARTO DE LA PAGINA PLAY BY PLAY         ####
#################################################################################################
def devolverPlayByPlayJugadores(partido, pagina, url, numero):
    cuarto = 0
    contador = "A"
    seguir = False
    save = ""
    crearPrimerCuarto(partido)

    for link in pagina.find_all('td'):
        particion = link.text
        # print particion
        cuartoJugando(particion, partido)
        # print particion

        if ("12:00.0" not in particion and "Start" not in particion and "Jump" not in particion and "End" not in particion and "1st" not in particion and "2nd" not in particion and "3rd" not in particion and "4th" not in particion)\
                or (seguir == True)\
                or("12:00.0" in save and "Start" not in particion and "Jump" not in particion and "End" not in particion and "1st" not in particion and "2nd" not in particion and "3rd" not in particion and "4th" not in particion):
            if contador == "A":
                # print "Tiempo Restante de Cuarto:     " + particion
                contador = "B"
            elif contador == "B":
                # print "    Equipo Visitante:          " + particion
                actividadPartido(particion, partido.equipoVisitante.jugadores, cuarto, partido.equipoLocal.jugadores, partido.equipoVisitante, partido.equipoLocal)
                contador = "C"
            elif contador == "C":
                # print "    Suma tanteo del Visitante: " + particion
                contador = "D"
            elif contador == "D":
                # print "    Tanteo Actual:             " + particion
                contador = "E"
            elif contador == "E":
                # print "    Suma tanteo del Local:     " + particion
                contador = "F"
            elif contador == "F":
                # print "    Equipo Local:              " + particion
                actividadPartido(particion, partido.equipoLocal.jugadores, cuarto, partido.equipoVisitante.jugadores, partido.equipoLocal, partido.equipoVisitante)
                contador = "A"
                # print "\n"

        if "Start" in particion or "Jump" in particion:
            contador = "A"
            seguir = True
        else:
            seguir = False

        if "1st" in particion:
            if "overtime" in particion and "End" not in particion:
                cuarto = 4
                # print "EMPIEZA PRIMERA PRORROGA"

        if "2nd" in particion:
            if "quarter" in particion and "End" not in particion:
                cuarto = 1
                # print "EMPIEZA SEGUNDO CUARTO"
            elif "overtime" in particion and "End" not in particion:
                cuarto = 5
                # print "EMPIEZA SEGUNDA PRORROGA"

        if "3rd" in particion:
            if "quarter" in particion and "End" not in particion:
                cuarto = 2
                # print "EMPIEZA TERCER CUARTO"
            elif "overtime" in particion and "End" not in particion:
                cuarto = 6
                # print "EMPIEZA TERCERA PRORROGA"

        if "4th" in particion:
            if "quarter" in particion and "End" not in particion:
                cuarto = 3
                # print "EMPIEZA CUARTO CUARTO"
            elif "overtime" in particion and "End" not in particion:
                cuarto = 7
                # print "EMPIEZA CUARTA PRORROGA"

        if "5th" in particion:
            if "overtime" in particion and "End" not in particion:
                cuarto = 8
                # print "EMPIEZA QUINTA PRORROGA"

        if "6th" in particion:
            if "overtime" in particion and "End" not in particion:
                cuarto = 9
                # print "EMPIEZA SEXTA PRORROGA"
        if '12:00.0' in particion:
            save = particion
            contador = "B"
    completarEstadisticasJugadores(partido.equipoLocal.jugadores)
    completarEstadisticasJugadores(partido.equipoVisitante.jugadores)

    return partido


def completarEstadisticasJugadores(jugadoresPartido):
    for i in jugadoresPartido:
        i.completarEstadisticas()


def numueroTiroLibre(libre):
    if "1" in libre:
        return "        Primer "
    if "2" in libre:
        return "        Segundo "
    if "3" in libre:
        return "        Tercer "


def esAsistenia(asistencia):
    temp = len(asistencia[len(asistencia) - 1])
    # print '        Canasta Asistida por ' + asistencia[len(asistencia) - 1][:temp - 1]


def autorJugada(parte, jugadoresPartido):
    for i in range(len(jugadoresPartido)):
        if parte in jugadoresPartido[i].apellido:
            return i


def autorJugadaInicial(inicial, apellido, jugadoresPartido, otrosJugadores):
    for i in range(len(jugadoresPartido)):
        if inicial[0] in jugadoresPartido[i].nombre[0].upper() and apellido in jugadoresPartido[i].apellido:
            return i
    for i in range(len(otrosJugadores)):
        if inicial[0] in otrosJugadores[i].nombre[0].upper() and apellido in otrosJugadores[i].apellido:
            return i
    return -1


#################################################################################################
####  SUB FUNCION DE PLAY BY PLAY QUE CATEGORIZA EL TIPO DE JUGADA EN LA QUE ESTAMOS         ####
#################################################################################################
def actividadPartido(texto, jugadoresPartido, cuarto, otrosJugadores, primerEquipo, segundoEquipo):
    # print texto
    parte = devolverCorrecto(texto)
    parte = parte.split()
    posicion = 0
    posicionBis = 0
    try:
        #########################################
        # #    REBOTE                           ##
        #########################################
        if 'rebound' in texto:
            if "Team" not in texto:
                posicion = autorJugadaInicial(parte[3], parte[4], jugadoresPartido, otrosJugadores)
                if posicion != -1:
                    if 'Offensive' in texto:
                        # print '        Rebote Ofensivo de: ' + parte[3] + " " + parte[4]
                        jugadoresPartido[posicion].estadisticasCuarto[cuarto].reboteOfensivo += 1
                        jugadoresPartido[posicion].estadisticasCuarto[cuarto].totalRebotes += 1
                    elif 'Defensive' in texto:
                        # print '        Rebote Defensivo de: ' + parte[3] + parte[4]
                        jugadoresPartido[posicion].estadisticasCuarto[cuarto].reboteDefensivo += 1
                        jugadoresPartido[posicion].estadisticasCuarto[cuarto].totalRebotes += 1

        #########################################
        # #    TIRO DE CAMPO Y LIBRE            ##
        #########################################
        tipoTiro = devolverTipoTiro(texto)
        if '2-pt' in texto:
            if 'misses' in texto:
                # print "        Tiro de 2 de: " + parte[1] + ". Fuera    " + tipoTiro
                posicion = autorJugadaInicial(parte[0], parte[1], jugadoresPartido, otrosJugadores)
                if posicion != -1:
                    # jugadoresPartido[posicion].estadisticasCuarto[cuarto].tirosCampoIntentados += 1
                    if 'dunk' in texto:
                        jugadoresPartido[posicion].estadisticasCuarto[cuarto].mateFallado += 1
                        jugadoresPartido[posicion].estadisticasCuarto[cuarto].tirosCampoIntentados += 1
                    elif 'layup' in texto:
                        jugadoresPartido[posicion].estadisticasCuarto[cuarto].bandejaFallada += 1
                        jugadoresPartido[posicion].estadisticasCuarto[cuarto].tirosCampoIntentados += 1
                    elif 'hook' in texto:
                        jugadoresPartido[posicion].estadisticasCuarto[cuarto].ganchoFallado += 1
                        jugadoresPartido[posicion].estadisticasCuarto[cuarto].tirosCampoIntentados += 1
                    else:
                        jugadoresPartido[posicion].estadisticasCuarto[cuarto].suspensionFallado += 1
                        jugadoresPartido[posicion].estadisticasCuarto[cuarto].tirosCampoIntentados += 1
                    if '(block' in texto:
                        jugadoresPartido[posicion].estadisticasCuarto[cuarto].taponRecibido += 1
                        temp = len(parte[len(parte) - 1])
                        if '.' in parte[-2]:
                            posicionBis = autorJugadaInicial(parte[-2], parte[len(parte) - 1][:temp - 1],otrosJugadores, jugadoresPartido)
                            if posicionBis != -1:
                                otrosJugadores[posicionBis].estadisticasCuarto[cuarto].tapones += 1
                        else:
                            posicionBis = autorJugadaInicial(parte[-3], parte[len(parte) - 2][:temp - 1] + " " + parte[len(parte) - 1][:temp - 1],otrosJugadores, jugadoresPartido)
                            if posicionBis != -1:
                                otrosJugadores[posicionBis].estadisticasCuarto[cuarto].tapones += 1
            elif 'makes' in texto:
                # print "        Tiro de 2 de: " + parte[1] + ". Dentro    " + tipoTiro
                posicion = autorJugadaInicial(parte[0], parte[1], jugadoresPartido, otrosJugadores)
                if posicion != -1:
                    jugadoresPartido[posicion].estadisticasCuarto[cuarto].tirosCampoIntentados += 1
                    jugadoresPartido[posicion].estadisticasCuarto[cuarto].tirosCampoMetidos += 1
                    if 'dunk' in texto:
                        jugadoresPartido[posicion].estadisticasCuarto[cuarto].mate += 1
                    elif 'layup' in texto:
                        jugadoresPartido[posicion].estadisticasCuarto[cuarto].bandeja += 1
                    elif 'hook' in texto:
                        jugadoresPartido[posicion].estadisticasCuarto[cuarto].gancho += 1
                    else:
                        jugadoresPartido[posicion].estadisticasCuarto[cuarto].suspension += 1
                    #########################################
                    # #    ASISTENCIA                       ##
                    #########################################
                    if '(assist' in texto:
                        temp = len(parte[len(parte) - 1])
                        # print '     Canasta Asistida por ' + parte[len(parte) - 1][:temp - 1]
                        if '.' in parte[-2]:
                            posicionBis = autorJugadaInicial(parte[-2], parte[len(parte) - 1][:temp - 1],
                                                             jugadoresPartido, otrosJugadores)
                            if posicionBis != -1:
                                jugadoresPartido[posicionBis].estadisticasCuarto[cuarto].asistencias += 1
                        else:
                            posicionBis = autorJugadaInicial(parte[-3], parte[len(parte) - 2][:temp - 1] + " " + parte[
                                                                                                                     len(
                                                                                                                         parte) - 1][:temp - 1],
                                                             jugadoresPartido, otrosJugadores)
                            if posicionBis != -1:
                                jugadoresPartido[posicionBis].estadisticasCuarto[cuarto].asistencias += 1
        if '3-pt' in texto:
            if 'misses' in texto:
                # print "        Tiro de 3 de: " + parte[1] + ". Fuera    "
                posicion = autorJugadaInicial(parte[0], parte[1], jugadoresPartido, otrosJugadores)
                if posicion != -1:
                    jugadoresPartido[posicion].estadisticasCuarto[cuarto].tirosCampoIntentados += 1
                    jugadoresPartido[posicion].estadisticasCuarto[cuarto].triplesIntentados += 1
                    jugadoresPartido[posicion].estadisticasCuarto[cuarto].suspensionFallado += 1
                    if '(block' in texto:
                        jugadoresPartido[posicion].estadisticasCuarto[cuarto].taponRecibidoTriple += 1
                        temp = len(parte[len(parte) - 1])
                        if '.' in parte[-2]:
                            posicionBis = autorJugadaInicial(parte[-2], parte[len(parte) - 1][:temp - 1],
                                                             otrosJugadores, jugadoresPartido)
                            if posicionBis != -1:
                                otrosJugadores[posicionBis].estadisticasCuarto[cuarto].tapones += 1
                        else:
                            posicionBis = autorJugadaInicial(parte[-3], parte[len(parte) - 2][:temp - 1] + " " + parte[
                                                                                                                     len(
                                                                                                                         parte) - 1][:temp - 1],
                                                             otrosJugadores, jugadoresPartido)
                            if posicionBis != -1:
                                otrosJugadores[posicionBis].estadisticasCuarto[cuarto].tapones += 1
            elif 'makes' in texto:
                # print "        Tiro de 3 de: " + parte[1] + ". Dentro    "
                posicion = autorJugadaInicial(parte[0], parte[1], jugadoresPartido, otrosJugadores)
                if posicion != -1:
                    jugadoresPartido[posicion].estadisticasCuarto[cuarto].tirosCampoIntentados += 1
                    jugadoresPartido[posicion].estadisticasCuarto[cuarto].tirosCampoMetidos += 1
                    jugadoresPartido[posicion].estadisticasCuarto[cuarto].triplesIntentados += 1
                    jugadoresPartido[posicion].estadisticasCuarto[cuarto].triplesMetidos += 1
                    jugadoresPartido[posicion].estadisticasCuarto[cuarto].suspension += 1
                    #########################################
                    # #    ASISTENCIA                       ##
                    #########################################
                    if '(assist' in texto:
                        temp = len(parte[len(parte) - 1])
                        # print '     Canasta Asistida por ' + parte[len(parte) - 1][:temp - 1]
                        if '.' in parte[-2]:
                            posicionBis = autorJugadaInicial(parte[-2], parte[len(parte) - 1][:temp - 1],
                                                             jugadoresPartido, otrosJugadores)
                            if posicionBis != -1:
                                jugadoresPartido[posicionBis].estadisticasCuarto[cuarto].asistencias += 1
                        else:
                            posicionBis = autorJugadaInicial(parte[-3], parte[len(parte) - 2][:temp - 1] + " " + parte[
                                                                                                                     len(
                                                                                                                         parte) - 1][:temp - 1],
                                                             jugadoresPartido, otrosJugadores)
                            if posicionBis != -1:
                                jugadoresPartido[posicionBis].estadisticasCuarto[cuarto].asistencias += 1
        if 'free' in texto:
            posicion = autorJugadaInicial(parte[0], parte[1], jugadoresPartido, otrosJugadores)
            if posicion != -1:
                if 'misses' in texto:
                    # print numueroTiroLibre(parte[5]) + "tiro libre de " + parte[7] + " Fallado por " + parte[1]
                    jugadoresPartido[posicion].estadisticasCuarto[cuarto].tirosLibresIntentados += 1

                    if "1" in parte[5]:
                        jugadoresPartido[posicion].estadisticasCuarto[cuarto].primerTiroLibreFuera += 1
                    elif "2" in parte[5]:
                        jugadoresPartido[posicion].estadisticasCuarto[cuarto].segundoTiroLibreFuera += 1
                    else:
                        jugadoresPartido[posicion].estadisticasCuarto[cuarto].tercerTiroLibreFuera += 1
                elif 'makes' in texto:
                    # print numueroTiroLibre(parte[5]) + "tiro libre de " + parte[7] + " Metido por " + parte[1]
                    jugadoresPartido[posicion].estadisticasCuarto[cuarto].tirosLibresIntentados += 1
                    jugadoresPartido[posicion].estadisticasCuarto[cuarto].tirosLibresMetidos += 1

                    if "1" in parte[5]:
                        jugadoresPartido[posicion].estadisticasCuarto[cuarto].primerTiroLibreDentro += 1
                    elif "2" in parte[5]:
                        jugadoresPartido[posicion].estadisticasCuarto[cuarto].segundoTiroLibreDentro += 1
                    else:
                        jugadoresPartido[posicion].estadisticasCuarto[cuarto].tercerTiroLibreDentro += 1

        ##########################################################################
        # #    TIPOS DE PERDIDAS EN EL TRANSCURSO DEL PARTIDO                    ##
        ##########################################################################
        # #    traveling                   Pasos                                 ##
        # #    bad pass                    Mal pase                              ##
        # #    offensive foul              Falta en ataque                       ##
        # #    out of bounds lost ball     Fuera de banda, tocar el ultimo       ##
        # #    lost ball                   Balon perdido                         ##
        # #    step out of bounds          Fuera de banda, pisar linea           ##
        # #    shot clock                  Reloj de Tiro_Perdida Equipo          ##
        # #    off goalTending             Goaltending ofensivo                  ##
        # #        El defensive es violación no es ningun tipo de perdida        ##
        # #                                                                      ##
        ##########################################################################
        if 'Turnover by Team' not in texto:
            if 'Turnover' in texto:
                posicion = autorJugadaInicial(parte[2], parte[3], jugadoresPartido, otrosJugadores)
                if posicion != -1:
                    # print '        Perdida de: ' + parte[2] + " " + parte[3]
                    jugadoresPartido[posicion].estadisticasCuarto[cuarto].perdidas += 1
                    #########################################
                    # #    ROBOS                            ##
                    #########################################
                    if 'steal' in texto:
                        temp = len(parte[len(parte) - 1])
                        # jugadoresPartido[autorJugadaInicial(parte[-2], parte[len(parte) - 1][:temp - 1],otrosJugadores)].estadisticasCuarto[cuarto].robos += 1
                        if '.' in parte[-2]:
                            posicionBis = autorJugadaInicial(parte[-2], parte[len(parte) - 1][:temp - 1],
                                                             otrosJugadores, jugadoresPartido)
                            if posicionBis != -1:
                                otrosJugadores[posicionBis].estadisticasCuarto[cuarto].robos += 1
                        else:
                            posicionBis = autorJugadaInicial(parte[-3], parte[len(parte) - 2][:temp - 1] + " " + parte[
                                                                                                                     len(
                                                                                                                         parte) - 1][:temp - 1],
                                                             otrosJugadores, jugadoresPartido)
                            if posicionBis != -1:
                                otrosJugadores[posicionBis].estadisticasCuarto[cuarto].robos += 1

                    if '(traveling' in texto:
                        jugadoresPartido[posicion].estadisticasCuarto[cuarto].perdidaPasos += 1
                    elif '(bad pass' in texto:
                        jugadoresPartido[posicion].estadisticasCuarto[cuarto].perdidaMalPase += 1
                    elif '(out of bounds lost ball' in texto:
                        jugadoresPartido[posicion].estadisticasCuarto[cuarto].perdidaFueraBanda += 1
                    elif '(lost ball' in texto:
                        jugadoresPartido[posicion].estadisticasCuarto[cuarto].perdidaBalonPerdido += 1
                    elif '(step out of bounds' in texto:
                        jugadoresPartido[posicion].estadisticasCuarto[cuarto].perdidaPisarFuera += 1
                    elif '(off goalTending' in texto:
                        jugadoresPartido[posicion].estadisticasCuarto[cuarto].perdidaGoaltending += 1

        #########################################
        # #    FALTA                            ##
        #########################################
        if 'foul' in texto:
            if 'Personal take ' in texto:
                # print '        Falta Personal en defensa: ' + parte[4] + " " + parte[5]
                posicion = autorJugadaInicial(parte[4], parte[5], otrosJugadores, jugadoresPartido)
                if posicion != -1:
                    otrosJugadores[posicion].estadisticasCuarto[cuarto].faltaPersonalDefensa += 1
                    otrosJugadores[posicion].estadisticasCuarto[cuarto].faltasPersonales += 1
                    if '(drawn' in texto:
                        temp = len(parte[len(parte) - 1])
                        # jugadoresPartido[autorJugadaInicial(parte[-2], parte[len(parte) - 1][:temp - 1],jugadoresPartido)].estadisticasCuarto[cuarto].faltaPersonalProvocadaEnDefensa += 1
                        if '.' in parte[-2]:
                            posicionBis = autorJugadaInicial(parte[-2], parte[len(parte) - 1][:temp - 1],
                                                             jugadoresPartido, otrosJugadores)
                            if posicionBis != -1:
                                jugadoresPartido[posicionBis].estadisticasCuarto[cuarto].faltaPersonalProvocadaEnDefensa += 1
                                jugadoresPartido[posicionBis].estadisticasCuarto[cuarto].faltasPersonalesProvocadas += 1
                        else:
                            posicionBis = autorJugadaInicial(parte[-3], parte[len(parte) - 2][:temp - 1] + " " + parte[len(parte) - 1][:temp - 1], jugadoresPartido, otrosJugadores)
                            if posicionBis != -1:
                                jugadoresPartido[posicionBis].estadisticasCuarto[cuarto].faltaPersonalProvocadaEnDefensa += 1
                                jugadoresPartido[posicionBis].estadisticasCuarto[cuarto].faltasPersonalesProvocadas += 1
            elif 'Personal' in texto:
                # print '        Falta Personal en defensa: ' + parte[3] + " " + parte[4]
                posicion = autorJugadaInicial(parte[3], parte[4], otrosJugadores, jugadoresPartido)
                if posicion != -1:
                    otrosJugadores[posicion].estadisticasCuarto[cuarto].faltaPersonalDefensa += 1
                    otrosJugadores[posicion].estadisticasCuarto[cuarto].faltasPersonales += 1
                    if '(drawn' in texto:
                        temp = len(parte[len(parte) - 1])
                        # jugadoresPartido[autorJugadaInicial(parte[-2], parte[len(parte) - 1][:temp - 1],jugadoresPartido)].estadisticasCuarto[cuarto].faltaPersonalProvocadaEnDefensa += 1
                        if '.' in parte[-2]:
                            posicionBis = autorJugadaInicial(parte[-2], parte[len(parte) - 1][:temp - 1],
                                                             jugadoresPartido, otrosJugadores)
                            if posicionBis != -1:
                                jugadoresPartido[posicionBis].estadisticasCuarto[cuarto].faltaPersonalProvocadaEnDefensa += 1
                                jugadoresPartido[posicionBis].estadisticasCuarto[cuarto].faltasPersonalesProvocadas += 1
                                    
                        else:
                            posicionBis = autorJugadaInicial(parte[-3], parte[len(parte) - 2][:temp - 1] + " " + parte[len(parte) - 1][:temp - 1],jugadoresPartido, otrosJugadores)
                            if posicionBis != -1:
                                jugadoresPartido[posicionBis].estadisticasCuarto[cuarto].faltaPersonalProvocadaEnDefensa += 1
                                jugadoresPartido[posicionBis].estadisticasCuarto[cuarto].faltasPersonalesProvocadas += 1
            elif 'Loose' in texto:
                # print '        Falta Personal en defensa: ' + parte[4] + " " + parte[5]
                posicion = autorJugadaInicial(parte[4], parte[5], jugadoresPartido, otrosJugadores)
                if posicion != -1:
                    jugadoresPartido[posicion].estadisticasCuarto[cuarto].faltaPersonalDefensa += 1
                    jugadoresPartido[posicion].estadisticasCuarto[cuarto].faltasPersonales += 1
                    if '(drawn' in texto:
                        temp = len(parte[len(parte) - 1])
                        # jugadoresPartido[autorJugadaInicial(parte[-2], parte[len(parte) - 1][:temp - 1],jugadoresPartido)].estadisticasCuarto[cuarto].faltaPersonalProvocadaEnDefensa += 1
                        if '.' in parte[-2]:
                            posicionBis = autorJugadaInicial(parte[-2], parte[len(parte) - 1][:temp - 1], otrosJugadores,jugadoresPartido)
                            if posicionBis != -1:
                                otrosJugadores[posicionBis].estadisticasCuarto[cuarto].faltaPersonalProvocadaEnDefensa += 1
                                otrosJugadores[posicionBis].estadisticasCuarto[cuarto].faltasPersonalesProvocadas += 1
                        else:
                            posicionBis = autorJugadaInicial(parte[-3], parte[len(parte) - 2][:temp - 1] + " " + parte[len(parte) - 1][:temp - 1], otrosJugadores,jugadoresPartido)
                            if posicionBis != -1:
                                otrosJugadores[posicionBis].estadisticasCuarto[cuarto].faltaPersonalProvocadaEnDefensa += 1
                                otrosJugadores[posicionBis].estadisticasCuarto[cuarto].faltasPersonalesProvocadas += 1
            elif 'Shooting' in texto:
                # print '        Falta personal de Tiro: ' + parte[3] + " " + parte[4]
                posicion = autorJugadaInicial(parte[3], parte[4], otrosJugadores, jugadoresPartido)
                if posicion != -1:
                    otrosJugadores[posicion].estadisticasCuarto[cuarto].faltaPersonalTiro += 1
                    otrosJugadores[posicion].estadisticasCuarto[cuarto].faltasPersonales += 1
                    if '(drawn' in texto:
                        temp = len(parte[len(parte) - 1])
                        # jugadoresPartido[autorJugadaInicial(parte[-2], parte[len(parte) - 1][:temp - 1],jugadoresPartido)].estadisticasCuarto[cuarto].faltaPersonalProvocadaEnTiro += 1
                        if '.' in parte[-2]:
                            posicionBis = autorJugadaInicial(parte[-2], parte[len(parte) - 1][:temp - 1],jugadoresPartido, otrosJugadores)
                            if posicionBis != -1:
                                jugadoresPartido[posicionBis].estadisticasCuarto[cuarto].faltaPersonalProvocadaEnTiro += 1
                                jugadoresPartido[posicionBis].estadisticasCuarto[cuarto].faltasPersonalesProvocadas += 1
                        else:
                            posicionBis = autorJugadaInicial(parte[-3], parte[len(parte) - 2][:temp - 1] + " " + parte[len(parte) - 1][:temp - 1],jugadoresPartido, otrosJugadores)
                            if posicionBis != -1:
                                jugadoresPartido[posicionBis].estadisticasCuarto[cuarto].faltaPersonalProvocadaEnTiro += 1
                                jugadoresPartido[posicionBis].estadisticasCuarto[cuarto].faltasPersonalesProvocadas += 1
            elif 'Offensive' in texto:
                # print '        Falta Personal en Ataque: ' + parte[3] + " " + parte[4]
                posicion = autorJugadaInicial(parte[3], parte[4], jugadoresPartido, otrosJugadores)
                if posicion != -1:
                    jugadoresPartido[posicion].estadisticasCuarto[cuarto].faltaPersonalAtaque += 1
                    jugadoresPartido[posicion].estadisticasCuarto[cuarto].faltasPersonales += 1
                    if '(drawn' in texto:
                        temp = len(parte[len(parte) - 1])
                        # jugadoresPartido[autorJugadaInicial(parte[-2], parte[len(parte) - 1][:temp - 1],jugadoresPartido)].estadisticasCuarto[cuarto].faltaPersonalProvocadaEnAtaque += 1
                        if '.' in parte[-2]:
                            posicionBis = autorJugadaInicial(parte[-2], parte[len(parte) - 1][:temp - 1],otrosJugadores, jugadoresPartido)
                            if posicionBis != -1:
                                otrosJugadores[posicionBis].estadisticasCuarto[cuarto].faltaPersonalProvocadaEnAtaque += 1
                                otrosJugadores[posicionBis].estadisticasCuarto[cuarto].faltasPersonalesProvocadas += 1
                        else:
                            posicionBis = autorJugadaInicial(parte[-3], parte[len(parte) - 2][:temp - 1] + " " + parte[len(parte) - 1][:temp - 1],otrosJugadores, jugadoresPartido)
                            if posicionBis != -1:
                                otrosJugadores[posicionBis].estadisticasCuarto[cuarto].faltaPersonalProvocadaEnAtaque += 1
                                otrosJugadores[posicionBis].estadisticasCuarto[cuarto].faltasPersonalesProvocadas += 1
            elif 'Technical' in texto:
                if 'Technical foul by Team' not in texto:
                    # print '        Tecnica del Jugador: ' + parte[3] + " " + parte[4]
                    posicion = autorJugadaInicial(parte[3], parte[4], jugadoresPartido, otrosJugadores)
                    if posicion != -1:
                        jugadoresPartido[posicion].estadisticasCuarto[cuarto].faltaTecnica += 1
                        jugadoresPartido[posicion].estadisticasCuarto[cuarto].faltasPersonales += 1
    except IndexError:
        print 'Fuera de Rango'


#########################################################################################
####  CREAMOS LOS CUARTOS SEGUN NOS VAYAN HACIENDO FALTA                             ####
#########################################################################################
def crearPrimerCuarto(partido):
    for i in range(len(partido.equipoLocal.jugadores)):
        partido.equipoLocal.jugadores[i].estadisticasCuarto = []
        partido.equipoLocal.jugadores[i].meterCuarto(partido.equipoLocal.jugadores[i].cuarto1)
    for i in range(len(partido.equipoVisitante.jugadores)):
        partido.equipoVisitante.jugadores[i].estadisticasCuarto = []
        partido.equipoVisitante.jugadores[i].meterCuarto(partido.equipoVisitante.jugadores[i].cuarto1)


def crearSegundoCuarto(partido):
    for i in range(len(partido.equipoLocal.jugadores)):
        partido.equipoLocal.jugadores[i].cuarto2 = cuarto.statNormal("2nd Quarter")
        partido.equipoLocal.jugadores[i].meterCuarto(partido.equipoLocal.jugadores[i].cuarto2)
    for i in range(len(partido.equipoVisitante.jugadores)):
        partido.equipoVisitante.jugadores[i].cuarto2 = cuarto.statNormal("2nd Quarter")
        partido.equipoVisitante.jugadores[i].meterCuarto(partido.equipoVisitante.jugadores[i].cuarto2)


def crearTercerCuarto(partido):
    for i in range(len(partido.equipoLocal.jugadores)):
        partido.equipoLocal.jugadores[i].cuarto3 = cuarto.statNormal("3rd Quarter")
        partido.equipoLocal.jugadores[i].meterCuarto(partido.equipoLocal.jugadores[i].cuarto3)
    for i in range(len(partido.equipoVisitante.jugadores)):
        partido.equipoVisitante.jugadores[i].cuarto3 = cuarto.statNormal("3rd Quarter")
        partido.equipoVisitante.jugadores[i].meterCuarto(partido.equipoVisitante.jugadores[i].cuarto3)


def crearCuartoCuarto(partido):
    for i in range(len(partido.equipoLocal.jugadores)):
        partido.equipoLocal.jugadores[i].cuarto4 = cuarto.statNormal("4th Quarter")
        partido.equipoLocal.jugadores[i].meterCuarto(partido.equipoLocal.jugadores[i].cuarto4)
    for i in range(len(partido.equipoVisitante.jugadores)):
        partido.equipoVisitante.jugadores[i].cuarto4 = cuarto.statNormal("4th Quarter")
        partido.equipoVisitante.jugadores[i].meterCuarto(partido.equipoVisitante.jugadores[i].cuarto4)


def crearPrimerOvertime(partido):
    for i in range(len(partido.equipoLocal.jugadores)):
        partido.equipoLocal.jugadores[i].over1 = cuarto.statNormal("1st Overtime")
        partido.equipoLocal.jugadores[i].meterCuarto(partido.equipoLocal.jugadores[i].over1)
    for i in range(len(partido.equipoVisitante.jugadores)):
        partido.equipoVisitante.jugadores[i].over1 = cuarto.statNormal("1st Overtime")
        partido.equipoVisitante.jugadores[i].meterCuarto(partido.equipoVisitante.jugadores[i].over1)


def crearSegundoOvertime(partido):
    for i in range(len(partido.equipoLocal.jugadores)):
        partido.equipoLocal.jugadores[i].over2 = cuarto.statNormal("2nd Overtime")
        partido.equipoLocal.jugadores[i].meterCuarto(partido.equipoLocal.jugadores[i].over2)
    for i in range(len(partido.equipoVisitante.jugadores)):
        partido.equipoVisitante.jugadores[i].over2 = cuarto.statNormal("2nd Overtime")
        partido.equipoVisitante.jugadores[i].meterCuarto(partido.equipoVisitante.jugadores[i].over2)


def crearTercerOvertime(partido):
    for i in range(len(partido.equipoLocal.jugadores)):
        partido.equipoLocal.jugadores[i].over3 = cuarto.statNormal("3rd Overtime")
        partido.equipoLocal.jugadores[i].meterCuarto(partido.equipoLocal.jugadores[i].over3)
    for i in range(len(partido.equipoVisitante.jugadores)):
        partido.equipoVisitante.jugadores[i].over3 = cuarto.statNormal("3rd Overtime")
        partido.equipoVisitante.jugadores[i].meterCuarto(partido.equipoVisitante.jugadores[i].over3)


def crearCuartoOvertime(partido):
    for i in range(len(partido.equipoLocal.jugadores)):
        partido.equipoLocal.jugadores[i].over4 = cuarto.statNormal("4th Overtime")
        partido.equipoLocal.jugadores[i].meterCuarto(partido.equipoLocal.jugadores[i].over4)
    for i in range(len(partido.equipoVisitante.jugadores)):
        partido.equipoVisitante.jugadores[i].over4 = cuarto.statNormal("4th Overtime")
        partido.equipoVisitante.jugadores[i].meterCuarto(partido.equipoVisitante.jugadores[i].over4)


def crearQuintoOvertime(partido):
    for i in range(len(partido.equipoLocal.jugadores)):
        partido.equipoLocal.jugadores[i].over5 = cuarto.statNormal("5th Overtime")
        partido.equipoLocal.jugadores[i].meterCuarto(partido.equipoLocal.jugadores[i].over5)
    for i in range(len(partido.equipoVisitante.jugadores)):
        partido.equipoVisitante.jugadores[i].over5 = cuarto.statNormal("5th Overtime")
        partido.equipoVisitante.jugadores[i].meterCuarto(partido.equipoVisitante.jugadores[i].over5)


def crearSextoOvertime(partido):
    for i in range(len(partido.equipoLocal.jugadores)):
        partido.equipoLocal.jugadores[i].over6 = cuarto.statNormal("6th Overtime")
        partido.equipoLocal.jugadores[i].meterCuarto(partido.equipoLocal.jugadores[i].over6)
    for i in range(len(partido.equipoVisitante.jugadores)):
        partido.equipoVisitante.jugadores[i].over6 = cuarto.statNormal("6th Overtime")
        partido.equipoVisitante.jugadores[i].meterCuarto(partido.equipoVisitante.jugadores[i].over6)


################################################################################
####  FUNCION QUE NOS INDICA EN QUE CUARTO ESTAMOS EMPEZANDO A JUGAR        ####
################################################################################
def cuartoJugando(texto, partido):
    # print texto
    if "Start of 2nd quarter" in texto or "End of 1st quarter" in texto:
        crearSegundoCuarto(partido)
        # print "*************************************"
        # print "****     EMPEZAMOS CUARTO 2      ****"
        # print "*************************************\n"
    if "Start of 3rd quarter" in texto or "End of 2nd quarter" in texto:
        crearTercerCuarto(partido)
        # print "*************************************"
        # print "****     EMPEZAMOS CUARTO 3      ****"
        # print "*************************************\n"
    if "End of 3rd quarter" in texto or "Start of 4th quarter" in texto:
        crearCuartoCuarto(partido)
        # print "*************************************"
        # print "****     EMPEZAMOS CUARTO 4      ****"
        # print "*************************************\n"
    if "Start of 1st overtime" in texto:
        crearPrimerOvertime(partido)
        # print "*************************************"
        # print "****    EMPEZAMOS PRORROGA 1     ****"
        # print "*************************************\n"
    if "Start of 2nd overtime" in texto:
        crearSegundoOvertime(partido)
        # print "*************************************"
        # print "****    EMPEZAMOS PRORROGA 2     ****"
        # print "*************************************\n"
    if "Start of 3rd overtime" in texto:
        crearTercerOvertime(partido)
        # print "*************************************"
        # print "****    EMPEZAMOS PRORROGA 3     ****"
        # print "*************************************\n"
    if "Start of 4th overtime" in texto:
        crearCuartoOvertime(partido)
        # print "*************************************"
        # print "****    EMPEZAMOS PRORROGA 4     ****"
        # print "*************************************\n"
    if "Start of 5th overtime" in texto:
        crearQuintoOvertime(partido)
        # print "*************************************"
        # print "****    EMPEZAMOS PRORROGA 5     ****"
        # print "*************************************\n"
    if "Start of 6th overtime" in texto:
        crearSextoOvertime(partido)
        # print "*************************************"
        # print "****    EMPEZAMOS PRORROGA 6     ****"
        # print "*************************************\n"


# #    ABRA QUE REVISAR CUANTOS CUARTOS TIENE EL PARTIDO, ES POR ELLO QUE TENEMOS UN BOCETO QUE NOS DICE EL ANCHO DE CADA CUARTO DEPENDIENDO
# #    LOS CUARTOS JUGADOS EN ESE PARTIDO
#################################################################################################
####  EN LA PAGINA DE MAS/MESNO, TENEMOS QUE SABER CUANTOS CUARTOS ESTAMOS JUGANDO           ####
####  PARA SABER EL ANCHO QUE NOS OCUPA CADA CUARTO EN LA TABLA                              ####
#################################################################################################
def devolverCuarto(ancho):
    global cuartoActual
    if ancho < 250:
        cuartoActual = 1
        return "1"
    elif ancho < 500:
        cuartoActual = 2
        return "2"
    elif ancho < 750:
        cuartoActual = 3
        return "3"
    elif ancho < 1000:
        cuartoActual = 4
        return "4"


def devolverCuarto1Prorrogas(ancho):
    global cuartoActual
    if ancho < 227:
        cuartoActual = 1
        return "1"
    elif ancho < 453:
        cuartoActual = 2
        return "2"
    elif ancho < 679:
        cuartoActual = 3
        return "3"
    elif ancho < 905:
        cuartoActual = 4
        return "4"
    elif ancho < 1001:
        cuartoActual = 5
        return "5"


def devolverCuarto2Prorrogas(ancho):
    global cuartoActual
    if ancho < 208:
        cuartoActual = 1
        return "1"
    elif ancho < 416:
        cuartoActual = 2
        return "2"
    elif ancho < 623:
        cuartoActual = 3
        return "3"
    elif ancho < 830:
        cuartoActual = 4
        return "4"
    elif ancho < 916:
        cuartoActual = 5
        return "5"
    elif ancho < 1001:
        cuartoActual = 6
        return "6"


def devolverCuarto3Prorrogas(ancho):
    global cuartoActual
    if ancho < 191:
        cuartoActual = 1
        return "1"
    elif ancho < 382:
        cuartoActual = 2
        return "2"
    elif ancho < 572:
        cuartoActual = 3
        return "3"
    elif ancho < 762:
        cuartoActual = 4
        return "4"
    elif ancho < 841:
        cuartoActual = 5
        return "5"
    elif ancho < 920:
        cuartoActual = 6
        return "6"
    elif ancho < 1001:
        cuartoActual = 7
        return "7"


def devolverCuarto4Prorrogas(ancho):
    global cuartoActual
    if ancho < 177:
        cuartoActual = 1
        return "1"
    elif ancho < 354:
        cuartoActual = 2
        return "2"
    elif ancho < 531:
        cuartoActual = 3
        return "3"
    elif ancho < 708:
        cuartoActual = 4
        return "4"
    elif ancho < 780:
        cuartoActual = 5
        return "5"
    elif ancho < 854:
        cuartoActual = 6
        return "6"
    elif ancho < 928:
        cuartoActual = 7
        return "7"
    elif ancho < 1001:
        cuartoActual = 8
        return "8"


#################################################################################################
####  FUNCION QUE NOS DEUVUELVE EL MAS MENOS DE LOS JUGADORES EN LOS PARTIDOS                ####
#################################################################################################
def devolverMasMenosJugadores(partido, soup):
    listaJugadores = []

    numeroCuartos = 4

    # #    SACAMOS LOS NÚMEROS DE CUARTOS QUE TENEMOS
    selector = '.header'
    for div in soup.select(selector):
        divisor = str(div).split('\n')
        numeroCuartos = len(divisor) - 2
    print 'Número de cuartos jugados: ' + str(numeroCuartos)
    partido.numeroCuartos = numeroCuartos

    selector = '.player'
    contador = 1
    for div in soup.select(selector):
        # print 'Jugador número: ' + str(contador)
        size = int(len(div.text.split(' ')))
        if size == 7:
            listaJugadores.append(div.text.split(' ')[0])
        elif size == 8:
            listaJugadores.append(div.text.split(' ')[0] + ' ' + div.text.split(' ')[1])
        elif size == 9:
            listaJugadores.append(div.text.split(' ')[0] + ' ' + div.text.split(' ')[1] + ' ' + div.text.split(' ')[2])
        elif size == 10:
            listaJugadores.append(div.text.split(' ')[0] + ' ' + div.text.split(' ')[1] + ' ' + div.text.split(' ')[2] + ' ' + div.text.split(' ')[3])
        contador += 1

    cuartoActual = 0
    selector = '.player-plusminus'
    contador = 0
    primerCuarto = 0
    segundoCuarto = 0
    tercerCuarto = 0
    cuartoCuarto = 0
    primerProrroga = 0
    segundaProrroga = 0
    terceraProrroga = 0
    cuartaProrroga = 0
    for div in soup.select(selector):
        # print 'Jugador número: ' + listaJugadores[contador] + ' '
        player = devolverJugadorMasMenos(partido.equipoLocal.jugadores, partido.equipoVisitante.jugadores, devolverCorrecto(listaJugadores[contador]))
        divisor = str(div).replace('<div class="player-plusminus">', '').replace('<div style="width:', '').replace('<div class="minus" style="width:', '').replace('<div class="plus" style="width:', '').replace('</div>', '').replace('<div class="even" style="width:', '').replace(';"> ', '').replace('\n', ' ').replace('px;">', ' ')
        sumatorioAncho = 0
        for i in divisor.split(' '):
            i = i.replace(' ', '').replace('\n', '')
            if i != '':
                if '+' in i or '-' in i or '0' == i:
                    global cuartoActual
                    if numeroCuartos == 4:
                        devolverCuarto(sumatorioAncho)
                    elif numeroCuartos == 5:
                        devolverCuarto1Prorrogas(sumatorioAncho)
                    elif numeroCuartos == 6:
                        devolverCuarto2Prorrogas(sumatorioAncho)
                    elif numeroCuartos == 7:
                        devolverCuarto3Prorrogas(sumatorioAncho)
                    elif numeroCuartos == 8:
                        devolverCuarto4Prorrogas(sumatorioAncho)

                    if cuartoActual == 1:
                        primerCuarto += int(i)
                    elif cuartoActual == 2:
                        segundoCuarto += int(i)
                    elif cuartoActual == 3:
                        tercerCuarto += int(i)
                    elif cuartoActual == 4:
                        cuartoCuarto += int(i)
                    elif cuartoActual == 5:
                        primerProrroga += int(i)
                    elif cuartoActual == 6:
                        segundaProrroga += int(i)
                    elif cuartoActual == 7:
                        terceraProrroga += int(i)
                    elif cuartoActual == 8:
                        cuartaProrroga += int(i)
                else:
                    # print 'Ancho: '+i+' px'
                    sumatorioAncho += int(i)
        contador += 1
        total = primerCuarto + segundoCuarto + tercerCuarto + cuartoCuarto + primerProrroga + segundaProrroga + terceraProrroga + cuartaProrroga
        # print '1º Cuarto:   ' + str(primerCuarto)
        player.cuarto1.masMenos = primerCuarto
        # print '2º Cuarto:   ' + str(segundoCuarto)
        player.cuarto2.masMenos = segundoCuarto
        # print '3º Cuarto:   ' + str(tercerCuarto)
        player.cuarto3.masMenos = tercerCuarto
        # print '4º Cuarto:   ' + str(cuartoCuarto)
        player.cuarto4.masMenos = cuartoCuarto
        if numeroCuartos > 4:
            # print '1º Overtime: ' + str(primerProrroga)
            player.over1.masMenos = primerProrroga
        if numeroCuartos > 5:
            # print '2º Overtime: ' + str(segundaProrroga)
            player.over2.masMenos = segundaProrroga
        if numeroCuartos > 6:
            # print '3º Overtime: ' + str(terceraProrroga)
            player.over3.masMenos = terceraProrroga
        if numeroCuartos > 7:
            # print '4º Overtime: ' + str(cuartaProrroga)
            player.over4.masMenos = cuartaProrroga

        # print 'Total:       ' + str(total)
        primerCuarto = 0
        segundoCuarto = 0
        tercerCuarto = 0
        cuartoCuarto = 0
        primerProrroga = 0
        segundaProrroga = 0
        terceraProrroga = 0
        cuartaProrroga = 0
    return partido


###################################################
####  FUNCION QUE BUSCA EL JUGADOR             ####
###################################################
def devolverJugadorMasMenos(local, visitante, jugador):
    print "BUSCANDO: " + jugador
    if "Nene" in jugador:
        print "paramos"
        jugador = "Nene Hilario"
        for i in local:
            if i.id in "hilarne01":
                i.nombre = "Nene"
                i.apellido = "Hilario"
    
        for i in visitante:
            if i.id in "hilarne01":
                i.nombre = "Nene"
                i.apellido = "Hilario"
                
    if "Jeffery Taylor" in jugador:
        print "paramos"
        jugador = "Jeff Taylor"
        
    if "Gigi" in jugador:
        print "paramos"
            
    if "Jr." in jugador:
        jugador = jugador[0:-4]
    if "Jr" in jugador:
        jugador = jugador[0:-3]
    if "III" in jugador:
        jugador = jugador[0:-4]
    if "II" in jugador:
        jugador = jugador[0:-3]
    if "IV" in jugador:
        jugador = jugador[0:-3]
    if "Sr." in jugador:
        jugador = jugador[0:-4]

    # print jugador
    if " Mbenga" in jugador:
        jugador = "Didier Ilunga-Mbenga"
    elif jugador == "Tim Hardaway Jr.":
        jugador = "Tim Hardaway"
    elif jugador == "Glenn Robinson III":
        jugador = "Glenn Robinson"
    elif jugador == "Larry Nance Jr.":
        jugador = "Larry Nance"
    elif jugador == "Gary Payton II":
        jugador = "Gary Payton"
    elif jugador == "Taurean Prince":
        jugador = "Taurean Prince"
    elif jugador == "Wendell Carter Jr.":
        jugador = "Wendell Carter"
    elif jugador == "Derrick Jones Jr.":
        jugador = "Derrick Jones"
    elif jugador == "Jaren Jackson Jr.":
        jugador = "Jaren Jackson"
    # elif jugador == "Mo Bamba":
        # jugador = "Mohamed Bamba"
    # elif jugador == "Gigi Datome":
        # jugador = "Luigi Datome"
    elif jugador == "Jeff Taylor":
        jugador = "Jeff Taylor"
    elif jugador == "Efthimis Rentzias":
        jugador = "Efthimi Rentzias"
    # elif jugador == "Vitor Luiz Faverani":
        # jugador = "Vitor Faverani"
    elif jugador == "Xavier Tillman Sr.":
        jugador = "Xavier Tillman"
    elif jugador == "Didi Louzada":
        jugador = "Marcos Louzada Silva"
    elif jugador == "Aleksandar Djordjevic":
        jugador = "Aleksandar Dordevic";
    elif jugador == "Kiwane Lemorris Garris":
        jugador = "Kiwane Garris"

    for i in local:
        nombre = i.nombre + " " + i.apellido
        # print "Nombre:  "+nombre
        if jugador in nombre:
            # print "     Nombre Encontrado :"+nombre+"   "+jugador
            return i

    for i in visitante:
        nombre = i.nombre + " " + i.apellido
        # print "Nombre:  "+nombre
        if jugador in nombre:
            # print "     Nombre Encontrado :"+nombre+"   "+jugador
            return  i


#######################################################################
####  FUNCION PARA RECOGER DATOS EXTRAS DEL CADA PARTIDO           ####
#######################################################################
def recogerLideratosPartido(pagina, partido):
    pagina.replace('<!--', '').replace('-->', '')
    div = pagina.split('<tr ><th scope="row" class="right " data-stat="field" >')
    # print "####################################################"
    # print "Ties:          "
    partido.empates = devolverFormato(str(div[1].split('>'))[54:-20])
    # print "####################################################"
    # print "Lead changes:  "
    partido.cambiosLider = devolverFormato(str(div[2].split('>'))[62:-20])
    # print "####################################################"
    # print "Game tied:     "
    partido.tiempoEmpate = devolverSegundos(devolverFormato(str(div[3].split('>'))[59:-20]))
    # print "####################################################"
    # print "Visitor led:   "
    partido.tiempoVisitanteGanando = devolverSegundos(devolverFormato(str(div[4].split('>'))[-27:-20]))
    partido.equipoVisitante.tiempoLider = devolverSegundos(devolverFormato(str(div[4].split('>'))[-27:-20]))
    # print "####################################################"
    # print "Local led:     "
    partido.tiempoLocalGanando = devolverSegundos(devolverFormato(str(div[5].split('>'))[-170:-163]))
    partido.equipoLocal.tiempoLider = devolverSegundos(devolverFormato(str(div[5].split('>'))[-170:-163]))
    # print "####################################################"
    # print "Visitor Most Consecutive Points:   "
    partido.visitantePuntosConsecutivos = devolverFormato(str(str(div[6].split('>'))[-22:-20]))
    partido.equipoVisitante.puntosConsecutivos = devolverFormato(str(str(div[6].split('>'))[-22:-20]))
    # print "####################################################"
    # print "Local Most Consecutive Points:     "
    partido.localPuntosConsecutivos = devolverFormato(str(str(div[7].split('>'))[-165:-163]))
    partido.equipoLocal.puntosConsecutivos = devolverFormato(str(str(div[7].split('>'))[-165:-163]))
    # print "####################################################"
    # print "Visitor longest Scoring Drought:   "
    partido.visitanteSinAnotar = devolverSegundos(devolverFormato(str(str(div[8].split('>'))[-27:-20])))
    partido.equipoVisitante.sinAnotar = devolverSegundos(devolverFormato(str(str(div[8].split('>'))[-27:-20])))
    # print "####################################################"
    # print "Local longest Scoring Drought:     "
    partido.localSinAnotar = devolverSegundos(devolverFormato(str(str(div[9].split('>'))[-162:-155])))
    partido.equipoLocal.sinAnotar = devolverSegundos(devolverFormato(str(str(div[9].split('>'))[-162:-155])))
    return partido


#################################################################################################
####  FUNCION QUE NOS DEVUELVE UNA CADENA FORMATEADA   EJ. TENEMOS 3:45.3                    ####
####  PARA CALCULAR LOS SEGUNDOS QUITAMOS EL ULTIMO .3 QUEDANDONOS SOLO CON EL 3:45          ####
#################################################################################################
def devolverFormato(cadena):
    return cadena.replace("'", "").replace(".0", "").replace(" ", "").replace(".1", "").replace(".2", "").replace(".3", "").replace(".4", "").replace(".5", "").replace(".6", "").replace(".7", "").replace(".8", "").replace(".9", "")


############################################################
####  FUNCION QUE NOS DEVUELVE LOS SEGUNDOS             ####
############################################################
def devolverSegundos(cadena):
    valores = cadena.split(":")
    return int(valores[0]) * 60 + int(valores[1])


################################################################################
####  FUNCION QUE COMPLETA LAS ESTADISTICAS DEL PARTIDO DE UN JUGADOR       ####
################################################################################
def completarFullBoxscoreJugador(partido):
    for jugador in partido.equipoLocal.jugadores:
        for cuarto in jugador.estadisticasCuarto:
            jugador.fullBox.tirosCampoMetidos = jugador.fullBox.tirosCampoMetidos + cuarto.tirosCampoMetidos
            jugador.fullBox.tirosCampoIntentados = jugador.fullBox.tirosCampoIntentados + cuarto.tirosCampoIntentados
            jugador.fullBox.triplesMetidos = jugador.fullBox.triplesMetidos + cuarto.triplesMetidos
            jugador.fullBox.triplesIntentados = jugador.fullBox.triplesIntentados + cuarto.triplesIntentados
            jugador.fullBox.tirosLibresMetidos = jugador.fullBox.tirosLibresMetidos + cuarto.tirosLibresMetidos
            jugador.fullBox.tirosLibresIntentados = jugador.fullBox.tirosLibresIntentados + cuarto.tirosLibresIntentados
            jugador.fullBox.reboteOfensivo = jugador.fullBox.reboteOfensivo + cuarto.reboteOfensivo
            jugador.fullBox.reboteDefensivo = jugador.fullBox.reboteDefensivo + cuarto.reboteDefensivo
            jugador.fullBox.totalRebotes = jugador.fullBox.totalRebotes + cuarto.totalRebotes
            jugador.fullBox.asistencias = jugador.fullBox.asistencias + cuarto.asistencias
            jugador.fullBox.robos = jugador.fullBox.robos + cuarto.robos
            jugador.fullBox.tapones = jugador.fullBox.tapones + cuarto.tapones
            jugador.fullBox.taponRecibido = jugador.fullBox.taponRecibido + cuarto.taponRecibido
            jugador.fullBox.taponRecibidoTriple = jugador.fullBox.taponRecibidoTriple + cuarto.taponRecibidoTriple
            jugador.fullBox.perdidas = jugador.fullBox.perdidas + cuarto.perdidas
            jugador.fullBox.perdidaPasos = jugador.fullBox.perdidaPasos + cuarto.perdidaPasos
            jugador.fullBox.perdidaMalPase = jugador.fullBox.perdidaMalPase + cuarto.perdidaMalPase
            jugador.fullBox.perdidaFueraBanda = jugador.fullBox.perdidaFueraBanda + cuarto.perdidaFueraBanda
            jugador.fullBox.perdidaBalonPerdido = jugador.fullBox.perdidaBalonPerdido + cuarto.perdidaBalonPerdido
            jugador.fullBox.perdidaPisarFuera = jugador.fullBox.perdidaPisarFuera + cuarto.perdidaPisarFuera
            jugador.fullBox.perdidaGoaltending = jugador.fullBox.perdidaGoaltending + cuarto.perdidaGoaltending
            jugador.fullBox.faltaPersonalDefensa = jugador.fullBox.faltaPersonalDefensa + cuarto.faltaPersonalDefensa
            jugador.fullBox.faltaPersonalProvocadaEnDefensa = jugador.fullBox.faltaPersonalProvocadaEnDefensa + cuarto.faltaPersonalProvocadaEnDefensa
            jugador.fullBox.faltaPersonalAtaque = jugador.fullBox.faltaPersonalAtaque + cuarto.faltaPersonalAtaque
            jugador.fullBox.faltaPersonalProvocadaEnAtaque = jugador.fullBox.faltaPersonalProvocadaEnAtaque + cuarto.faltaPersonalProvocadaEnAtaque
            jugador.fullBox.faltaPersonalTiro = jugador.fullBox.faltaPersonalTiro + cuarto.faltaPersonalTiro
            jugador.fullBox.faltaPersonalProvocadaEnTiro = jugador.fullBox.faltaPersonalProvocadaEnTiro + cuarto.faltaPersonalProvocadaEnTiro
            jugador.fullBox.faltaTecnica = jugador.fullBox.faltaTecnica + cuarto.faltaTecnica
            jugador.fullBox.faltasPersonales = jugador.fullBox.faltasPersonales + cuarto.faltasPersonales
            jugador.fullBox.faltasPersonalesProvocadas = jugador.fullBox.faltasPersonalesProvocadas + cuarto.faltasPersonalesProvocadas
            jugador.fullBox.puntos = jugador.fullBox.puntos + cuarto.puntos
            jugador.fullBox.masMenos = jugador.fullBox.masMenos + cuarto.masMenos
            jugador.fullBox.mate = jugador.fullBox.mate + cuarto.mate
            jugador.fullBox.mateFallado = jugador.fullBox.mateFallado + cuarto.mateFallado
            jugador.fullBox.suspension = jugador.fullBox.suspension + cuarto.suspension
            jugador.fullBox.suspensionFallado = jugador.fullBox.suspensionFallado + cuarto.suspensionFallado
            jugador.fullBox.bandeja = jugador.fullBox.bandeja + cuarto.bandeja
            jugador.fullBox.bandejaFallada = jugador.fullBox.bandejaFallada + cuarto.bandejaFallada
            jugador.fullBox.gancho = jugador.fullBox.gancho + cuarto.gancho
            jugador.fullBox.ganchoFallado = jugador.fullBox.ganchoFallado + cuarto.ganchoFallado
            jugador.fullBox.primerTiroLibreDentro = jugador.fullBox.primerTiroLibreDentro + cuarto.primerTiroLibreDentro
            jugador.fullBox.primerTiroLibreFuera = jugador.fullBox.primerTiroLibreFuera + cuarto.primerTiroLibreFuera
            jugador.fullBox.primerTiroLibreTotal = jugador.fullBox.primerTiroLibreTotal + cuarto.primerTiroLibreTotal
            jugador.fullBox.segundoTiroLibreDentro = jugador.fullBox.segundoTiroLibreDentro + cuarto.segundoTiroLibreDentro
            jugador.fullBox.segundoTiroLibreFuera = jugador.fullBox.segundoTiroLibreFuera + cuarto.segundoTiroLibreFuera
            jugador.fullBox.segundoTiroLibreTotal = jugador.fullBox.segundoTiroLibreTotal + cuarto.segundoTiroLibreTotal
            jugador.fullBox.tercerTiroLibreDentro = jugador.fullBox.tercerTiroLibreDentro + cuarto.tercerTiroLibreDentro
            jugador.fullBox.tercerTiroLibreFuera = jugador.fullBox.tercerTiroLibreFuera + cuarto.tercerTiroLibreFuera
            jugador.fullBox.tercerTiroLibreTotal = jugador.fullBox.tercerTiroLibreTotal + cuarto.tercerTiroLibreTotal
        del jugador.estadisticasCuarto
    jugador.fullBox.completarEstadisticas()
    jugador.fullBox.completarPorcentajes()

    for jugador in partido.equipoVisitante.jugadores:
        for cuarto in jugador.estadisticasCuarto:
            jugador.fullBox.tirosCampoMetidos = jugador.fullBox.tirosCampoMetidos + cuarto.tirosCampoMetidos
            jugador.fullBox.tirosCampoIntentados = jugador.fullBox.tirosCampoIntentados + cuarto.tirosCampoIntentados
            jugador.fullBox.triplesMetidos = jugador.fullBox.triplesMetidos + cuarto.triplesMetidos
            jugador.fullBox.triplesIntentados = jugador.fullBox.triplesIntentados + cuarto.triplesIntentados
            jugador.fullBox.tirosLibresMetidos = jugador.fullBox.tirosLibresMetidos + cuarto.tirosLibresMetidos
            jugador.fullBox.tirosLibresIntentados = jugador.fullBox.tirosLibresIntentados + cuarto.tirosLibresIntentados
            jugador.fullBox.reboteOfensivo = jugador.fullBox.reboteOfensivo + cuarto.reboteOfensivo
            jugador.fullBox.reboteDefensivo = jugador.fullBox.reboteDefensivo + cuarto.reboteDefensivo
            jugador.fullBox.totalRebotes = jugador.fullBox.totalRebotes + cuarto.totalRebotes
            jugador.fullBox.asistencias = jugador.fullBox.asistencias + cuarto.asistencias
            jugador.fullBox.robos = jugador.fullBox.robos + cuarto.robos
            jugador.fullBox.tapones = jugador.fullBox.tapones + cuarto.tapones
            jugador.fullBox.taponRecibido = jugador.fullBox.taponRecibido + cuarto.taponRecibido
            jugador.fullBox.taponRecibidoTriple = jugador.fullBox.taponRecibidoTriple + cuarto.taponRecibidoTriple
            jugador.fullBox.perdidas = jugador.fullBox.perdidas + cuarto.perdidas
            jugador.fullBox.perdidaPasos = jugador.fullBox.perdidaPasos + cuarto.perdidaPasos
            jugador.fullBox.perdidaMalPase = jugador.fullBox.perdidaMalPase + cuarto.perdidaMalPase
            jugador.fullBox.perdidaFueraBanda = jugador.fullBox.perdidaFueraBanda + cuarto.perdidaFueraBanda
            jugador.fullBox.perdidaBalonPerdido = jugador.fullBox.perdidaBalonPerdido + cuarto.perdidaBalonPerdido
            jugador.fullBox.perdidaPisarFuera = jugador.fullBox.perdidaPisarFuera + cuarto.perdidaPisarFuera
            jugador.fullBox.perdidaGoaltending = jugador.fullBox.perdidaGoaltending + cuarto.perdidaGoaltending
            jugador.fullBox.faltaPersonalDefensa = jugador.fullBox.faltaPersonalDefensa + cuarto.faltaPersonalDefensa
            jugador.fullBox.faltaPersonalProvocadaEnDefensa = jugador.fullBox.faltaPersonalProvocadaEnDefensa + cuarto.faltaPersonalProvocadaEnDefensa
            jugador.fullBox.faltaPersonalAtaque = jugador.fullBox.faltaPersonalAtaque + cuarto.faltaPersonalAtaque
            jugador.fullBox.faltaPersonalProvocadaEnAtaque = jugador.fullBox.faltaPersonalProvocadaEnAtaque + cuarto.faltaPersonalProvocadaEnAtaque
            jugador.fullBox.faltaPersonalTiro = jugador.fullBox.faltaPersonalTiro + cuarto.faltaPersonalTiro
            jugador.fullBox.faltaPersonalProvocadaEnTiro = jugador.fullBox.faltaPersonalProvocadaEnTiro + cuarto.faltaPersonalProvocadaEnTiro
            jugador.fullBox.faltaTecnica = jugador.fullBox.faltaTecnica + cuarto.faltaTecnica
            jugador.fullBox.faltasPersonales = jugador.fullBox.faltasPersonales + cuarto.faltasPersonales
            jugador.fullBox.faltasPersonalesProvocadas = jugador.fullBox.faltasPersonalesProvocadas + cuarto.faltasPersonalesProvocadas
            jugador.fullBox.puntos = jugador.fullBox.puntos + cuarto.puntos
            jugador.fullBox.masMenos = jugador.fullBox.masMenos + cuarto.masMenos
            jugador.fullBox.mate = jugador.fullBox.mate + cuarto.mate
            jugador.fullBox.mateFallado = jugador.fullBox.mateFallado + cuarto.mateFallado
            jugador.fullBox.suspension = jugador.fullBox.suspension + cuarto.suspension
            jugador.fullBox.suspensionFallado = jugador.fullBox.suspensionFallado + cuarto.suspensionFallado
            jugador.fullBox.bandeja = jugador.fullBox.bandeja + cuarto.bandeja
            jugador.fullBox.bandejaFallada = jugador.fullBox.bandejaFallada + cuarto.bandejaFallada
            jugador.fullBox.gancho = jugador.fullBox.gancho + cuarto.gancho
            jugador.fullBox.ganchoFallado = jugador.fullBox.ganchoFallado + cuarto.ganchoFallado
            jugador.fullBox.primerTiroLibreDentro = jugador.fullBox.primerTiroLibreDentro + cuarto.primerTiroLibreDentro
            jugador.fullBox.primerTiroLibreFuera = jugador.fullBox.primerTiroLibreFuera + cuarto.primerTiroLibreFuera
            jugador.fullBox.primerTiroLibreTotal = jugador.fullBox.primerTiroLibreTotal + cuarto.primerTiroLibreTotal
            jugador.fullBox.segundoTiroLibreDentro = jugador.fullBox.segundoTiroLibreDentro + cuarto.segundoTiroLibreDentro
            jugador.fullBox.segundoTiroLibreFuera = jugador.fullBox.segundoTiroLibreFuera + cuarto.segundoTiroLibreFuera
            jugador.fullBox.segundoTiroLibreTotal = jugador.fullBox.segundoTiroLibreTotal + cuarto.segundoTiroLibreTotal
            jugador.fullBox.tercerTiroLibreDentro = jugador.fullBox.tercerTiroLibreDentro + cuarto.tercerTiroLibreDentro
            jugador.fullBox.tercerTiroLibreFuera = jugador.fullBox.tercerTiroLibreFuera + cuarto.tercerTiroLibreFuera
            jugador.fullBox.tercerTiroLibreTotal = jugador.fullBox.tercerTiroLibreTotal + cuarto.tercerTiroLibreTotal
        del jugador.estadisticasCuarto
    jugador.fullBox.completarEstadisticas()
    jugador.fullBox.completarPorcentajes()
    return partido


################################################################################
####  FUNCION QUE COMPLETA LAS ESTADISTICAS DEL PARTIDO DEL EQUIO LOCAL     ####
################################################################################
def completarFullBoxScoreLocal(partido):
    fullStatLocal = cuarto.statNormal("Full Boxscore Local")
    for jugadorLocal in partido.equipoLocal.jugadores:
        fullStatLocal.tirosCampoMetidos = fullStatLocal.tirosCampoMetidos + jugadorLocal.fullBox.tirosCampoMetidos
        fullStatLocal.tirosCampoIntentados = fullStatLocal.tirosCampoIntentados + jugadorLocal.fullBox.tirosCampoIntentados
        fullStatLocal.triplesMetidos = fullStatLocal.triplesMetidos + jugadorLocal.fullBox.triplesMetidos
        fullStatLocal.triplesIntentados = fullStatLocal.triplesIntentados + jugadorLocal.fullBox.triplesIntentados
        fullStatLocal.tirosLibresMetidos = fullStatLocal.tirosLibresMetidos + jugadorLocal.fullBox.tirosLibresMetidos
        fullStatLocal.tirosLibresIntentados = fullStatLocal.tirosLibresIntentados + jugadorLocal.fullBox.tirosLibresIntentados
        fullStatLocal.reboteOfensivo = fullStatLocal.reboteOfensivo + jugadorLocal.fullBox.reboteOfensivo
        fullStatLocal.reboteDefensivo = fullStatLocal.reboteDefensivo + jugadorLocal.fullBox.reboteDefensivo
        fullStatLocal.totalRebotes = fullStatLocal.totalRebotes + jugadorLocal.fullBox.totalRebotes
        fullStatLocal.asistencias = fullStatLocal.asistencias + jugadorLocal.fullBox.asistencias
        fullStatLocal.robos = fullStatLocal.robos + jugadorLocal.fullBox.robos
        fullStatLocal.tapones = fullStatLocal.tapones + jugadorLocal.fullBox.tapones
        fullStatLocal.taponRecibido = fullStatLocal.taponRecibido + jugadorLocal.fullBox.taponRecibido
        fullStatLocal.taponRecibidoTriple = fullStatLocal.taponRecibidoTriple + jugadorLocal.fullBox.taponRecibidoTriple
        fullStatLocal.perdidas = fullStatLocal.perdidas + jugadorLocal.fullBox.perdidas
        fullStatLocal.perdidaPasos = fullStatLocal.perdidaPasos + jugadorLocal.fullBox.perdidaPasos
        fullStatLocal.perdidaMalPase = fullStatLocal.perdidaMalPase + jugadorLocal.fullBox.perdidaMalPase
        fullStatLocal.perdidaFueraBanda = fullStatLocal.perdidaFueraBanda + jugadorLocal.fullBox.perdidaFueraBanda
        fullStatLocal.perdidaBalonPerdido = fullStatLocal.perdidaBalonPerdido + jugadorLocal.fullBox.perdidaBalonPerdido
        fullStatLocal.perdidaPisarFuera = fullStatLocal.perdidaPisarFuera + jugadorLocal.fullBox.perdidaPisarFuera
        fullStatLocal.perdidaGoaltending = fullStatLocal.perdidaGoaltending + jugadorLocal.fullBox.perdidaGoaltending
        fullStatLocal.faltaPersonalDefensa = fullStatLocal.faltaPersonalDefensa + jugadorLocal.fullBox.faltaPersonalDefensa
        fullStatLocal.faltaPersonalProvocadaEnDefensa = fullStatLocal.faltaPersonalProvocadaEnDefensa + jugadorLocal.fullBox.faltaPersonalProvocadaEnDefensa
        fullStatLocal.faltaPersonalAtaque = fullStatLocal.faltaPersonalAtaque + jugadorLocal.fullBox.faltaPersonalAtaque
        fullStatLocal.faltaPersonalProvocadaEnAtaque = fullStatLocal.faltaPersonalProvocadaEnAtaque + jugadorLocal.fullBox.faltaPersonalProvocadaEnAtaque
        fullStatLocal.faltaPersonalTiro = fullStatLocal.faltaPersonalTiro + jugadorLocal.fullBox.faltaPersonalTiro
        fullStatLocal.faltaPersonalProvocadaEnTiro = fullStatLocal.faltaPersonalProvocadaEnTiro + jugadorLocal.fullBox.faltaPersonalProvocadaEnTiro
        fullStatLocal.faltaTecnica = fullStatLocal.faltaTecnica + jugadorLocal.fullBox.faltaTecnica
        fullStatLocal.faltasPersonales = fullStatLocal.faltasPersonales + jugadorLocal.fullBox.faltasPersonales
        fullStatLocal.faltasPersonalesProvocadas = fullStatLocal.faltasPersonalesProvocadas + jugadorLocal.fullBox.faltasPersonalesProvocadas
        fullStatLocal.puntos = fullStatLocal.puntos + jugadorLocal.fullBox.puntos
        fullStatLocal.masMenos = fullStatLocal.masMenos + jugadorLocal.fullBox.masMenos
        fullStatLocal.mate = fullStatLocal.mate + jugadorLocal.fullBox.mate
        fullStatLocal.mateFallado = fullStatLocal.mateFallado + jugadorLocal.fullBox.mateFallado
        fullStatLocal.suspension = fullStatLocal.suspension + jugadorLocal.fullBox.suspension
        fullStatLocal.suspensionFallado = fullStatLocal.suspensionFallado + jugadorLocal.fullBox.suspensionFallado
        fullStatLocal.bandeja = fullStatLocal.bandeja + jugadorLocal.fullBox.bandeja
        fullStatLocal.bandejaFallada = fullStatLocal.bandejaFallada + jugadorLocal.fullBox.bandejaFallada
        fullStatLocal.gancho = fullStatLocal.gancho + jugadorLocal.fullBox.gancho
        fullStatLocal.ganchoFallado = fullStatLocal.ganchoFallado + jugadorLocal.fullBox.ganchoFallado
        fullStatLocal.primerTiroLibreDentro = fullStatLocal.primerTiroLibreDentro + jugadorLocal.fullBox.primerTiroLibreDentro
        fullStatLocal.primerTiroLibreFuera = fullStatLocal.primerTiroLibreFuera + jugadorLocal.fullBox.primerTiroLibreFuera
        fullStatLocal.primerTiroLibreTotal = fullStatLocal.primerTiroLibreTotal + jugadorLocal.fullBox.primerTiroLibreTotal
        fullStatLocal.segundoTiroLibreDentro = fullStatLocal.segundoTiroLibreDentro + jugadorLocal.fullBox.segundoTiroLibreDentro
        fullStatLocal.segundoTiroLibreFuera = fullStatLocal.segundoTiroLibreFuera + jugadorLocal.fullBox.segundoTiroLibreFuera
        fullStatLocal.segundoTiroLibreTotal = fullStatLocal.segundoTiroLibreTotal + jugadorLocal.fullBox.segundoTiroLibreTotal
        fullStatLocal.tercerTiroLibreDentro = fullStatLocal.tercerTiroLibreDentro + jugadorLocal.fullBox.tercerTiroLibreDentro
        fullStatLocal.tercerTiroLibreFuera = fullStatLocal.tercerTiroLibreFuera + jugadorLocal.fullBox.tercerTiroLibreFuera
        fullStatLocal.tercerTiroLibreTotal = fullStatLocal.tercerTiroLibreTotal + jugadorLocal.fullBox.tercerTiroLibreTotal
    partido.equipoLocal.fullBoxscore = fullStatLocal
    partido.equipoLocal.fullBoxscore.completarEstadisticas()
    partido.equipoLocal.fullBoxscore.completarPorcentajes()
    return partido


###################################################################################
####  FUNCION QUE COMPLETA LAS ESTADISTICAS DEL PARTIDO DEL EQUIPO VISITANTE    ###
###################################################################################
def completarFullBoxScoreVisitante(partido):
    fullStatVisitante = cuarto.statNormal("Full Boxscore Visitante")
    for jugadorVisitante in partido.equipoVisitante.jugadores:
        fullStatVisitante.tirosCampoMetidos = fullStatVisitante.tirosCampoMetidos + jugadorVisitante.fullBox.tirosCampoMetidos
        fullStatVisitante.tirosCampoIntentados = fullStatVisitante.tirosCampoIntentados + jugadorVisitante.fullBox.tirosCampoIntentados
        fullStatVisitante.triplesMetidos = fullStatVisitante.triplesMetidos + jugadorVisitante.fullBox.triplesMetidos
        fullStatVisitante.triplesIntentados = fullStatVisitante.triplesIntentados + jugadorVisitante.fullBox.triplesIntentados
        fullStatVisitante.tirosLibresMetidos = fullStatVisitante.tirosLibresMetidos + jugadorVisitante.fullBox.tirosLibresMetidos
        fullStatVisitante.tirosLibresIntentados = fullStatVisitante.tirosLibresIntentados + jugadorVisitante.fullBox.tirosLibresIntentados
        fullStatVisitante.reboteOfensivo = fullStatVisitante.reboteOfensivo + jugadorVisitante.fullBox.reboteOfensivo
        fullStatVisitante.reboteDefensivo = fullStatVisitante.reboteDefensivo + jugadorVisitante.fullBox.reboteDefensivo
        fullStatVisitante.totalRebotes = fullStatVisitante.totalRebotes + jugadorVisitante.fullBox.totalRebotes
        fullStatVisitante.asistencias = fullStatVisitante.asistencias + jugadorVisitante.fullBox.asistencias
        fullStatVisitante.robos = fullStatVisitante.robos + jugadorVisitante.fullBox.robos
        fullStatVisitante.tapones = fullStatVisitante.tapones + jugadorVisitante.fullBox.tapones
        fullStatVisitante.taponRecibido = fullStatVisitante.taponRecibido + jugadorVisitante.fullBox.taponRecibido
        fullStatVisitante.taponRecibidoTriple = fullStatVisitante.taponRecibidoTriple + jugadorVisitante.fullBox.taponRecibidoTriple
        fullStatVisitante.perdidas = fullStatVisitante.perdidas + jugadorVisitante.fullBox.perdidas
        fullStatVisitante.perdidaPasos = fullStatVisitante.perdidaPasos + jugadorVisitante.fullBox.perdidaPasos
        fullStatVisitante.perdidaMalPase = fullStatVisitante.perdidaMalPase + jugadorVisitante.fullBox.perdidaMalPase
        fullStatVisitante.perdidaFueraBanda = fullStatVisitante.perdidaFueraBanda + jugadorVisitante.fullBox.perdidaFueraBanda
        fullStatVisitante.perdidaBalonPerdido = fullStatVisitante.perdidaBalonPerdido + jugadorVisitante.fullBox.perdidaBalonPerdido
        fullStatVisitante.perdidaPisarFuera = fullStatVisitante.perdidaPisarFuera + jugadorVisitante.fullBox.perdidaPisarFuera
        fullStatVisitante.perdidaGoaltending = fullStatVisitante.perdidaGoaltending + jugadorVisitante.fullBox.perdidaGoaltending
        fullStatVisitante.faltaPersonalDefensa = fullStatVisitante.faltaPersonalDefensa + jugadorVisitante.fullBox.faltaPersonalDefensa
        fullStatVisitante.faltaPersonalProvocadaEnDefensa = fullStatVisitante.faltaPersonalProvocadaEnDefensa + jugadorVisitante.fullBox.faltaPersonalProvocadaEnDefensa
        fullStatVisitante.faltaPersonalAtaque = fullStatVisitante.faltaPersonalAtaque + jugadorVisitante.fullBox.faltaPersonalAtaque
        fullStatVisitante.faltaPersonalProvocadaEnAtaque = fullStatVisitante.faltaPersonalProvocadaEnAtaque + jugadorVisitante.fullBox.faltaPersonalProvocadaEnAtaque
        fullStatVisitante.faltaPersonalTiro = fullStatVisitante.faltaPersonalTiro + jugadorVisitante.fullBox.faltaPersonalTiro
        fullStatVisitante.faltaPersonalProvocadaEnTiro = fullStatVisitante.faltaPersonalProvocadaEnTiro + jugadorVisitante.fullBox.faltaPersonalProvocadaEnTiro
        fullStatVisitante.faltaTecnica = fullStatVisitante.faltaTecnica + jugadorVisitante.fullBox.faltaTecnica
        fullStatVisitante.faltasPersonales = fullStatVisitante.faltasPersonales + jugadorVisitante.fullBox.faltasPersonales
        fullStatVisitante.faltasPersonalesProvocadas = fullStatVisitante.faltasPersonalesProvocadas + jugadorVisitante.fullBox.faltasPersonalesProvocadas
        fullStatVisitante.puntos = fullStatVisitante.puntos + jugadorVisitante.fullBox.puntos
        fullStatVisitante.masMenos = fullStatVisitante.masMenos + jugadorVisitante.fullBox.masMenos
        fullStatVisitante.mate = fullStatVisitante.mate + jugadorVisitante.fullBox.mate
        fullStatVisitante.mateFallado = fullStatVisitante.mateFallado + jugadorVisitante.fullBox.mateFallado
        fullStatVisitante.suspension = fullStatVisitante.suspension + jugadorVisitante.fullBox.suspension
        fullStatVisitante.suspensionFallado = fullStatVisitante.suspensionFallado + jugadorVisitante.fullBox.suspensionFallado
        fullStatVisitante.bandeja = fullStatVisitante.bandeja + jugadorVisitante.fullBox.bandeja
        fullStatVisitante.bandejaFallada = fullStatVisitante.bandejaFallada + jugadorVisitante.fullBox.bandejaFallada
        fullStatVisitante.gancho = fullStatVisitante.gancho + jugadorVisitante.fullBox.gancho
        fullStatVisitante.ganchoFallado = fullStatVisitante.ganchoFallado + jugadorVisitante.fullBox.ganchoFallado
        fullStatVisitante.primerTiroLibreDentro = fullStatVisitante.primerTiroLibreDentro + jugadorVisitante.fullBox.primerTiroLibreDentro
        fullStatVisitante.primerTiroLibreFuera = fullStatVisitante.primerTiroLibreFuera + jugadorVisitante.fullBox.primerTiroLibreFuera
        fullStatVisitante.primerTiroLibreTotal = fullStatVisitante.primerTiroLibreTotal + jugadorVisitante.fullBox.primerTiroLibreTotal
        fullStatVisitante.segundoTiroLibreDentro = fullStatVisitante.segundoTiroLibreDentro + jugadorVisitante.fullBox.segundoTiroLibreDentro
        fullStatVisitante.segundoTiroLibreFuera = fullStatVisitante.segundoTiroLibreFuera + jugadorVisitante.fullBox.segundoTiroLibreFuera
        fullStatVisitante.segundoTiroLibreTotal = fullStatVisitante.segundoTiroLibreTotal + jugadorVisitante.fullBox.segundoTiroLibreTotal
        fullStatVisitante.tercerTiroLibreDentro = fullStatVisitante.tercerTiroLibreDentro + jugadorVisitante.fullBox.tercerTiroLibreDentro
        fullStatVisitante.tercerTiroLibreFuera = fullStatVisitante.tercerTiroLibreFuera + jugadorVisitante.fullBox.tercerTiroLibreFuera
        fullStatVisitante.tercerTiroLibreTotal = fullStatVisitante.tercerTiroLibreTotal + jugadorVisitante.fullBox.tercerTiroLibreTotal
    partido.equipoVisitante.fullBoxscore = fullStatVisitante
    partido.equipoVisitante.fullBoxscore.completarEstadisticas()
    partido.equipoVisitante.fullBoxscore.completarPorcentajes()
    return partido


################################################################################
####  FUNCION QUE COMPLETA LAS ESTADISTICAS AVENZADAS DEL PARTIDO           ####
################################################################################
def completarEstadisticaAvanzada(equipo):
    # # ESTADISTICAS PARA JUGADORES
    for jugador in equipo.jugadores:
    # perFGA  %Tiros intentados de un jugador respecto al equipo
        if comprobarNumero(jugador.boxscore.tirosCampoIntentados) and comprobarNumero(equipo.estadisticaNormal.tirosCampoIntentados):
            jugador.estadisticaAvanzada.perFGA = (float(jugador.boxscore.tirosCampoIntentados) / float(equipo.estadisticaNormal.tirosCampoIntentados)) * 100
            jugador.estadisticaAvanzada.perFGA = float("{0:.3f}".format(jugador.estadisticaAvanzada.perFGA))
        else:
            jugador.estadisticaAvanzada.perFGA = 0
    # perFGM        % Tiros anotados de un jugador respecto al equipo
        if comprobarNumero(jugador.boxscore.tirosCampoMetidos) and comprobarNumero(equipo.estadisticaNormal.tirosCampoMetidos):
            jugador.estadisticaAvanzada.perFGM = (float(jugador.boxscore.tirosCampoMetidos) / float(equipo.estadisticaNormal.tirosCampoMetidos)) * 100
            jugador.estadisticaAvanzada.perFGM = float("{0:.3f}".format(jugador.estadisticaAvanzada.perFGM))
        else:
            jugador.estadisticaAvanzada.perFGM = 0
    # FTARate       % Tiros libres respecto a los tiros de campo
        if comprobarNumero(jugador.boxscore.tirosLibresIntentados) and comprobarNumero(jugador.boxscore.tirosCampoIntentados):
            jugador.estadisticaAvanzada.FTARate = (float(jugador.boxscore.tirosLibresIntentados) / float(jugador.boxscore.tirosCampoIntentados)) * 100
            jugador.estadisticaAvanzada.FTARate = float("{0:.3f}".format(jugador.estadisticaAvanzada.FTARate))
        else:
            jugador.estadisticaAvanzada.FTARate = 0
        if comprobarNumero(equipo.estadisticaNormal.tirosLibresIntentados) and comprobarNumero(equipo.estadisticaNormal.tirosCampoIntentados):
            equipo.estadisticaAvanzada.FTARate = (float(equipo.estadisticaNormal.tirosLibresIntentados) / float(equipo.estadisticaNormal.tirosCampoIntentados)) * 100
            equipo.estadisticaAvanzada.FTARate = float("{0:.3f}".format(equipo.estadisticaAvanzada.FTARate))
        else:
            equipo.estadisticaAvanzada.FTARate = 0
    # perFTA        % Tiros libres intentados de un jugador respecto al equipo
        if comprobarNumero(jugador.boxscore.tirosLibresIntentados) and comprobarNumero(equipo.estadisticaNormal.tirosLibresIntentados):
            jugador.estadisticaAvanzada.perFTA = (float(jugador.boxscore.tirosLibresIntentados) / float(equipo.estadisticaNormal.tirosLibresIntentados)) * 100
            jugador.estadisticaAvanzada.perFTA = float("{0:.3f}".format(jugador.estadisticaAvanzada.perFTA))
        else:
            jugador.estadisticaAvanzada.perFTA = 0
    # perFTM        % Tiros libres anotados de un jugador respecto al equipo
        if comprobarNumero(jugador.boxscore.tirosLibresMetidos) and comprobarNumero(equipo.estadisticaNormal.tirosLibresMetidos):
            jugador.estadisticaAvanzada.perFTM = (float(jugador.boxscore.tirosLibresMetidos) / float(equipo.estadisticaNormal.tirosLibresMetidos)) * 100
            jugador.estadisticaAvanzada.perFTM = float("{0:.3f}".format(jugador.estadisticaAvanzada.perFTM))
        else:
            jugador.estadisticaAvanzada.perFTM = 0
    # perPTS1       % De puntos de tiro libre respecto al total de puntos
        if comprobarNumero(jugador.boxscore.tirosLibresMetidos) and comprobarNumero(jugador.boxscore.puntos):
            jugador.estadisticaAvanzada.perPTS1 = (float(jugador.boxscore.tirosLibresMetidos) / float(jugador.boxscore.puntos)) * 100
            jugador.estadisticaAvanzada.perPTS1 = float("{0:.3f}".format(jugador.estadisticaAvanzada.perPTS1))
        else:
            jugador.estadisticaAvanzada.perPTS1 = 0
        if comprobarNumero(equipo.estadisticaNormal.tirosLibresMetidos) and comprobarNumero(equipo.estadisticaNormal.puntos):
            equipo.estadisticaAvanzada.perPTS1 = (float(equipo.estadisticaNormal.tirosLibresMetidos) / float(equipo.estadisticaNormal.puntos)) * 100
            equipo.estadisticaAvanzada.perPTS1 = float("{0:.3f}".format(equipo.estadisticaAvanzada.perPTS1))
        else:
            equipo.estadisticaAvanzada.perPTS1 = 0
    # perFGA2P      % Tiros de 2 intentados de un jugador respecto al equipo
        if comprobarNumero(jugador.boxscore.tirosCampoIntentados) and comprobarNumero(equipo.estadisticaNormal.tirosCampoIntentados):
            jugador.estadisticaAvanzada.perFGA2P = (float(jugador.boxscore.tirosCampoIntentados) / float(equipo.estadisticaNormal.tirosCampoIntentados)) * 100
            jugador.estadisticaAvanzada.perFGA2P = float("{0:.3f}".format(jugador.estadisticaAvanzada.perFGA2P))
        else:
            jugador.estadisticaAvanzada.perFGA = 0
    # perFGM2P      % Tiros de 2 anotados de un jugador respecto al equipo
        if comprobarNumero(jugador.boxscore.tirosCampoMetidos) and comprobarNumero(equipo.estadisticaNormal.tirosCampoMetidos):
            jugador.estadisticaAvanzada.perFGM2P = (float(jugador.boxscore.tirosCampoMetidos) / float(equipo.estadisticaNormal.tirosCampoMetidos)) * 100
            jugador.estadisticaAvanzada.perFGM2P = float("{0:.3f}".format(jugador.estadisticaAvanzada.perFGM2P))
        else:
            jugador.estadisticaAvanzada.perFGM2P = 0
    # perPTS2PT    % Tiros de 2 intentados de un jugador o equipo
        if comprobarNumero(jugador.boxscore.tirosCampoIntentados) and comprobarNumero(jugador.boxscore.tirosCampoIntentados):
            jugador.estadisticaAvanzada.perPTS2PT = (float(jugador.boxscore.tirosCampoIntentados - jugador.boxscore.triplesIntentados) / float(jugador.boxscore.tirosCampoIntentados)) * 100
            jugador.estadisticaAvanzada.perPTS2PT = float("{0:.3f}".format(jugador.estadisticaAvanzada.perPTS2PT))
        else:
            jugador.estadisticaAvanzada.perPTS2PT = 0
        if comprobarNumero(equipo.estadisticaNormal.tirosCampoIntentados) and comprobarNumero(equipo.estadisticaNormal.tirosCampoIntentados):
            equipo.estadisticaAvanzada.perPTS2PT = (float(equipo.estadisticaNormal.tirosCampoIntentados - equipo.estadisticaNormal.triplesIntentados) / float(equipo.estadisticaNormal.tirosCampoIntentados)) * 100
            equipo.estadisticaAvanzada.perPTS2PT = float("{0:.3f}".format(equipo.estadisticaAvanzada.perPTS2PT))
        else:
            equipo.estadisticaAvanzada.perPTS2PT = 0
    # perPTS2PTM    % tiros de 2 anotados de un jugador o equipo
        if comprobarNumero(jugador.boxscore.tirosCampoMetidos) and comprobarNumero(jugador.boxscore.tirosCampoMetidos):
            jugador.estadisticaAvanzada.perPTS2PTM = (float(jugador.boxscore.tirosCampoMetidos - jugador.boxscore.triplesMetidos) / float(jugador.boxscore.tirosCampoMetidos)) * 100
            jugador.estadisticaAvanzada.perPTS2PTM = float("{0:.3f}".format(jugador.estadisticaAvanzada.perPTS2PTM))
        else:
            jugador.estadisticaAvanzada.perPTS2PTM = 0
        if comprobarNumero(equipo.estadisticaNormal.tirosCampoMetidos) and comprobarNumero(equipo.estadisticaNormal.tirosCampoMetidos):
            equipo.estadisticaAvanzada.perPTS2PTM = (float(equipo.estadisticaNormal.tirosCampoMetidos - equipo.estadisticaNormal.triplesMetidos) / float(equipo.estadisticaNormal.tirosCampoMetidos)) * 100
            equipo.estadisticaAvanzada.perPTS2PTM = float("{0:.3f}".format(equipo.estadisticaAvanzada.perPTS2PTM))
        else:
            equipo.estadisticaAvanzada.perFGA = 0
    # perPTS2       % De puntos de 2 respecto al total de los puntos
        if comprobarNumero(jugador.boxscore.tirosCampoMetidos) and comprobarNumero(jugador.boxscore.tirosCampoIntentados):
            jugador.estadisticaAvanzada.perPTS2 = (2 * (float(jugador.boxscore.tirosCampoMetidos - jugador.boxscore.triplesMetidos)) / float(jugador.boxscore.puntos)) * 100
            jugador.estadisticaAvanzada.perPTS2 = float("{0:.3f}".format(jugador.estadisticaAvanzada.perPTS2))
        else:
            jugador.estadisticaAvanzada.perPTS2 = 0
        if comprobarNumero(equipo.estadisticaNormal.tirosCampoMetidos) and comprobarNumero(equipo.estadisticaNormal.tirosCampoIntentados):
            equipo.estadisticaAvanzada.perPTS2 = (2 * (float(equipo.estadisticaNormal.tirosCampoMetidos - equipo.estadisticaNormal.triplesMetidos)) / float(equipo.estadisticaNormal.puntos)) * 100
            equipo.estadisticaAvanzada.perPTS2 = float("{0:.3f}".format(equipo.estadisticaAvanzada.perPTS2))
        else:
            equipo.estadisticaAvanzada.perPTS2 = 0
    # per3PA        % Tiros de 3 intentados de un jugador respecto al equipo
        if comprobarNumero(jugador.boxscore.triplesIntentados) and comprobarNumero(equipo.estadisticaNormal.triplesIntentados):
            jugador.estadisticaAvanzada.per3PA = (float(jugador.boxscore.triplesIntentados) / float(equipo.estadisticaNormal.triplesIntentados)) * 100
            jugador.estadisticaAvanzada.per3PA = float("{0:.3f}".format(jugador.estadisticaAvanzada.per3PA))
        else:
            jugador.estadisticaAvanzada.per3PA = 0
    # per3PM        % Tiros de 3 anotados de un jugador respecto al equipo
        if comprobarNumero(jugador.boxscore.triplesMetidos) and comprobarNumero(equipo.estadisticaNormal.triplesMetidos):
            jugador.estadisticaAvanzada.per3PM = (float(jugador.boxscore.triplesMetidos) / float(equipo.estadisticaNormal.triplesMetidos)) * 100
            jugador.estadisticaAvanzada.per3PM = float("{0:.3f}".format(jugador.estadisticaAvanzada.per3PM))
        else:
            jugador.estadisticaAvanzada.per3PM = 0
    # perPTS3PT     % Tiros de 3 Intentados de un jugador o equipo
        if comprobarNumero(jugador.boxscore.triplesIntentados) and comprobarNumero(jugador.boxscore.triplesIntentados):
            jugador.estadisticaAvanzada.perPTS3PT = (float(jugador.boxscore.triplesIntentados) / float(jugador.boxscore.triplesIntentados)) * 100
            jugador.estadisticaAvanzada.perPTS3PT = float("{0:.3f}".format(jugador.estadisticaAvanzada.perPTS3PT))
        else:
            jugador.estadisticaAvanzada.perPTS3PT = 0
        if comprobarNumero(equipo.estadisticaNormal.triplesIntentados) and comprobarNumero(equipo.estadisticaNormal.triplesIntentados):
            equipo.estadisticaAvanzada.perPTS3PT = (float(equipo.estadisticaNormal.triplesIntentados) / float(equipo.estadisticaNormal.triplesIntentados)) * 100
            equipo.estadisticaAvanzada.perPTS3PT = float("{0:.3f}".format(equipo.estadisticaAvanzada.perPTS3PT))
        else:
            equipo.estadisticaAvanzada.perPTS3PT = 0
    # perPTS3PTM    % Tiros de 3 anotados de un jugador o equipo
        if comprobarNumero(jugador.boxscore.triplesMetidos) and comprobarNumero(jugador.boxscore.triplesMetidos):
            jugador.estadisticaAvanzada.perPTS3PTM = (float(jugador.boxscore.triplesMetidos) / float(jugador.boxscore.triplesMetidos)) * 100
            jugador.estadisticaAvanzada.perPTS3PTM = float("{0:.3f}".format(jugador.estadisticaAvanzada.perPTS3PTM))
        else:
            jugador.estadisticaAvanzada.perPTS3PTM = 0
        if comprobarNumero(equipo.estadisticaNormal.triplesMetidos) and comprobarNumero(equipo.estadisticaNormal.triplesMetidos):
            equipo.estadisticaAvanzada.perPTS3PTM = (float(equipo.estadisticaNormal.triplesMetidos) / float(equipo.estadisticaNormal.triplesMetidos)) * 100
            equipo.estadisticaAvanzada.perPTS3PTM = float("{0:.3f}".format(equipo.estadisticaAvanzada.perPTS3PTM))
        else:
            equipo.estadisticaAvanzada.perPTS3PTM = 0
    # perPTS3       % De puntos de 3 respecto al total de los puntos
        if comprobarNumero(jugador.boxscore.triplesMetidos) and comprobarNumero(jugador.boxscore.puntos):
            jugador.estadisticaAvanzada.perPOINTS = ((3 * float(jugador.boxscore.puntos)) / float(equipo.estadisticaNormal.puntos)) * 100
            jugador.estadisticaAvanzada.perPTS3 = float("{0:.3f}".format(jugador.estadisticaAvanzada.perPTS3))
        else:
            jugador.estadisticaAvanzada.perPTS3 = 0
        if comprobarNumero(equipo.estadisticaNormal.triplesMetidos) and comprobarNumero(equipo.estadisticaNormal.puntos):
            equipo.estadisticaAvanzada.perPTS3 = ((3 * float(equipo.estadisticaNormal.triplesMetidos)) / float(equipo.estadisticaNormal.puntos)) * 100
            equipo.estadisticaAvanzada.perPTS3 = float("{0:.3f}".format(equipo.estadisticaAvanzada.perPTS3))
        else:
            equipo.estadisticaAvanzada.perPTS3 = 0
    # perPOINTS     % De puntos de un jugador respecto al equipo
        if comprobarNumero(jugador.boxscore.puntos) and comprobarNumero(equipo.estadisticaNormal.puntos):
            jugador.estadisticaAvanzada.perPOINTS = ((float(jugador.boxscore.puntos)) / float(equipo.estadisticaNormal.puntos)) * 100
            jugador.estadisticaAvanzada.perPOINTS = float("{0:.3f}".format(jugador.estadisticaAvanzada.perPOINTS))
        else:
            jugador.estadisticaAvanzada.perPOINTS = 0
    # perSTL        % De robos de un jugador respecto al equipo
        if comprobarNumero(jugador.boxscore.robos) and comprobarNumero(equipo.estadisticaNormal.robos):
            jugador.estadisticaAvanzada.perSTL = (float(jugador.boxscore.robos) / float(equipo.estadisticaNormal.robos)) * 100
            jugador.estadisticaAvanzada.perSTL = float("{0:.3f}".format(jugador.estadisticaAvanzada.perSTL))
        else:
            jugador.estadisticaAvanzada.perSTL = 0
    # perAST        % De Asistencias de un jugador respecto al equipo
        if comprobarNumero(jugador.boxscore.asistencias) and comprobarNumero(equipo.estadisticaNormal.asistencias):
            jugador.estadisticaAvanzada.perAST = (float(jugador.boxscore.asistencias) / float(equipo.estadisticaNormal.asistencias)) * 100
            jugador.estadisticaAvanzada.perAST = float("{0:.3f}".format(jugador.estadisticaAvanzada.perAST))
        else:
            jugador.estadisticaAvanzada.perAST = 0
    # perTOV        % De perdidas de un jugador respecto al equipo
        if comprobarNumero(jugador.boxscore.perdidas) and comprobarNumero(equipo.estadisticaNormal.perdidas):
            jugador.estadisticaAvanzada.perTOV = (float(jugador.boxscore.perdidas) / float(equipo.estadisticaNormal.perdidas)) * 100
            jugador.estadisticaAvanzada.perTOV = float("{0:.3f}".format(jugador.estadisticaAvanzada.perTOV))
        else:
            jugador.estadisticaAvanzada.perTOV = 0
    # perBLK        % De tapones de un jugador respecto al equipo
        if comprobarNumero(jugador.boxscore.tapones) and comprobarNumero(equipo.estadisticaNormal.tapones):
            jugador.estadisticaAvanzada.perBLK = (float(jugador.boxscore.tapones) / float(equipo.estadisticaNormal.tapones)) * 100
            jugador.estadisticaAvanzada.perBLK = float("{0:.3f}".format(jugador.estadisticaAvanzada.perBLK))
        else:
            jugador.estadisticaAvanzada.perBLK = 0
    # perDREB       % De retobes Defensivos de un jugador respecto al equipo
        if comprobarNumero(jugador.boxscore.reboteDefensivo) and comprobarNumero(equipo.estadisticaNormal.reboteDefensivo):
            jugador.estadisticaAvanzada.perDREB = (float(jugador.boxscore.reboteDefensivo) / float(equipo.estadisticaNormal.reboteDefensivo)) * 100
            jugador.estadisticaAvanzada.perDREB = float("{0:.3f}".format(jugador.estadisticaAvanzada.perDREB))
        else:
            jugador.estadisticaAvanzada.perDREB = 0
    # perOREB       % De rebotes Ofensivos de un jugador respecto al equipo
        if comprobarNumero(jugador.boxscore.reboteOfensivo) and comprobarNumero(equipo.estadisticaNormal.reboteOfensivo):
            jugador.estadisticaAvanzada.perOREB = (float(jugador.boxscore.reboteOfensivo) / float(equipo.estadisticaNormal.reboteOfensivo)) * 100
            jugador.estadisticaAvanzada.perOREB = float("{0:.3f}".format(jugador.estadisticaAvanzada.perOREB))
        else:
            jugador.estadisticaAvanzada.perOREB = 0
    # perTREB       % Del total de rebotes de un jugador respecto al equipo
        if comprobarNumero(jugador.boxscore.totalRebotes) and comprobarNumero(equipo.estadisticaNormal.totalRebotes):
            jugador.estadisticaAvanzada.perTREB = (float(jugador.boxscore.totalRebotes) / float(equipo.estadisticaNormal.totalRebotes)) * 100
            jugador.estadisticaAvanzada.perTREB = float("{0:.3f}".format(jugador.estadisticaAvanzada.perTREB))
        else:
            jugador.estadisticaAvanzada.perTREB = 0
    # perPF         % De Faltas de un jugador respecto al equipo
        if comprobarNumero(jugador.boxscore.faltasPersonales) and comprobarNumero(equipo.estadisticaNormal.faltasPersonales):
            jugador.estadisticaAvanzada.perPF = (float(jugador.boxscore.faltasPersonales) / float(equipo.estadisticaNormal.faltasPersonales)) * 100
            jugador.estadisticaAvanzada.perPF = float("{0:.3f}".format(jugador.estadisticaAvanzada.perPF))
        else:
            jugador.estadisticaAvanzada.perPF = 0
    # perPFP        % De faltas provocadas de un jugador respecto al equipo
        if comprobarNumero(jugador.boxscore.faltasPersonalesProvocadas) and comprobarNumero(equipo.estadisticaNormal.faltasPersonalesProvocadas):
            jugador.estadisticaAvanzada.perPFP = (float(jugador.boxscore.faltasPersonalesProvocadas) / float(equipo.estadisticaNormal.faltasPersonalesProvocadas)) * 100
            jugador.estadisticaAvanzada.perPFP = float("{0:.3f}".format(jugador.estadisticaAvanzada.perPFP))
        else:
            jugador.estadisticaAvanzada.perPFP = 0
    # NETRTG        Diferencia entre Offensive Rating y Defensive Ratting
        jugador.estadisticaAvanzada.NETRTG = jugador.estadisticaAvanzada.offensiveRating - jugador.estadisticaAvanzada.defensiveRating
        equipo.estadisticaAvanzada.NETRTG = equipo.estadisticaAvanzada.offensiveRating - equipo.estadisticaAvanzada.defensiveRating
    # FANTASY       Puntos Fantasy
        jugador.estadisticaAvanzada.FANTASY = jugador.boxscore.puntos + 1.2 * jugador.boxscore.totalRebotes + 1.5 * jugador.boxscore.asistencias + 3 * (jugador.boxscore.robos + jugador.boxscore.tapones) - jugador.boxscore.perdidas
        equipo.estadisticaAvanzada.FANTASY = equipo.estadisticaNormal.puntos + 1.2 * equipo.estadisticaNormal.totalRebotes + 1.5 * equipo.estadisticaNormal.asistencias + 3 * (equipo.estadisticaNormal.robos + equipo.estadisticaNormal.tapones) - equipo.estadisticaNormal.perdidas
    # #  ESTADISTICAS PARA  EQUIPO
    return equipo


#########################################################
####  FUNCION QUE COMPRUEBA EL NUMERO SI ES !=0      ####
#########################################################
def comprobarNumero(numero):
    if numero != 0:
        return True
    return False


def devolverTipoTiro(texto):
    if 'dunk' in texto:
        return 'Mate'
    if 'layup' in texto:
        return 'Bandeja'
    if 'hook' in texto:
        return 'Gancho'
    return 'tiro'