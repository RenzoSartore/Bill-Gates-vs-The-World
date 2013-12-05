# -*- encoding: utf-8 -*-
import pilas
# Permite que este ejemplo funcion incluso si no has instalado pilas.
import sys
# Importamos todos los archios necesarios para el programa.
from pinguinito import MiPingu
from cajita import MiCaja
from bomba import Bomba
from bananita import Bananita
import random


pilas.iniciar()

#Definims la musica de fondo

musica_de_fondo = pilas.musica.cargar("musica.mp3")
musica_de_fondo.reproducir()

#Escena de Menu

class EscenaDeMenu(pilas.escena.Base):

    def __init__(self):
        pilas.escena.Base.__init__(self)

    def iniciar(self):
        fondo = pilas.fondos.DesplazamientoHorizontal()
        fondo.agregar("menu.jpg", y=0, velocidad=1000)

#Creamos las opciones que estaran dentro del menu para acceder a las distintas escenas

        opciones = [
		    ('Comenzar a jugar', self.comenzar),('Ayuda', self.ayuda),
		    ('Salir', self.salir)]

        self.menu = pilas.actores.Menu(opciones)

    def comenzar(self):
        pilas.cambiar_escena(EscenaDeJuego())

    def ayuda(self):
        pilas.cambiar_escena(EscenaDeAyuda())

    def salir(self):
        import sys
        sys.exit(0)

#Escena Del Juego

class EscenaDeJuego(pilas.escena.Base):

    def __init__(self):
        pilas.escena.Base.__init__(self)

    def iniciar(self):

        Pingu = MiPingu(y=-140)
        Pingu.aprender(pilas.habilidades.SeMantieneEnPantalla)

        #Definimos el Fondo

        fondo = pilas.fondos.DesplazamientoHorizontal()
        fondo.agregar("fondo.jpg")

        #Creamos las cajas que van a funcionar como "suelo"

        caja = MiCaja(x=200, y=-215)
        caja2 = MiCaja(x=250, y=-215)
        caja3 = MiCaja(x=300, y=-215)
        caja4 = MiCaja(x=150, y=-215)
        caja5 = MiCaja(x=100, y=-215)
        caja6 = MiCaja(x=50, y=-215)
        caja7 = MiCaja(x=0, y=-215)
        caja8 = MiCaja(x=-50, y=-215)
        caja9 = MiCaja(x=-100, y=-215)
        caja10 = MiCaja(x=-150, y=-215)
        caja11 = MiCaja(x=-200, y=-215)
        caja12 = MiCaja(x=-250, y=-215)
        caja13 = MiCaja(x=-300, y=-215)

        #Vector

        cajas = [caja,caja2,caja3,caja4,caja5,caja6,caja7,caja8,caja9,caja10,caja11,caja12,caja13]


        #Creamos las bananas (Dinero)

        b1 = Bananita()
        b1.x = 200
        b1.y = -150

        #Vector de bananas donde se almacenaran las nuevas bananas creadas

        bananas = [b1]

        #Definimos las vidas, su color y donde se ubicacion

        vida = pilas.actores.Puntaje(x=-190, y=200, color=pilas.colores.azul)
        vida.magnitud = 40
        vida.aumentar(3)

        puntos = pilas.actores.Puntaje(x=230, y=200, color=pilas.colores.blanco)
        puntos.magnitud = 40

        #Creamos la clase "BombaConMovimiento" que permite que las bombas caigan de forma horizontal hacia el piso

        class BombaConMovimiento(Bomba):

            def __init__(self, x=0, y=0):
                Bomba.__init__(self, x, y)

            def actualizar(self):
                self.y -= 3

        #Creamos el vector donde se van a almacenar las bombas

        bombas = []

        #Creamos la clase "Tiempo" para que las bombas caigan de manera mas rapida

        class Tiempo():

            def __init__(self, value=3.0):
                self.value = value

            def decrementar(self):
                if (self.value > 0.8):
                    self.value = self.value - 0.1
		
            def dameTiempo(self):
                return self.value


        #Creacion la funcion con la cual se van a crear las bombas

        tiempo = Tiempo()



        def crear_enemigo():
            bombas.append(BombaConMovimiento(x=random.randrange(-320, 320), y=240))
            tiempo.decrementar()
            print tiempo.dameTiempo()
            pilas.mundo.agregar_tarea(tiempo.dameTiempo(), crear_enemigo)

        def crear_banana():     
            bananas.append(Bananita(x=random.randrange(-320, 320), y=-140))
            pilas.mundo.agregar_tarea(tiempo.dameTiempo(), crear_banana)
		                    

        #Funcion para que exlote la bomba y el actor reaccione a ellas

        def hacer_explotar_una_bomba(Pingu, bomba):
            bomba.explotar()
            Pingu.gritar()
            print "Explotaste un Pinguini"

        #Funcion para el actor reaccione con las bananas y estas desasparezcan, tambien hacemos que al juntar determinado numero de puntos, se sume 1 vida mas

        def comer_banana(Pingu, banana):
            banana.eliminar()
            puntos.escala = 0
            puntos.escala = pilas.interpolar(1, duracion=0.5, tipo='rebote_final')
            puntos.aumentar(1)
            Pingu.sonreir()
            a=puntos.obtener()
            v=vida.obtener()
            if a == 20 or a==40 or a==60 or a==80 or a==100 or a==120 or a==140 or a==160 or a==180 or a==200 or a==220 or a==240 or a==260 or a==280 or a==300:
                if v < 5:
                    vida.aumentar(1)
                    pilas.avisar("Conseguiste 1 Vida. Ahora tenes %d vidas" %(vida.obtener()))
                    print "Ganaste plata"
                elif v > 5:
                    vida.aumentar(0)

        #Funcion para las bombas al tocar las cajas, pierdas una vida y al no tener mas de estas, perder

        def perder(cajas, bomba):
            vida.aumentar(-1)
            v2=vida.obtener()
            pilas.avisar("Perdiste una vida. Te quedan %d vidas" %(vida.obtener()))
            bomba.explotar()
            if v2 <= 0:
                pilas.escena_actual().tareas.eliminar_todas()
                t = pilas.actores.Texto("GAME OVER. Conseguiste %d puntos" %(puntos.obtener()))
                t.escala = 0
                t.escala = [1], 0.5


        # Le indicamos a pilas que funcion tiene que ejecutar cuando se produzca cada colicion y otras funciones que definimos antes

        pilas.mundo.colisiones.agregar(Pingu, bombas, hacer_explotar_una_bomba)
        pilas.escena_actual().colisiones.agregar(Pingu, bananas, comer_banana)
        pilas.escena_actual().colisiones.agregar(cajas,bombas, perder)
        crear_enemigo()
        pilas.escena_actual().colisiones.agregar(bombas, cajas, perder)
        crear_banana()


