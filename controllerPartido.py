#!/usr/bin/env python
# -*- coding: utf-8 -*-

import     controllerEquipo
import     json


class partido:
# FECHA    A LA HORA DE GUARDAR LA FECHA SE GUARDA {"$Timestamp":"1989-11-03T17:17:17.881Z"},
    hora = ""
    dia = ""
    mes = ""
    year = ""
# UBICACION
    estadio = ""
    ubicacion = ""
    asistencia = 0
# TIPO DE PARTIDO
    playOff = False
    playIn = False
    conferencia = ""
    bracket = ""
    game = 0
# EQUIPOS DEL PARTIDO
    empates = ""
    cambiosLider = ""
    tiempoEmpate = ""
    tiempoLocalGanando = ""
    tiempoVisitanteGanando = ""
    equipoLocal = controllerEquipo.equipo()
    equipoVisitante = controllerEquipo.equipo()
    numeroCuartos = 0

    #Funcion que recibe la fecha, estadio y la ubicación del partido
    def rellenarFechaUbicacion(self,dia,mes,year,listaFuncion,asistencia):
        self.dia        =    dia
        self.mes        =    mes
        self.year        =    year
        self.hora        =    listaFuncion[0]
        if listaFuncion.__len__() > 2 :
            self.estadio = listaFuncion[1]
            self.ubicacion = listaFuncion[2] + "," + listaFuncion[3]
        else:
            self.estadio = "Desconocido"
            self.ubicacion = "Desconocida"
        self.asistencia    =    asistencia

    #Funcion para imprimir fecha, estadio, ubicaci�n y asistencia
    def imprimirPartido(self):
        print ("Fecha:    " + self.dia + "-" + self.mes + "-" + self.year + "-" + self.hora)
        print ("Estadio:     " + self.estadio)
        print ("Lugar:         " + self.ubicacion)
        print ("Asistencia    " + str(self.asistencia))

    def getDatosPartido(self):
        imprimir = 'Fecha:         ' + self.dia + '-' + self.mes + '-' + self.year + '-' + self.hora
        imprimir = imprimir + 'Estadio:     ' + self.estadio
        imprimir = imprimir + 'Lugar:         ' + self.ubicacion
        imprimir = imprimir + 'Asistencia    ' + str(self.asistencia)
        return imprimir

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=2)
