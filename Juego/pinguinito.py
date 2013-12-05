import pilas
class MiPingu(pilas.actores.Pingu):

    def __init__(self, x=0, y=0):               
        pilas.actores.Pingu.__init__(self, x=x, y=y)
        self.radioNormal()

    def radioNormal(self):
        self.centro = ("centro", "centro")
    	self.radio_de_colision = 50
        
    
    def gritar(self):
        print "Quiero Gritar"
        """Hace que el mono grite emitiendo un sonido."""
        #self.imagen.definir_cuadro(2)
        self.imagen = pilas.imagenes.cargar_grilla("pingu2.png", 10)
        self.centro = ("centro", "centro")
        # Luego de un segundo regresa a la normalidad
        pilas.mundo.agregar_tarea_una_vez(0.3, self.normal)
        self.radioNormal()

    def sonreir(self):
        print "Quiero Sonreir"
        """Hace que el mono grite emitiendo un sonido."""
        #self.imagen.definir_cuadro(2)
        self.imagen = pilas.imagenes.cargar_grilla("pingu3.png", 10)
        # Luego de un segundo regresa a la normalidad
        pilas.mundo.agregar_tarea_una_vez(0.3, self.normal)
        self.radioNormal()

    def normal(self):
        print "Soy Normal"
        self.imagen = pilas.imagenes.cargar_grilla("pingu.png", 10)
        self.imagen.definir_cuadro(4)
        self.radioNormal()