#Con esto al precionar la tecla q regresamos al menu

        pilas.avisar("Pulsa la tecla 'q' para regresar al menu o 'r' para reiniciar")

        pilas.eventos.pulsa_tecla.conectar(self.cuando_pulsa_tecla)

    def cuando_pulsa_tecla(self, evento):
        if evento.texto == u'q':
            pilas.cambiar_escena(EscenaDeMenu())

        pilas.eventos.pulsa_tecla.conectar(self.cuando_pulsa_tecla2)

    def cuando_pulsa_tecla2(self, evento):
        if evento.texto == u'r':
            pilas.cambiar_escena(EscenaDeJuego2())



#-----------------------------------------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------------------------------------------


class EscenaDeJuego2(pilas.escena.Base):

    def __init__(self):
        pilas.escena.Base.__init__(self)

    def iniciar(self):

        Pingu = MiPingu(y=-140)
        Pingu.aprender(pilas.habilidades.SeMantieneEnPantalla)

        #Definimos el Fondo

        fondo = pilas.fondos.DesplazamientoHorizontal()
        fondo.agregar("fondo.jpg")

        #Creamos las cajas que van a funcionar como "suelo"

        caja = MiCaja(x=200, y=-215)
        caja2 = MiCaja(x=250, y=-215)
        caja3 = MiCaja(x=300, y=-215)
        caja4 = MiCaja(x=150, y=-215)
        caja5 = MiCaja(x=100, y=-215)
        caja6 = MiCaja(x=50, y=-215)
        caja7 = MiCaja(x=0, y=-215)
        caja8 = MiCaja(x=-50, y=-215)
        caja9 = MiCaja(x=-100, y=-215)
        caja10 = MiCaja(x=-150, y=-215)
        caja11 = MiCaja(x=-200, y=-215)
        caja12 = MiCaja(x=-250, y=-215)
        caja13 = MiCaja(x=-300, y=-215)

        #Vector

        cajas = [caja,caja2,caja3,caja4,caja5,caja6,caja7,caja8,caja9,caja10,caja11,caja12,caja13]


        #Creamos las bananas (Dinero)

        b1 = Bananita()
        b1.x = 200
        b1.y = -150

        #Vector de bananas donde se almacenaran las nuevas bananas creadas

        bananas = [b1]

        #Definimos las vidas, su color y donde se ubicacion

        vida = pilas.actores.Puntaje(x=-190, y=200, color=pilas.colores.azul)
        vida.magnitud = 40
        vida.aumentar(3)

        puntos = pilas.actores.Puntaje(x=230, y=200, color=pilas.colores.blanco)
        puntos.magnitud = 40

        #Creamos la clase "BombaConMovimiento" que permite que las bombas caigan de forma horizontal hacia el piso

        class BombaConMovimiento(Bomba):

            def __init__(self, x=0, y=0):
                Bomba.__init__(self, x, y)

            def actualizar(self):
                self.y -= 3

        #Creamos el vector donde se van a almacenar las bombas

        bombas = []

        #Creamos la clase "Tiempo" para que las bombas caigan de manera mas rapida

        class Tiempo():

            def __init__(self, value=3.0):
                self.value = value

            def decrementar(self):
                if (self.value > 0.8):
                    self.value = self.value - 0.1
		
            def dameTiempo(self):
                return self.value


        #Creacion la funcion con la cual se van a crear las bombas

        tiempo = Tiempo()



        def crear_enemigo():
            bombas.append(BombaConMovimiento(x=random.randrange(-320, 320), y=240))
            tiempo.decrementar()
            print tiempo.dameTiempo()
            pilas.mundo.agregar_tarea(tiempo.dameTiempo(), crear_enemigo)

        def crear_banana():     
            bananas.append(Bananita(x=random.randrange(-320, 320), y=-140))
            pilas.mundo.agregar_tarea(tiempo.dameTiempo(), crear_banana)
		                    

        #Funcion para que exlote la bomba y el actor reaccione a ellas

        def hacer_explotar_una_bomba(Pingu, bomba):
            bomba.explotar()
            Pingu.gritar()
            print "Explotaste un Pinguini"

        #Funcion para el actor reaccione con las bananas y estas desasparezcan, tambien hacemos que al juntar determinado numero de puntos, se sume 1 vida mas

        def comer_banana(Pingu, banana):
            banana.eliminar()
            puntos.escala = 0
            puntos.escala = pilas.interpolar(1, duracion=0.5, tipo='rebote_final')
            puntos.aumentar(1)
            Pingu.sonreir()
            a=puntos.obtener()
            v=vida.obtener()
            if a == 20 or a==40 or a==60 or a==80 or a==100 or a==120 or a==140 or a==160 or a==180 or a==200 or a==220 or a==240 or a==260 or a==280 or a==300:
                if v < 5:
                    vida.aumentar(1)
                    pilas.avisar("Conseguiste 1 Vida. Ahora tenes %d vidas" %(vida.obtener()))
                    print "Ganaste plata"
                elif v > 5:
                    vida.aumentar(0)

        #Funcion para las bombas al tocar las cajas, pierdas una vida y al no tener mas de estas, perder

        def perder(cajas, bomba):
            vida.aumentar(-1)
            v2=vida.obtener()
            pilas.avisar("Perdiste una vida. Te quedan %d vidas" %(vida.obtener()))
            bomba.explotar()
            if v2 <= 0:
                pilas.escena_actual().tareas.eliminar_todas()
                t = pilas.actores.Texto("GAME OVER. Conseguiste %d puntos" %(puntos.obtener()))
                t.escala = 0
                t.escala = [1], 0.5


        # Le indicamos a pilas que funcion tiene que ejecutar cuando se produzca cada colicion y otras funciones que definimos antes

        pilas.mundo.colisiones.agregar(Pingu, bombas, hacer_explotar_una_bomba)
        pilas.escena_actual().colisiones.agregar(Pingu, bananas, comer_banana)
        pilas.escena_actual().colisiones.agregar(cajas,bombas, perder)
        crear_enemigo()
        pilas.escena_actual().colisiones.agregar(bombas, cajas, perder)
        crear_banana()


