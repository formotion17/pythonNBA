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
import funciones
import funcionesPartido
import time as reloj
from pymongo import MongoClient
from collections import OrderedDict

############################################################################
####   PERMITE CAMBIAR DEL ASCII PREDETERMINADO A OTRAS CODIFICACIONES  ####
############################################################################
#reload(sys)
#sys.setdefaultencoding('utf-8')


def devolverPaginaDescargada(year, tipo, numero):
    page = open("/Users/formotion/tfg/python/DATA/DOWNLOADED PAGES/" + str(year) + "-" + str(year + 1) + "/" + str(numero) + "." + tipo + ".html", "r")
    return BeautifulSoup(page, "html.parser")

def contarArvhicosEnCarpeta(ruta):
    contenido = os.listdir(ruta)
    
    num_archivos = 0
    for elemento in contenido:
        num_archivos += 1
        
    return int(num_archivos/4)



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

client = MongoClient("mongodb://localhost:27017")

db = client["NBA"]

collection = db["partidos"]




##  BUCLE PARA IR RECORRIENDO TEMPORADAS
for year in range(constantes.TEMPORADA_INICIAL, constantes.TEMPORADA_FINAL):

    ##  BUCLE PARA IR RECORRIENDO LOS PARTIDOS DE LA TEMPORADA
    for archivo in range(1, contarArvhicosEnCarpeta("/Users/formotion/tfg/python/DATA/DOWNLOADED PAGES/" + str(year) + "-" + str(year + 1))+1):
        
    
        ############################################################################
        ####  ENTRAMOS EN LA PAGINA PARA DESCARGAR LAS                          ####
        ####  ESTADISTICAS POR CUARTO DE CADA EQUIPO                            ####
        ############################################################################
    
        print ("    ENTRAMOS EN LA P�GINA DE JUGADA A JUGADA")
    
        ## RECOGEMOS Y PARSEAMOS LA PAGINA DE PLAY BY PLAY DEL PARTIDO
        playbyplay = devolverPaginaDescargada(year, 'b', archivo)
        
        errorPagina = playbyplay.select('h1')[0].text.strip()
        
        if '    Page Not Found (404 error)' !=errorPagina:
            
            # Encontrar el elemento contenedor para obtener dia y mes
            scorebox_meta = playbyplay.find('div', class_='scorebox_meta')
            
            dia = scorebox_meta.find('div').text.split(',')[1].strip().split(' ') [1]
            mes = devolverMes(scorebox_meta.find('div').text.split(',')[1].strip().split(' ') [0])
        
        
            ##  NAVEGAMOS POR LA PAGINA RECOGIENDO DIFERENTES COSAS
            for stats in playbyplay.findAll('div', {"class": "scorebox"}):
        
                ##  RECOGEMOS EL NOMBRE DE LOS EQUIPOS VISITANTE Y LOCAL
                teams = []
                nombre = stats('a')
                for nombre in stats.findAll('strong'):
                    teams.append(str(nombre.find('a').text))
                equipoVisitante = teams[0]
                equipoLocal = teams[1]
            
            print (dia)
            print (mes)
            print (str(funciones.devolverAnioCorrecto(year, mes)))
            print (equipoLocal)
            print (equipoVisitante)
            
            
            filtro = {
                "dia": dia,
                "mes": str(mes),
                "year": str(funciones.devolverAnioCorrecto(year, mes)),
                "equipoLocal.nombre": equipoLocal
            }
            
            # Realizar la búsqueda en la colección
            documento = collection.find_one(filtro)
            
            ##  RECOGEMOS LAS ESTADISTICAS POR CUARTO DE CADA JUGADOR
            tanteo = funcionesPartido.devolverTanteoPartido(playbyplay)
            
            tanteoPartido = list(OrderedDict.fromkeys(tanteo))
            
            listaTanteoLocal=[]
            
            for resultado in tanteoPartido:
                #print(resultado)
                dividir = resultado.split('-')
                listaTanteoLocal.append(int(dividir[1])-int(dividir[0]))
            
            documento["tanteo"]=tanteoPartido
            documento["tanteoLocal"]=listaTanteoLocal
            
            collection.update_one(filtro, {"$set": documento})
    
    
        ############################################################################
        ####  GUARDAMOS EL PARTIDO EN UN ARCHIVO JSON                           ####
        ############################################################################
    
        print ("Fin del partido partido")
        print ("********************************************************")
        print (" ")
