import pygame
import random
import math

#constantes para la superficie de dibujo
ANCHO = 900
ALTO = 650
FPS = 60

COLOR_AGUA_1 = (16, 110, 190)
COLOR_AGUA_2 = (30, 144, 255)
COLOR_ARENA = (194, 178, 128)
COLOR_ARENA_2 = (210, 190, 140)
COLOR_GUSANO = (255, 70, 70)
COLOR_GUSANO_2 = (255, 150, 150)
COLOR_GUSANO_BORDE = (180, 30, 30)
COLOR_CANGREJO = (200, 50, 30)
COLOR_CANGREJO_2 = (220, 80, 50)
COLOR_BURBUJA = (200, 235, 255)
COLOR_TEXTO = (255, 255, 255)


#clase PEZ
class Pez():
    def __init__(self):
        #atributos de la clase especificos
        self.x = ANCHO//2
        self.y = ALTO//2
        self.vel = 6
        self.tam = 28
        self.vida = 3
        self.puntaje = 0
        self.direccion = 1
        self.anim = 0
        self.invulnerable = 0
        self.efecto_comer = 0
    
    def mover(self, teclas):
        dirx = 0
        diry = 0
        if teclas[pygame.K_LEFT]:
            dirx = -self.vel
            self.direccion = -1
        if teclas[pygame.K_RIGHT]:
            dirx = self.vel
            self.direccion = 1
        if teclas[pygame.K_UP]:
            diry = -self.vel
        if teclas[pygame.K_DOWN]:
            diry = self.vel
        if dirx!= 0 and diry!= 0:
            dirx *= 0.707
            diry *= 0.707
        self.x += dirx
        self.y += diry
        self.x = max(self.tam, min(ANCHO - self.tam, self.x))
        self.y = max(self.tam, min(ALTO - 80 - self.tam, self.y))
        self.anim += 0.25
        if self.invulnerable > 0:
            self.invulnerable -= 1
        if self.efecto_comer > 0:
            self.efecto_comer -= 1
    
    def comer(self):
        self.puntaje += 1
        self.efecto_comer = 15
    
    def golpe(self):
        if self.invulnerable == 0:
            self.vida -= 1
            self.invulnerable = 90
            return True
        return False

    def dibujar(self, ventana):
        #imagen original (mirando a la derecha)
        self.imagen = pygame.image.load("fishnemo.png").convert_alpha()
        self.imagen = pygame.transform.scale(self.imagen, (self.tam * 2, self.tam * 2))
        
        #si self.direccion es -1 (va a la izquierda), la imagen se volvea horizontalmente
        if self.direccion == -1:
            self.imagen = pygame.transform.flip(self.imagen, True, False)
        else:
            self.imagen = self.imagen

        #imagen se dibuja en la ventana
        ventana.blit(self.imagen, (self.x - self.tam, self.y - self.tam))


    def rect(self):
        return pygame.Rect(self.x - self.tam, self.y - self.tam, self.tam*2, self.tam*1.5)

class Gusano:
    def __init__(self):
        self.respawn()
        self.tam_w = 22
        self.tam_h = 12
        self.ondulacion = random.uniform(0, 6.28)
        self.tipo = random.randint(0,2)
        self.vel_mult = 1.0
    def respawn(self):
        self.x = random.randint(40, ANCHO-60)
        self.y = random.randint(40, ALTO-150)
        self.vel_x = random.choice([-3.5, -3, 3, 3.5])
        self.vel_y = random.choice([-3.5, -3, 3, 3.5])
        self.tipo = random.randint(0,2)
    def mover(self, nivel):
        factor = 1.0 + nivel * 0.15
        self.x += self.vel_x * factor * self.vel_mult
        self.y += self.vel_y * factor * self.vel_mult
        if self.x < 10 or self.x > ANCHO - 30:
            self.vel_x *= -1
            self.x = max(10, min(ANCHO-30, self.x))
        if self.y < 10 or self.y > ALTO - 110:
            self.vel_y *= -1
            self.y = max(10, min(ALTO-110, self.y))
        if random.randint(0, 70) == 0:
            self.vel_x = random.uniform(-4, 4)
            self.vel_y = random.uniform(-4, 4)
        self.ondulacion += 0.35
    def dibujar(self, ventana):
        off = math.sin(self.ondulacion) * 4
        c1 = COLOR_GUSANO if self.tipo==0 else (100,255,100) if self.tipo==1 else (255,255,80)
        c2 = COLOR_GUSANO_2 if self.tipo==0 else (180,255,180) if self.tipo==1 else (255,255,180)
        pygame.draw.ellipse(ventana, COLOR_GUSANO_BORDE, (self.x-2, self.y+off-2, self.tam_w+4, self.tam_h+4))
        pygame.draw.ellipse(ventana, c1, (self.x, self.y+off, self.tam_w, self.tam_h))
        pygame.draw.ellipse(ventana, c2, (self.x+3, self.y+off+2, 8, 5))
        pygame.draw.circle(ventana, (0,0,0), (int(self.x+self.tam_w-4), int(self.y+off+5)), 2)
    def rect(self):
        return pygame.Rect(self.x, self.y, self.tam_w, self.tam_h)

