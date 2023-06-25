#!/usr/bin/env python
# -*- coding: utf-8 -*-

from    bs4         import BeautifulSoup
import  urllib
import  os
import  re
import  funciones
import  constantes

class statNormal:
    cuarto                              =   ""
    tirosCampoMetidos                   =   0
    tirosCampoIntentados                =   0
    tirosCampoPorcentaje                =   0
    triplesMetidos                      =   0
    triplesIntentados                   =   0
    triplesPorcentaje                   =   0
    tirosLibresMetidos                  =   0
    tirosLibresIntentados               =   0
    tirosLibresPorcentaje               =   0
    reboteOfensivo                      =   0
    reboteDefensivo                     =   0
    totalRebotes                        =   0
    asistencias                         =   0
    robos                               =   0
    tapones                             =   0
    taponRecibido                       =   0
    taponRecibidoTriple                 =   0
    perdidas                            =   0
    perdidaPasos                        =   0
    perdidaMalPase                      =   0
    perdidaFueraBanda                   =   0
    perdidaBalonPerdido                 =   0
    perdidaPisarFuera                   =   0
    perdidaGoaltending                  =   0
    perdidaCampoAtras                   =   0
    perdidaOtros                        =   0
    perdidaTresSegundos                 =   0
    perdidaFalta                        =   0
    perdidaDobles                       =   0
    perdidaPie                          =   0
    faltaPersonalDefensa                =   0
    faltaPersonalProvocadaEnDefensa     =   0
    faltaPersonalAtaque                 =   0
    faltaPersonalProvocadaEnAtaque      =   0
    faltaPersonalTiro                   =   0
    faltaPersonalProvocadaEnTiro        =   0
    faltaTecnica                        =   0
    faltasPersonales                    =   0
    faltasPersonalesProvocadas          =   0
    faltaPersonalDoble                  =   0
    puntos                              =   0
    masMenos                            =   0
    mate                                =   0
    mateFallado                         =   0
    suspension                          =   0
    suspensionFallado                   =   0
    bandeja                             =   0
    bandejaFallada                      =   0
    gancho                              =   0
    ganchoFallado                       =   0
    primerTiroLibreDentro               =   0
    primerTiroLibreFuera                =   0
    primerTiroLibreTotal                =   0
    primerTiroLibrePorcentaje           =   0
    segundoTiroLibreDentro              =   0
    segundoTiroLibreFuera               =   0
    segundoTiroLibreTotal               =   0
    segundoTiroLibrePorcentaje          =   0
    tercerTiroLibreDentro               =   0
    tercerTiroLibreFuera                =   0
    tercerTiroLibreTotal                =   0
    tercerTiroLibrePorcentaje           =   0


    def __init__(self, numero):
        self.cuarto = numero
        
    def completarEstadisticas(self):
        ## REBOTES
        self.totalRebotes           =   self.reboteDefensivo        +   self.reboteOfensivo

        ## TIROS LIBRES
        self.primerTiroLibreTotal   =   self.primerTiroLibreDentro  +   self.primerTiroLibreFuera
        self.segundoTiroLibreTotal  =   self.segundoTiroLibreDentro +   self.segundoTiroLibreFuera
        self.tercerTiroLibreTotal   =   self.tercerTiroLibreDentro  +   self.tercerTiroLibreFuera

        ## PUNTOS
        self.puntos                 =   self.tirosCampoMetidos*2    +   self.triplesMetidos +   self.tirosLibresMetidos

        ## FALTAS PERSONALES
        self.faltasPersonales       =   self.faltaPersonalDefensa   +   self.faltaPersonalAtaque    +   self.faltaTecnica   +   self.faltaPersonalTiro  +self.faltaPersonalDoble

        ## FALTAS PERSONALES PROVOCADAS
        self.faltasPersonalesProvocadas =   self.faltaPersonalProvocadaEnDefensa    +   self.faltaPersonalProvocadaEnAtaque +   self.faltaPersonalProvocadaEnTiro

        ## TIROS LIBRES
        if self.tirosLibresMetidos!=0:
            self.tirosLibresPorcentaje = (float(self.tirosLibresMetidos) / float(self.tirosLibresIntentados)) * 100
            self.tirosLibresPorcentaje = float("{0:.3f}".format(self.tirosLibresPorcentaje))
        else:
            self.tirosLibresPorcentaje  =   0

        ## TIRO LIBRE - TIPO
        if self.primerTiroLibreDentro != 0:
            self.primerTiroLibrePorcentaje = (float(self.primerTiroLibreDentro) / float(self.primerTiroLibreTotal)) * 100
            self.primerTiroLibrePorcentaje = float("{0:.3f}".format(self.primerTiroLibrePorcentaje))
        else:
            self.primerTiroLibrePorcentaje = 0

        if self.segundoTiroLibreDentro != 0:
            self.segundoTiroLibrePorcentaje = (float(self.segundoTiroLibreDentro) / float(self.segundoTiroLibreTotal)) * 100
            self.segundoTiroLibrePorcentaje = float("{0:.3f}".format(self.segundoTiroLibrePorcentaje))
        else:
            self.segundoTiroLibrePorcentaje = 0

        if self.tercerTiroLibreDentro != 0:
            self.tercerTiroLibrePorcentaje = (float(self.tercerTiroLibreDentro) / float(self.tercerTiroLibreTotal)) * 100
            self.tercerTiroLibrePorcentaje = float("{0:.3f}".format(self.tercerTiroLibrePorcentaje))
        else:
            self.tercerTiroLibrePorcentaje = 0

        ## TIROS DE 2
        if self.tirosCampoMetidos != 0:
            self.tirosCampoPorcentaje = (float(self.tirosCampoMetidos) / float(self.tirosCampoIntentados)) * 100
            self.tirosCampoPorcentaje = float("{0:.3f}".format(self.tirosCampoPorcentaje))
        else:
            self.tirosCampoPorcentaje = 0

        ## TIROS DE 3
        if self.triplesMetidos != 0:
            self.triplesPorcentaje = (float(self.triplesMetidos) / float(self.triplesIntentados)) * 100
            self.triplesPorcentaje = float("{0:.3f}".format(self.triplesPorcentaje))
        else:
            self.triplesPorcentaje = 0

    def completarPorcentajes(self):
        ## TIROS LIBRES
        if self.tirosLibresMetidos != 0:
            self.tirosLibresPorcentaje = (float(self.tirosLibresMetidos) / float(self.tirosLibresIntentados)) * 100
            self.tirosLibresPorcentaje = float("{0:.3f}".format(self.tirosLibresPorcentaje))
        else:
            self.tirosLibresPorcentaje = 0

        ## TIRO LIBRE - TIPO
        if self.primerTiroLibreDentro != 0:
            self.primerTiroLibrePorcentaje = (float(self.primerTiroLibreDentro) / float(
                self.primerTiroLibreTotal)) * 100
            self.primerTiroLibrePorcentaje = float("{0:.3f}".format(self.primerTiroLibrePorcentaje))
        else:
            self.primerTiroLibrePorcentaje = 0

        if self.segundoTiroLibreDentro != 0:
            self.segundoTiroLibrePorcentaje = (float(self.segundoTiroLibreDentro) / float(
                self.segundoTiroLibreTotal)) * 100
            self.segundoTiroLibrePorcentaje = float("{0:.3f}".format(self.segundoTiroLibrePorcentaje))
        else:
            self.segundoTiroLibrePorcentaje = 0

        if self.tercerTiroLibreDentro != 0:
            self.tercerTiroLibrePorcentaje = (float(self.tercerTiroLibreDentro) / float(
                self.tercerTiroLibreTotal)) * 100
            self.tercerTiroLibrePorcentaje = float("{0:.3f}".format(self.tercerTiroLibrePorcentaje))
        else:
            self.tercerTiroLibrePorcentaje = 0

        ## TIROS DE 2
        if self.tirosCampoMetidos != 0:
            self.tirosCampoPorcentaje = (float(self.tirosCampoMetidos) / float(self.tirosCampoIntentados)) * 100
            self.tirosCampoPorcentaje = float("{0:.3f}".format(self.tirosCampoPorcentaje))
        else:
            self.tirosCampoPorcentaje = 0

        ## TIROS DE 3
        if self.triplesMetidos != 0:
            self.triplesPorcentaje = (float(self.triplesMetidos) / float(self.triplesIntentados)) * 100
            self.triplesPorcentaje = float("{0:.3f}".format(self.triplesPorcentaje))
        else:
            self.triplesPorcentaje = 0