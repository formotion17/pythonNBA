#!/usr/bin/env python
# -*- coding: utf-8 -*-

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

    def __init__(self):
        self.estadisticaNormal = controllerStatNormales.statNormal("Partido")
        self.estadisticaAvanzada = controllerStatAvanzadas.statAvanzada()
    
    def insertarJugador(self, jugador):
        self.jugadores.append(jugador)
