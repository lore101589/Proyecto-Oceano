import pygame
import random
import math

# =============================================================================================
# JUEGO: EL PEZ HAMBRIENTO
# Objetivo: Atrapar gusanos, para ganar puntos y esquivar cangrejos para no perder vidas.
# Controles: Flechas / WASD / R reinicia / ESC salir
# Se importaro las siguetes lirerias pygame, random y math               
# ==============================================================================================

ANCHO = 900
ALTO = 650
FPS = 60

COLOR_PEZ = (255, 165, 0)
COLOR_PEZ_2 = (255, 220, 120)
COLOR_PEZ_SOMBRA = (200, 120, 0)
COLOR_GUSANO = (255, 70, 70)
COLOR_GUSANO_2 = (255, 150, 150)
COLOR_GUSANO_BORDE = (180, 30, 30)
COLOR_BURBUJA = (200, 235, 255)
COLOR_TEXTO = (255, 255, 255)
COLOR_TEXT1 = (247, 10, 10)

class Pez:
    def __init__(self):
        self.x = ANCHO // 2
        self.y = ALTO // 2
        self.vel = 6
        self.tam = 28
        self.vida = 3
        self.puntaje = 0
        self.direccion = 1
        self.anim = 0
        self.invulnerable = 0
        self.efecto_comer = 0
    def mover(self, teclas):
        dx = 0
        dy = 0
        if teclas[pygame.K_LEFT] or teclas[pygame.K_a]:
            dx = -self.vel
            self.direccion = -1
        if teclas[pygame.K_RIGHT] or teclas[pygame.K_d]:
            dx = self.vel
            self.direccion = 1
        if teclas[pygame.K_UP] or teclas[pygame.K_w]:
            dy = -self.vel
        if teclas[pygame.K_DOWN] or teclas[pygame.K_s]:
            dy = self.vel
        if dx!= 0 and dy!= 0:
            dx *= 0.707
            dy *= 0.707
        self.x += dx
        self.y += dy
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
    def dibujar(self, pantalla):
        if self.invulnerable % 10 < 5:
            scale = 1.0 + (self.efecto_comer / 15) * 0.2
            tam = int(self.tam * scale)
            pygame.draw.ellipse(pantalla, COLOR_PEZ_SOMBRA, (self.x - tam, self.y - tam//2 + 4, tam*2, tam))
            pygame.draw.ellipse(pantalla, COLOR_PEZ, (self.x - tam, self.y - tam//1.5, tam*2, int(tam*1.2)))
            pygame.draw.ellipse(pantalla, COLOR_PEZ_2, (self.x - tam//2, self.y - tam//3, tam, tam//2))
            cola_x = self.x - tam * self.direccion
            cola_anim = math.sin(self.anim) * 5
            puntos_cola = [(cola_x, self.y + cola_anim), (cola_x - 18 * self.direccion, self.y - 14 + cola_anim), (cola_x - 18 * self.direccion, self.y + 14 + cola_anim)]
            pygame.draw.polygon(pantalla, COLOR_PEZ, puntos_cola)
            aleta_y = self.y + 8
            pygame.draw.ellipse(pantalla, COLOR_PEZ_2, (self.x - 10, aleta_y, 18, 8))
            ojo_x = self.x + 10 * self.direccion
            pygame.draw.circle(pantalla, (255,255,255), (int(ojo_x), int(self.y - 6)), 9)
            pygame.draw.circle(pantalla, (0,0,0), (int(ojo_x + 3*self.direccion), int(self.y - 6)), 5)
            pygame.draw.circle(pantalla, (255,255,255), (int(ojo_x+1), int(self.y-8)), 2)
            boca_x = self.x + tam * self.direccion * 0.85
            boca_open = 3 + math.sin(self.anim*2)*1
            pygame.draw.circle(pantalla, (0,0,0), (int(boca_x), int(self.y + 6)), int(boca_open))
    def rect(self):
        return pygame.Rect(self.x - self.tam, self.y - self.tam, self.tam*2, self.tam*1.5)

class Gusano:
    def __init__(self):
        self.respawn()#coloca al gusano en una posicion aleatoria y asigna velocidades
        self.tam_w = 22 #tamaño ancho
        self.tam_h = 12# tamaño alto
        self.ondulacion = random.uniform(0, 6.28)# permite animarlo
        self.vel_mult = 1.0# multiplicador de velocidad que puede aumentar cundo superas niveles
    def respawn(self): #cada vez que un gusano se lo come .el pez ,el programa llama al metodo para ubbicarlo en otra posicion
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
    def dibujar(self, pantalla):
        off = math.sin(self.ondulacion) * 4
        c1 = COLOR_GUSANO if self.tipo==0 else (100,255,100) if self.tipo==1 else (255,255,80)
        c2 = COLOR_GUSANO_2 if self.tipo==0 else (180,255,180) if self.tipo==1 else (255,255,180)
        pygame.draw.ellipse(pantalla, COLOR_GUSANO_BORDE, (self.x-2, self.y+off-2, self.tam_w+4, self.tam_h+4))
        pygame.draw.ellipse(pantalla, c1, (self.x, self.y+off, self.tam_w, self.tam_h))
        pygame.draw.ellipse(pantalla, c2, (self.x+3, self.y+off+2, 8, 5))
        pygame.draw.circle(pantalla, (0,0,0), (int(self.x+self.tam_w-4), int(self.y+off+5)), 2)
    def rect(self):
        return pygame.Rect(self.x, self.y, self.tam_w, self.tam_h)

class Cangrejo:
    def __init__(self):
        self.x = random.randint(0, ANCHO-60)
        self.y_base = ALTO - 75
        self.y = self.y_base
        self.vel = random.uniform(1.5, 3.2)
        self.dir = random.choice([-1,1])
        self.tam = 38
        self.anim =random.randint(0,628)/100.0
        #---- nuevo para salto------
        self.vy = 0
        self.en_suelo = True
        self.tiempo_salto = 0
        self.gravedad =0.55
        self.fuerza_salto = random.uniform(-12,-15)# que tan altosalta

    def mover(self, pez_x=None):
        #movimiento horizontal

        self.x += self.vel * self.dir
        self.anim += 0.15
        if self.x < 0 or self.x >ANCHO-self.tam:
            self.dir *= -1
        if random.randint(0, 200) == 0:
            self.dir *= -1

        #-----logica de salto-----------------------
        self.tiempo_salto += 1

        debe_saltar = False

        #----------si esta en el suelo,decide si salta
        if self.en_suelo:
        
            if self.tiempo_salto> random.randint(90,160):
                debe_saltar = True
            #si el pez esta cerca, salta para atraparlo
            if pez_x is not None and abs(self.x- pez_x) <180 and random.randint(0,100)<40:
                debe_saltar = True

        if debe_saltar:
            self.vy = self.fuerza_salto
            self.en_suelo=False
            self.tiempo_salto= 0

        else:
             # Está en el aire
            self.vy += self.gravedad
            self.y += self.vy
            if self.y >= self.y_base:
                self.y = self.y_base
                self.vy = 0
                self.en_suelo = True

    def dibujar(self, pantalla):
        y_off = self.y + (2 if int(self.anim)%2==0 else -2)
        # sombra cuando salta
        if not self.en_suelo:
            pygame.draw.ellipse(pantalla, (0,0,0,100), (self.x, self.y_base+25, self.tam, 8))
        
        pygame.draw.ellipse(pantalla, CANGREJO, (self.x, y_off, self.tam, self.tam//1.4))
        pygame.draw.ellipse(pantalla, CANGREJO2, (self.x+5, y_off+4, self.tam-10, 10))
        pygame.draw.circle(pantalla, NEGRO, (int(self.x+10), int(y_off+10)), 4)
        pygame.draw.circle(pantalla, NEGRO, (int(self.x+28), int(y_off+10)), 4)
        px1 = self.x-8+ (3 if int(self.anim)%2==0 else -3)
        px2 = self.x+self.tam+8+ (-3 if int(self.anim)%2==0 else 3)
        pygame.draw.circle(pantalla, CANGREJO, (int(px1), int(y_off+12)), 10)
        pygame.draw.circle(pantalla, CANGREJO, (int(px2), int(y_off+12)), 10)

    def rect(self):
        return pygame.Rect(self.x, self.y, self.tam, self.tam)

    def dibujar(self, pantalla, imagen_cangrejo):  
        pantalla.blit(imagen_cangrejo, (self.x - self.tam, self.y - self.tam))

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
    def dibujar(self, pantalla):
        pygame.draw.circle(pantalla, COLOR_BURBUJA, (int(self.x), int(self.y)), self.tam, 1)
          
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

def dibujar_fondo(pantalla, fondo):
    pantalla.blit(fondo,(0, 0))

def dibujar_corazon(pantalla, x, y, tam):   #######nuevo
    rojo = (255, 0, 0)
    pygame.draw.circle(pantalla, rojo, (x + tam//3, y + tam//3), tam//3)
    pygame.draw.circle(pantalla, rojo, (x + 2*tam//3, y + tam//3), tam//3)
    puntos = [(x, y + tam//3),(x + tam, y + tam//3),(x + tam//2, y + tam)]
    pygame.draw.polygon(pantalla, rojo, puntos)

def dibujar_hud(pantalla, pez, nivel, fuente, fuente_chica):
    txt_puntaje = fuente.render(f"Puntos: {pez.puntaje}", True, COLOR_TEXTO)
    pantalla.blit(txt_puntaje, (15, 15))
    txt_nivel = fuente.render(f"Nivel: {nivel}", True, COLOR_TEXTO)
    pantalla.blit(txt_nivel, (15, 50))
    txt_vida = fuente.render(f"Vidas:", True, COLOR_TEXTO)  #se modifico pero se puede borrar y que aparezcan los corazones solos
    pantalla.blit(txt_vida, (ANCHO-220, 15))
    for i in range(pez.vida):######se agrego
        dibujar_corazon(pantalla, ANCHO-115 + i*30, 20, 24)
    txt_ctrl = fuente_chica.render("WASD/Flechas mover | R reinicia | ESC salir", True, COLOR_TEXT1)#se cambio color texto
    pantalla.blit(txt_ctrl, (ANCHO//2 - txt_ctrl.get_width()//2, ALTO-25))

def mostrar_menu(pantalla, fondo, fuente, fuente_grande):     ##se modifico
    dibujar_fondo(pantalla, fondo)
    titulo = fuente_grande.render("EL PEZ HAMBRIENTO", True, (255,255,0))
    pantalla.blit(titulo, (ANCHO//2 - titulo.get_width()//2, 150))
    sub1 = fuente.render("Atrapa gusanos! Esquiva cangrejos!", True, COLOR_TEXTO)  ######se modifico
    sub2 = fuente.render("Sobreviví a las profundidades del océano", True, COLOR_TEXTO)  ####se modifico
    sub3 = fuente.render("Presiona ESPACIO para jugar", True, (COLOR_TEXT1))   #######se modifico
    pantalla.blit(sub1, (ANCHO//2 - sub1.get_width()//2, 250))
    pantalla.blit(sub2, (ANCHO//2 - sub2.get_width()//2, 290))
    pantalla.blit(sub3, (ANCHO//2 - sub3.get_width()//2, 350))
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

def mostrar_game_over(pantalla, pez, fuente, fuente_grande):
    overlay = pygame.Surface((ANCHO, ALTO))
    overlay.set_alpha(180)
    overlay.fill((0,0,0))
    pantalla.blit(overlay, (0,0))
    txt = fuente_grande.render("GAME OVER", True, (255,50,50))
    pantalla.blit(txt, (ANCHO//2 - txt.get_width()//2, 200))
    txt2 = fuente.render(f"Puntaje final: {pez.puntaje}", True, COLOR_TEXTO)
    pantalla.blit(txt2, (ANCHO//2 - txt2.get_width()//2, 280))
    txt3 = fuente.render("R para reiniciar o ESC para salir", True, COLOR_TEXTO)
    pantalla.blit(txt3, (ANCHO//2 - txt3.get_width()//2, 330))
    pygame.display.flip()
    while True:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit     
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_r:
                    return True
                if e.key == pygame.K_ESCAPE:
                    pygame.quit()
                    raise SystemExit  

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
    pygame.mixer.init()    
    pantalla = pygame.display.set_mode((ANCHO, ALTO))
    pygame.display.set_caption("El Pez Hambriento")
    reloj = pygame.time.Clock()

    #imagenes se cargan una sola vez y asi evitamos que se ralentice el juego
    fondo = pygame.image.load("pozadina.png").convert()
    fondo = pygame.transform.scale(fondo,(ANCHO, ALTO)) 
    imagen_cangrejo = pygame.image.load("cangrejo.png").convert_alpha()
    imagen_cangrejo = pygame.transform.scale(imagen_cangrejo, (100, 100))

    fuente = pygame.font.SysFont("Arial", 28, bold=True)
    fuente_chica = pygame.font.SysFont("Arial", 18)
    fuente_grande = pygame.font.SysFont("Arial", 60, bold=True)

    #musica de fondo
    pygame.mixer.music.load("sound_background.wav")  
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(-1)

    #sonido de game over
    sonido_game_over = pygame.mixer.Sound("sounds_game_over.wav")   
    sonido_game_over.set_volume(0.1)

    #sonido de golpe
    sonido_golpe = pygame.mixer.Sound("loselife.wav") 
    sonido_golpe.set_volume(0.2)

    #sonido de comida
    sonido_comida = pygame.mixer.Sound("sound_eat1.wav")
    sonido_comida.set_volume(0.2)
    mostrar_menu(pantalla, fondo, fuente, fuente_grande)
    pez = Pez()
    gusanos = [Gusano() for _ in range(3)]
    cangrejos = [Cangrejo() for _ in range(1)]
    burbujas = [Burbuja() for _ in range(25)]
    particulas = []
    nivel = 1
    tiempo_nivel = 0
    tiempo_total = 0
    jugando = True
    contador_fps = 0 
   
    while jugando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                jugando = False
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    jugando = False
                 
        if not jugando:   
            break

        teclas = pygame.key.get_pressed()
        pez.mover(teclas)
        for b in burbujas:
            b.mover()
        for g in gusanos:
            g.mover(nivel)
        for c in cangrejos:
            c.mover(pez.x)
        for p in particulas[:]:
            p.mover()
            if p.vida <= 0:
                particulas.remove(p)
        #colision con los gusanos  
        for g in gusanos:
            if pez.rect().colliderect(g.rect()):
                pez.comer()
                sonido_comida.play()
                for _ in range(10):
                    particulas.append(Particula(g.x, g.y))
                g.respawn()
                g.vel_mult += 0.05
        #colision con los cangrejos
        for c in cangrejos:
            if math.hypot(pez.x - c.x, pez.y - c.y) < 70:
                if pez.golpe():
                    if pez.vida <= 0:
                        pygame.mixer.music.stop()  
                        sonido_game_over.play()     
                        reiniciar = mostrar_game_over(pantalla, pez, fuente, fuente_grande)  ######se modifico
                        if reiniciar:
                            pygame.mixer.music.play(-1)
                            pez = Pez()
                            gusanos = [Gusano() for _ in range(3)]
                            cangrejos = [Cangrejo() for _ in range(1)]
                            burbujas = [Burbuja() for _ in range(25)]    
                            particulas = []    
                            nivel = 1
                            tiempo_nivel = 0    
                            continue              
                        else:
                            jugando = False
                        break 
                    else:
                        sonido_golpe.play()  
        if not jugando:  
            break

        #bucle que aumenta nivel
        tiempo_nivel += 1
        if tiempo_nivel > FPS * 30:
            nivel += 1
            tiempo_nivel = 0
            num_g, num_c = crear_nivel(nivel)
            while len(gusanos) < num_g:
                gusanos.append(Gusano())
            while len(cangrejos) < num_c:
                cangrejos.append(Cangrejo())

        dibujar_fondo(pantalla, fondo)  
        for b in burbujas:
            b.dibujar(pantalla)
        for g in gusanos:
            g.dibujar(pantalla)
        for c in cangrejos:
            c.dibujar(pantalla, imagen_cangrejo)
        for p in particulas:
            p.dibujar(pantalla)
        pez.dibujar(pantalla)

        dibujar_hud(pantalla, pez, nivel, fuente, fuente_chica)
        prog = tiempo_nivel / (FPS*30)
        pygame.draw.rect(pantalla, (50,50,50), (ANCHO//2 - 100, 20, 200, 12))
        pygame.draw.rect(pantalla, (0,255,100), (ANCHO//2 - 100, 20, int(200*prog), 12))
        pygame.display.flip()

        #actualiza el FPS
        contador_fps += 1

        if contador_fps >= 30:
            pygame.display.set_caption(f"El Pez Hambriento - FPS: {reloj.get_fps():.1f}")
            contador_fps = 0
        reloj.tick(FPS)
    pygame.quit()

if __name__ == "__main__":
    main()