#!/usr/bin/env python
# -*- coding: utf-8 -*-

from     bs4                     import     BeautifulSoup
import     urllib
import     os
import     re
import     funciones
import     constantes
import     controllerJugador
import     controllerStatNormales
import     controllerStatAvanzadas


class equipo:
    nombre = ""
    nombreAbreviado = ""
    victorias = 0
    derrotas = 0
    tanteo = 0
    puntosConsecutivos = 0
    tiempoSinAnotar = ""
    # tanteoCuartos            =    []
    # estadisticaNormal        =    controllerStatNormales.statNormal()
    # estadisticaAvanzada    =    controllerStatAvanzadas.statAvanzada()
    # jugadores                =    []    # controllerJugador.jugador()

    def __init__(self):
        self.estadisticaNormal = controllerStatNormales.statNormal("Partido")
        self.estadisticaAvanzada = controllerStatAvanzadas.statAvanzada()
    
    def insertarJugador(self, jugador):
        self.jugadores.append(jugador)
