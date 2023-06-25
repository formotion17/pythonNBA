class tiros:
    #     #CARTA DE TIRO

    #     cuarto              =    ""
    #     tiempoRestante      =    ""     #MIRAR SI PODEMOS CONSEGUIRLO EN SEGUNDOS

    #     posicionTop         =    0
    #     posicionLeft        =    0

    #     jugador             =    ""

    #     dentro              =    False
    #     tipoCanasta         =    ""  #DOS PUNTOS O TRES PUNTOS
    #     distancia           =    0
    #     equipo              =    ""
    #     tanteo              =    "" #TANTEO SEPARADO POR '-' PARA PODER OBTENER

    def meterCuarto(self, cuarto):
        self.cuarto = cuarto

    def meterTiempoRestante(self, tiempoRestante):
        segundos = tiempoRestante.split(':')
        self.tiempoRestante = int(segundos[0]) * 60 + int(segundos[1])

    def meterDentro(self, dentro):
        self.dentro = dentro

    def meterTipo(self, tipo):
        self.tipo = tipo

    def meterDistancia(self, distancia):
        self.distancia = distancia

    def meterTanteo(self, tanteo):
        self.tanteo = tanteo
    
    def tanteoEquipo(self,tanteo):
        self.tanteoEquipo = tanteo
    
    def tanteoRival(self,tanteo):
        self.tanteoRival = tanteo

    def meterSituacionAntes(self, situacion):
        self.situacionAntes = situacion

    def meterSituacionDespues(self, situacion):
       self.situacionDespues = situacion

    def meterTipoCuarto(self, cuarto):
        self.cuarto = self.cuarto + " " + cuarto

    def meterPosicionTop(self, posicionTop):
        self.posicionTop = posicionTop

    def meterPosicionLeft(self, posicionLeft):
        self.posicionLeft = posicionLeft