#Con esto al precionar la tecla q regresamos al menu

        pilas.avisar("Pulsa la tecla 'q' para regresar al menu o 'r' para reiniciar")

        pilas.eventos.pulsa_tecla.conectar(self.cuando_pulsa_tecla)

    def cuando_pulsa_tecla(self, evento):
        if evento.texto == u'q':
            pilas.cambiar_escena(EscenaDeMenu())

        pilas.eventos.pulsa_tecla.conectar(self.cuando_pulsa_tecla3)

    def cuando_pulsa_tecla3(self, evento):
        if evento.texto == u'r':
            pilas.cambiar_escena(EscenaDeJuego())



#-----------------------------------------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------------------------------------------





#Escena de Ayuda (La Escena ayuda consta basicamente en lo mismo que la escena del juego, exeptuando que los pinguinos y la plata se crea en lugares determinados, por eso no me tomo la molestia de comentar lo mismo que ya comente anteriormente)

class EscenaDeAyuda(pilas.escena.Base):

    def __init__(self):
        pilas.escena.Base.__init__(self)

    def iniciar(self):

#Definimos el Actor

	Pingu = MiPingu(y=-140)
	Pingu.aprender(pilas.habilidades.SeMantieneEnPantalla)


#Definimos el Fondo
	fondo = pilas.fondos.DesplazamientoHorizontal()
	fondo.agregar("ayuda.jpg", y=0, velocidad=1)