class Cangrejo:
    def __init__(self):
        self.x = random.randint(0, ANCHO-60)
        self.y = ALTO - 100
        self.vel = random.uniform(1.2, 2.8)
        self.dir = random.choice([-1,1])
        self.tam = 38
        self.anim = random.uniform(0, 6.28)
    def mover(self):
        self.x += self.vel * self.dir
        self.anim += 0.15
        if self.x < 0:
            self.x = 0
            self.dir *= -1
        if self.x > ANCHO - self.tam:
            self.x = ANCHO - self.tam
            self.dir *= -1
        if random.randint(0, 200) == 0:
            self.dir *= -1
    def dibujar(self, ventana):
        y_off = math.sin(self.anim)*2
        pygame.draw.ellipse(ventana, COLOR_CANGREJO, (self.x, self.y+y_off, self.tam, self.tam//1.4))
        pygame.draw.ellipse(ventana, COLOR_CANGREJO_2, (self.x+5, self.y+4+y_off, self.tam-10, 10))
        pygame.draw.circle(ventana, (0,0,0), (int(self.x+10), int(self.y+10+y_off)), 4)
        pygame.draw.circle(ventana, (0,0,0), (int(self.x+28), int(self.y+10+y_off)), 4)
        pygame.draw.circle(ventana, (255,255,255), (int(self.x+11), int(self.y+9+y_off)), 1)
        px1 = self.x - 8 + math.sin(self.anim)*3
        px2 = self.x + self.tam + 8 - math.sin(self.anim)*3
        pygame.draw.circle(ventana, COLOR_CANGREJO, (int(px1), int(self.y+12+y_off)), 10)
        pygame.draw.circle(ventana, COLOR_CANGREJO, (int(px2), int(self.y+12+y_off)), 10)
    def rect(self):
        return pygame.Rect(self.x, self.y, self.tam, self.tam)

class Burbuja:
    def __init__(self):
        self.reset(True)
    def reset(self, first=False):
        self.x = random.randint(0, ANCHO)
        self.y = random.randint(0, ALTO) if first else ALTO + random.randint(10, 200)
        self.vel = random.uniform(0.6, 2.8)
        self.tam = random.randint(3, 12)
        self.burbuja = random.uniform(0, 6.28)
        self.burbuja_speed = random.uniform(0.03, 0.09)
    def mover(self):
        self.y -= self.vel
        self.burbuja += self.burbuja_speed
        self.x += math.sin(self.burbuja) * 0.8
        if self.y < -20:
            self.reset()
    def dibujar(self, ventana):
        pygame.draw.circle(ventana, COLOR_BURBUJA, (int(self.x), int(self.y)), self.tam, 1)



class Particula:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vx = random.uniform(-3,3)
        self.vy = random.uniform(-3,3)
        self.vida = 20
        self.color = random.choice([(255,255,150),(255,200,100),(255,255,255)])
    def mover(self):
        self.x += self.vx
        self.y += self.vy
        self.vida -= 1
        self.vy += 0.1
    def dibujar(self, p):
        if self.vida>0:
            pygame.draw.circle(p, self.color, (int(self.x), int(self.y)), 3)

def dibujar_fondo(ventana, tiempo):
    fondo = pygame.image.load("pozadina.png").convert()
    fondo = pygame.transform.scale(fondo, (ANCHO, ALTO))
    ventana.blit(fondo, (0, 0))

def dibujar_hud(ventana, pez, nivel, fuente, fuente_chica):
    txt_puntaje = fuente.render(f"Puntos: {pez.puntaje}", True, COLOR_TEXTO)
    ventana.blit(txt_puntaje, (15, 15))
    txt_nivel = fuente.render(f"Nivel: {nivel}", True, COLOR_TEXTO)
    ventana.blit(txt_nivel, (15, 50))
    txt_vida = fuente.render(f"Vidas: {pez.vida} <3", True, COLOR_TEXTO)
    ventana.blit(txt_vida, (ANCHO-150, 15))
    txt_ctrl = fuente_chica.render("Flechas mover | R reinicia | ESC salir", True, COLOR_TEXTO)
    ventana.blit(txt_ctrl, (ANCHO//2 - txt_ctrl.get_width()//2, ALTO-25))

def mostrar_menu(ventana, fuente, fuente_grande):
    dibujar_fondo(ventana, 0)
    #CAMBIE COLOR DEL TITULO
    titulo = fuente_grande.render("EL PEZ HAMBRIENTO", True, (247, 10, 10))
    ventana.blit(titulo, (ANCHO//2 - titulo.get_width()//2, 150))
    sub1 = fuente.render("Atrapa gusanos! Esquiva cangrejos!", True, COLOR_TEXTO)
    sub2 = fuente.render("Cada 30s subis de nivel", True, COLOR_TEXTO)
    #CAMBIE COLOR DEL TITULO
    sub3 = fuente.render("Presiona ESPACIO para jugar", True, (247, 10, 10))
    ventana.blit(sub1, (ANCHO//2 - sub1.get_width()//2, 250))
    ventana.blit(sub2, (ANCHO//2 - sub2.get_width()//2, 290))
    ventana.blit(sub3, (ANCHO//2 - sub3.get_width()//2, 350))
    pygame.display.flip()
    esperando = True
    while esperando:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                exit()
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_SPACE:
                    esperando = False
                if e.key == pygame.K_ESCAPE:
                    pygame.quit()
                    exit()

def mostrar_game_over(ventana, pez, fuente, fuente_grande):
    overlay = pygame.Surface((ANCHO, ALTO))
    overlay.set_alpha(180)
    overlay.fill((0,0,0))
    ventana.blit(overlay, (0,0))
    txt = fuente_grande.render("GAME OVER", True, (255,50,50))
    ventana.blit(txt, (ANCHO//2 - txt.get_width()//2, 200))
    txt2 = fuente.render(f"Puntaje final: {pez.puntaje}", True, COLOR_TEXTO)
    ventana.blit(txt2, (ANCHO//2 - txt2.get_width()//2, 280))
    txt3 = fuente.render("R para reiniciar o ESC para salir", True, COLOR_TEXTO)
    ventana.blit(txt3, (ANCHO//2 - txt3.get_width()//2, 330))
    pygame.display.flip()
    while True:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                exit()
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_r:
                    return True
                if e.key == pygame.K_ESCAPE:
                    pygame.quit()
                    exit()

def crear_nivel(nivel):
    num_gusanos = 2 + nivel
    num_cangrejos = 1 + nivel//2
    if num_gusanos > 6:
        num_gusanos = 6
    if num_cangrejos > 4:
        num_cangrejos = 4
    return num_gusanos, num_cangrejos

def main():
    pygame.init()
    ventana = pygame.display.set_mode((ANCHO, ALTO))
    pygame.display.set_caption("El Pez Hambriento")
    reloj = pygame.time.Clock()
    fuente = pygame.font.SysFont("Arial", 28, bold=True)
    fuente_chica = pygame.font.SysFont("Arial", 18)
    fuente_grande = pygame.font.SysFont("Arial", 60, bold=True)
    mostrar_menu(ventana, fuente, fuente_grande)
    pez = Pez()
    gusanos = [Gusano() for _ in range(3)]
    cangrejos = [Cangrejo() for _ in range(1)]
    burbujas = [Burbuja() for _ in range(25)]
   
    particulas = []
    nivel = 1
    tiempo_nivel = 0
    jugando= True
    tiempo_total = 0
    while corriendo:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                jugando = False
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    jugando = False
                if evento.key == pygame.K_r:
                    pez = Pez()
                    gusanos = [Gusano() for _ in range(3)]
                    cangrejos = [Cangrejo() for _ in range(1)]
                    nivel = 1
                    tiempo_nivel = 0
        teclas = pygame.key.get_pressed()
        pez.mover(teclas)
        for b in burbujas:
            b.mover()
        for g in gusanos:
            g.mover(nivel)
        for c in cangrejos:
            c.mover()
        for p in particulas[:]:
            p.mover()
            if p.vida <= 0:
                particulas.remove(p)
        for g in gusanos:
            if pez.rect().colliderect(g.rect()):
                pez.comer()
                for _ in range(10):
                    particulas.append(Particula(g.x, g.y))
                g.respawn()
                g.vel_mult += 0.05
        for c in cangrejos:
            if pez.rect().colliderect(c.rect()):
                if pez.golpe():
                    if pez.vida <= 0:
                        if mostrar_game_over(ventana, pez, fuente, fuente_grande):
                            pez = Pez()
                            gusanos = [Gusano() for _ in range(3)]
                            cangrejos = [Cangrejo() for _ in range(1)]
                            nivel = 1
                            tiempo_nivel = 0
                            tiempo_total = 0
                            particulas = []
                        else:
                            jugando = False
        tiempo_nivel += 1
        tiempo_total += 1
        if tiempo_nivel > FPS * 30:
            nivel += 1
            tiempo_nivel = 0
            num_g, num_c = crear_nivel(nivel)
            while len(gusanos) < num_g:
                gusanos.append(Gusano())
            while len(cangrejos) < num_c:
                cangrejos.append(Cangrejo())
        dibujar_fondo(ventana, tiempo_total)
        for b in burbujas:
            b.dibujar(ventana)
        for g in gusanos:
            g.dibujar(ventana)
        for c in cangrejos:
            c.dibujar(ventana)
        for p in particulas:
            p.dibujar(ventana)
        pez.dibujar(ventana)
        dibujar_hud(ventana, pez, nivel, fuente, fuente_chica)
        prog = tiempo_nivel / (FPS*30)
        pygame.draw.rect(ventana, (50,50,50), (ANCHO//2 - 100, 20, 200, 12))
        pygame.draw.rect(ventana, (0,255,100), (ANCHO//2 - 100, 20, int(200*prog), 12))
        pygame.display.flip()
        reloj.tick(FPS)
    pygame.quit()

if __name__ == "__main__":
    main()