#!/usr/bin/env python
# -*- coding: utf-8 -*-


import controllerStatNormales    as cuarto
import controllerStatAvanzadas    as avanzadas


class jugador:
    id = ""
    nombre = ""
    apellido = ""
    inicio = False
    segundos = 0
    totalPartido = cuarto
    cuarto1 = cuarto


    def __init__(self, id):
        self.id = id;
        self.totalPartido = cuarto.statNormal("Partido")
        self.fullBox = cuarto.statNormal("Total Partido")
        self.estadisticaAvanzada = avanzadas.statAvanzada()
        self.cuarto1 = cuarto.statNormal("1st Quarter")

    def meterCuarto(self, quarter):
        self.estadisticasCuarto.append(quarter)

    def meterCartaTiro(self, jugada):
        self.listaTiros.append(jugada)

    def boxscore(self, numero):
        self.boxscore = cuarto.statNormal(numero)

    def completarEstadisticas(self):
        for i in self.estadisticasCuarto:
            i.completarEstadisticas()

            ## REBOTES
            self.totalPartido.reboteDefensivo += i.reboteDefensivo
            self.totalPartido.reboteOfensivo += i.reboteOfensivo
            self.totalPartido.totalRebotes += i.totalRebotes

            ## TIRO DE 2
            self.totalPartido.tirosCampoMetidos += i.tirosCampoMetidos
            self.totalPartido.tirosCampoIntentados += i.tirosCampoIntentados

            ## TIRO DE 3
            self.totalPartido.triplesMetidos += i.triplesMetidos
            self.totalPartido.triplesIntentados += i.triplesIntentados

            ## TIRO LIBRE
            self.totalPartido.tirosLibresMetidos += i.tirosLibresMetidos
            self.totalPartido.tirosLibresIntentados += i.tirosLibresIntentados

            ## TIRO LIBRE - TIPO
            self.totalPartido.primerTiroLibreDentro += i.primerTiroLibreDentro
            self.totalPartido.primerTiroLibreFuera += i.primerTiroLibreFuera
            self.totalPartido.primerTiroLibreTotal += i.primerTiroLibreTotal

            self.totalPartido.segundoTiroLibreDentro += i.segundoTiroLibreDentro
            self.totalPartido.segundoTiroLibreFuera += i.segundoTiroLibreFuera
            self.totalPartido.segundoTiroLibreTotal += i.segundoTiroLibreTotal

            self.totalPartido.tercerTiroLibreDentro += i.tercerTiroLibreDentro
            self.totalPartido.tercerTiroLibreFuera += i.tercerTiroLibreFuera
            self.totalPartido.tercerTiroLibreTotal += i.tercerTiroLibreTotal

            ## TIPO DE TIRO
            self.totalPartido.suspension += i.suspension
            self.totalPartido.suspensionFallado += i.suspensionFallado

            self.totalPartido.mate += i.mate
            self.totalPartido.mateFallado += i.mateFallado

            self.totalPartido.bandeja += i.bandeja
            self.totalPartido.bandejaFallada += i.bandejaFallada

            self.totalPartido.gancho += i.gancho
            self.totalPartido.ganchoFallado += i.ganchoFallado

            ## ASISTENCIA
            self.totalPartido.asistencias += i.asistencias

            ## TAPONES
            self.totalPartido.tapones += i.tapones

            ## TAPONES - RECIBIDOS
            self.totalPartido.taponRecibido += i.taponRecibido
            self.totalPartido.taponRecibidoTriple += i.taponRecibidoTriple

            ## PUNTOS
            self.totalPartido.puntos += i.puntos

            ## PERDIDAS
            self.totalPartido.perdidas += i.perdidas

            ## PERDIDAS - TIPO
            self.totalPartido.perdidaPasos += i.perdidaPasos
            self.totalPartido.perdidaMalPase += i.perdidaMalPase
            self.totalPartido.perdidaFueraBanda += i.perdidaFueraBanda
            self.totalPartido.perdidaPisarFuera += i.perdidaPisarFuera
            self.totalPartido.perdidaGoaltending += i.perdidaGoaltending
            self.totalPartido.perdidaBalonPerdido += i.perdidaBalonPerdido

            ## ROBOS
            self.totalPartido.robos += i.robos

            ## FALTAS PERSONALES REALIZADAS
            self.totalPartido.faltaPersonalDefensa += i.faltaPersonalDefensa
            self.totalPartido.faltaPersonalAtaque += i.faltaPersonalAtaque
            self.totalPartido.faltasPersonales += i.faltasPersonales
            self.totalPartido.faltaTecnica += i.faltaTecnica
            self.totalPartido.faltaPersonalTiro += i.faltaPersonalTiro
            self.totalPartido.faltaPersonalDoble += i.faltaPersonalDoble

            ## FALTAS PERSONALES RECIBIDAS
            self.totalPartido.faltaPersonalProvocadaEnDefensa += i.faltaPersonalProvocadaEnDefensa
            self.totalPartido.faltaPersonalProvocadaEnAtaque += i.faltaPersonalProvocadaEnAtaque
            self.totalPartido.faltaPersonalProvocadaEnTiro += i.faltaPersonalProvocadaEnTiro
            self.totalPartido.faltasPersonalesProvocadas += i.faltasPersonalesProvocadas

            ## PORCENTAJES
            self.totalPartido.completarPorcentajes()