#Creamos las cajas que van a funcionar como "suelo"

	caja = MiCaja(x=200, y=-215)
	caja2 = MiCaja(x=250, y=-215)
	caja3 = MiCaja(x=300, y=-215)
	caja4 = MiCaja(x=150, y=-215)
	caja5 = MiCaja(x=100, y=-215)
	caja6 = MiCaja(x=50, y=-215)
	caja7 = MiCaja(x=0, y=-215)
	caja8 = MiCaja(x=-50, y=-215)
	caja9 = MiCaja(x=-100, y=-215)
	caja10 = MiCaja(x=-150, y=-215)
	caja11 = MiCaja(x=-200, y=-215)
	caja12 = MiCaja(x=-250, y=-215)
	caja13 = MiCaja(x=-300, y=-215)


#Vector

	cajas = [caja,caja2,caja3,caja4,caja5,caja6,caja7,caja8,caja9,caja10,caja11,caja12,caja13]


#Vector de bananas donde se almacenaran las nuevas bananas creadas

	b1 = Bananita()
	b1.x = -200
	b1.y = -150

	bananas = [b1]



	class BombaConMovimiento(Bomba):

		def __init__(self, x=0, y=0):
			Bomba.__init__(self, x, y)

		def actualizar(self):
			self.y -= 3

				#if self.y > 240:
				    #self.y = -240

	bombas = []



	class Tiempo():

		def __init__(self, value=3.0):
			self.value = value

		def decrementar(self):
			if (self.value > 0.8):
				self.value = self.value - 0.1
		
		def dameTiempo(self):
			return self.value


	tiempo = Tiempo()

	def crear_enemigo():
		bombas.append(BombaConMovimiento(x=random.randrange(75, 280), y=240))
		tiempo.decrementar()
		print tiempo.dameTiempo()
		pilas.mundo.agregar_tarea(tiempo.dameTiempo(), crear_enemigo)

	def crear_banana():
		
		bananas.append(Bananita(x=random.randrange(-270, -60), y=-140))
		pilas.mundo.agregar_tarea(tiempo.dameTiempo(), crear_banana)
				



	def hacer_explotar_una_bomba(Pingu, bomba):
		bomba.explotar()
		Pingu.gritar()
		print "Explotaste la bomba 1"


	def comer_banana(Pingu, banana):
		banana.eliminar()
		puntos.escala = 0
		puntos.escala = pilas.interpolar(1, duracion=0.5, tipo='rebote_final')
		puntos.aumentar(1)
		Pingu.sonreir()
		print "Ta con hambre el, eh?"



	def perder(cajas, bomba):
		global fin_de_juego
		bomba.explotar()
		fin_de_juego = True
		pilas.avisar("Perdiste Conseguiste %d puntos pero puedes seguir practicando" %(puntos.obtener()))

	puntos = pilas.actores.Puntaje(x=-175, y=10, color=pilas.colores.blanco)
	puntos.magnitud = 40



	pilas.mundo.colisiones.agregar(Pingu, bombas, hacer_explotar_una_bomba)
	pilas.escena_actual().colisiones.agregar(Pingu, bananas, comer_banana)
	pilas.escena_actual().colisiones.agregar(cajas,bombas, perder)
	crear_enemigo()
	pilas.escena_actual().colisiones.agregar(bombas, cajas, perder)
	crear_banana()




        pilas.eventos.pulsa_tecla.conectar(self.cuando_pulsa_tecla)
	pilas.escena_actual().colisiones.agregar(Pingu, bananas, comer_banana)
    def cuando_pulsa_tecla(self, evento):
        if evento.texto == u'q':
            pilas.cambiar_escena(EscenaDeMenu())

pilas.cambiar_escena(EscenaDeMenu())
pilas.ejecutar()
