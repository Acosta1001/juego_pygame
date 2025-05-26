import pygame

class Entidad(pygame.sprite.Sprite):
    # pygame.sprite.Sprite --> es una clase que proporciona una forma estandarizada de trabajar con sprites
    def __init__(self, x, y, imagen, ancho=50, alto=50):
        super().__init__()
        # lectura de imagen con pygame
        imagen_original = pygame.image.load(imagen).convert_alpha()
        # re escalar imagen
        self.image = pygame.transform.smoothscale(imagen_original, (ancho, alto))
        # nos permite detectar el rectangulo para poder implementar las coliciones
        self.rect = self.image.get_rect(topleft=(x, y)).inflate(-10, -10)


class Jugador(Entidad):
    def __init__(self, x, y):
        super().__init__(x, y, "assets/jugador.png")
        self.energia = 100
        self.velocidad = 3

    def mover(self, teclas, obstaculos):
        viejo_rect = self.rect.copy()
        if teclas[pygame.K_LEFT]: self.rect.x -= self.velocidad
        if teclas[pygame.K_RIGHT]: self.rect.x += self.velocidad
        if teclas[pygame.K_UP]: self.rect.y -= self.velocidad
        if teclas[pygame.K_DOWN]: self.rect.y += self.velocidad
        # Limitar al borde de la pantalla (800x600)
        self.rect.x = max(0, min(self.rect.x, 800 - self.rect.width))
        self.rect.y = max(0, min(self.rect.y, 600 - self.rect.height))
         # Volver al estado anterior si colisiona con un obstáculo
        if pygame.sprite.spritecollideany(self, obstaculos):
            self.rect = viejo_rect

class Zombie(Entidad):
    def __init__(self, x, y):
        super().__init__(x, y, "assets/zombie.png")
        self.velocidad = 1

    def seguir_jugador(self, jugador, obstaculos):
        viejo_rect = self.rect.copy()
        if jugador.rect.x > self.rect.x: self.rect.x += self.velocidad
        elif jugador.rect.x < self.rect.x: self.rect.x -= self.velocidad
        if jugador.rect.y > self.rect.y: self.rect.y += self.velocidad
        elif jugador.rect.y < self.rect.y: self.rect.y -= self.velocidad
        self.rect.x = max(0, min(self.rect.x, 800 - self.rect.width))
        self.rect.y = max(0, min(self.rect.y, 600 - self.rect.height))
        if pygame.sprite.spritecollideany(self, obstaculos):
            self.rect = viejo_rect

class PuntoSalvavidas(Entidad):
    def __init__(self, x, y):
        super().__init__(x,y,"assets/cura.png")
        self.estado = True

class Obtaculo(Entidad):
    def __init__(self, x, y, ancho=70, alto=70):
        super().__init__(x, y, "assets/carro.png", ancho, alto)

class Juego:
    def __init__(self):
        pygame.init()
        self.pantalla = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Juego de Zombies")
        self.jugador = Jugador(100, 100)
        self.zombies = pygame.sprite.Group(Zombie(300, 300),Zombie(600, 300),Zombie(300, 500),Zombie(400,400))
        self.puntos = pygame.sprite.Group(PuntoSalvavidas(200, 200))
        self.obtaculos = pygame.sprite.Group(Obtaculo(250,250),Obtaculo(350,250),Obtaculo(350,450),Obtaculo(550,450))
        self.todos = pygame.sprite.Group(*self.puntos, self.jugador, *self.zombies, *self.obtaculos)

    def ejecutar(self):
        reloj = pygame.time.Clock()
        corriendo = True

        while corriendo:
            
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    corriendo = False

            teclas = pygame.key.get_pressed()
            self.jugador.mover(teclas,self.obtaculos)

            for z in self.zombies:
                z.seguir_jugador(self.jugador, self.obtaculos)

            # Colisiones
            if pygame.sprite.spritecollideany(self.jugador, self.puntos):
                self.jugador.energia = min(100, self.jugador.energia + 10)
            if pygame.sprite.spritecollideany(self.jugador, self.zombies):
                self.jugador.energia -= 3

            fondo = pygame.image.load("assets/fondo.png").convert()
            self.pantalla.blit(fondo, (0, 0))
            self.todos.draw(self.pantalla)
            pygame.display.flip()
            reloj.tick(60)
            if self.jugador.energia <= 0:
                print("Muerto por loka, sunga enferma, malparida, perra, zorra\n hija de @#$#@# y a usted no la quiere nadie por perdedora\nUsted es una tetranutra")
                corriendo = False # ya no esta corriendo por perdedora malparida sunga

        pygame.quit()


j =  Juego()
j.ejecutar()