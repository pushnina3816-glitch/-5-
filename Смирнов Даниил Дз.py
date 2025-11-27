import pygame
import math
import random

pygame.init()
screen = pygame.display.set_mode((800, 600), pygame.RESIZABLE)
pygame.display.set_caption("Солнечная система")
WIDTH, HEIGHT = 800, 600
cx = WIDTH // 2
cy = HEIGHT // 2   
FPS = 60
clock = pygame.time.Clock()


paused = False


pygame.mixer.init()


try:
    pygame.mixer.music.load("фоновый_звук.mp3")
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(-1)  
    music_playing = True
except:
    print("Не удалось загрузить фоновую музыку")
    music_playing = False


try:
    background = pygame.image.load("фон.jpn")
    background = pygame.transform.scale(background, (WIDTH, HEIGHT))
except:
    background = None


def load_planet_image(filename, radius):
    try:
        image = pygame.image.load(filename)
        return pygame.transform.scale(image, (radius * 2, radius * 2))
    except:
       
        return None


class Planet:
    def __init__(self, screen, radius, orbit_radius, color, speed, angle=0, image_name=None):
        self.screen = screen
        self.radius = radius
        self.orbit_radius = orbit_radius
        self.color = color
        self.speed = speed
        self.angle = angle
        self.x = 0
        self.y = 0
        
        
        if image_name:
            self.image = load_planet_image(image_name, radius)
        else:
            self.image = None

    def update(self, dt):
        global cx, cy
       
        if not paused:
            self.angle += self.speed * dt
        self.x = cx + self.orbit_radius * math.cos(self.angle)
        self.y = cy + self.orbit_radius * math.sin(self.angle)

    def draw(self):
        
        if self.image:
            rect = self.image.get_rect(center=(int(self.x), int(self.y)))
            self.screen.blit(self.image, rect)
        else:
            pygame.draw.circle(self.screen, self.color, (int(self.x), int(self.y)), self.radius)



class Moon:
    def __init__(self, screen, planet, radius, orbit_radius, color, speed, angle=0, image_name=None):
        self.screen = screen
        self.planet = planet  
        self.radius = radius
        self.orbit_radius = orbit_radius
        self.color = color
        self.speed = speed
        self.angle = angle
        self.x = 0
        self.y = 0
        
        
        if image_name:
            self.image = load_planet_image(image_name, radius)
        else:
            self.image = None

    def update(self, dt):
        
        if not paused:
            self.angle += self.speed * dt
        
        self.x = self.planet.x + self.orbit_radius * math.cos(self.angle)
        self.y = self.planet.y + self.orbit_radius * math.sin(self.angle)

    def draw(self):
     
        if self.image:
            rect = self.image.get_rect(center=(int(self.x), int(self.y)))
            self.screen.blit(self.image, rect)
        else:
            pygame.draw.circle(self.screen, self.color, (int(self.x), int(self.y)), self.radius)


class Comet:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.radius = random.randint(2, 5)
     
        self.x = random.randint(0, screen_width)
        self.y = -self.radius
      
        self.speed = random.uniform(2, 6)
    
        self.color = (
            random.randint(200, 255),
            random.randint(200, 255),
            random.randint(220, 255)
        )
       
        self.dx = random.uniform(-1, 1)
        
        
        try:
            self.image = pygame.image.load("комета.jpn")
            self.image = pygame.transform.scale(self.image, (self.radius * 2, self.radius * 2))
        except:
            self.image = None
        
    def update(self, dt):
        
        self.y += self.speed * dt * 60  
        self.x += self.dx * dt * 60
        
    def draw(self, screen):
        
        if self.image:
            rect = self.image.get_rect(center=(int(self.x), int(self.y)))
            screen.blit(self.image, rect)
        else:
            pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)
        
    def is_off_screen(self):
        
        return self.y > self.screen_height + self.radius



try:
    sun_image = pygame.image.load("солнце.jpn")
    sun_image = pygame.transform.scale(sun_image, (40, 40))
except:
    sun_image = None

sun_color = (255, 200, 0)
sun_radius = 20


mercury = Planet(screen, radius=12, orbit_radius=40, color=(128, 128, 128), speed=1.4, image_name="меркурий.png")
venus = Planet(screen, radius=11, orbit_radius=80, color=(255, 165, 0), speed=1.2, image_name="венера.jpn")
earth = Planet(screen, radius=10, orbit_radius=120, color=(100, 150, 255), speed=1, image_name="земля.png")
mars  = Planet(screen, radius=9, orbit_radius=180, color=(255, 100, 80), speed=0.8, image_name="марс.jpn")
jupiter = Planet(screen, radius=8, orbit_radius=200, color=(250, 140, 0), speed=0.6, image_name="юпитер.png")
saturn = Planet(screen, radius=7, orbit_radius=220, color=(255, 255, 255), speed=0.4, image_name="сатурн.jpn")
uranus = Planet(screen, radius=6, orbit_radius=240, color=(0, 0, 255), speed=0.3, image_name="уран.jpn")
neptune = Planet(screen, radius=5, orbit_radius=260, color=(0, 255, 0), speed=0.2, image_name="нептун.jpn")


moon = Moon(screen, earth, radius=3, orbit_radius=15, color=(200, 200, 200), speed=3, image_name="луна.jpn")


comets = []

comet_timer = 0
comet_interval = 2000 

running = True
while running:
    dt = clock.tick(FPS) / 1000.0
    
    
    current_time = pygame.time.get_ticks()
    if current_time - comet_timer > comet_interval:
        comets.append(Comet(WIDTH, HEIGHT))
        comet_timer = current_time
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.VIDEORESIZE:
            WIDTH, HEIGHT = event.w, event.h
            screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
            cx = WIDTH // 2
            cy = HEIGHT // 2
            
            if background:
                background = pygame.transform.scale(background, (WIDTH, HEIGHT))
      
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                paused = not paused
            
            elif event.key == pygame.K_m:
                if music_playing:
                    pygame.mixer.music.pause()
                    music_playing = False
                else:
                    pygame.mixer.music.unpause()
                    music_playing = True
    

    earth.update(dt)
    uranus.update(dt)
    saturn.update(dt)
    jupiter.update(dt)
    venus.update(dt)
    mars.update(dt)
    mercury.update(dt)
    neptune.update(dt)
    
   
    moon.update(dt)
    
   
    for comet in comets[:]:
        comet.update(dt)
        н
        if comet.is_off_screen():
            comets.remove(comet)
    
    
    if background:
        screen.blit(background, (0, 0))
    else:
        screen.fill((0, 0, 20))
    
   
    if sun_image:
        sun_rect = sun_image.get_rect(center=(cx, cy))
        screen.blit(sun_image, sun_rect)
    else:
        pygame.draw.circle(screen, sun_color, (cx, cy), sun_radius)
    
    
    earth.draw()
    uranus.draw()
    saturn.draw()
    jupiter.draw()
    mars.draw()
    venus.draw()
    mercury.draw()
    neptune.draw()
    
    
    moon.draw()
    
    
    for comet in comets:
        comet.draw(screen)
    
    
    if paused:
        font = pygame.font.SysFont(None, 36)
        pause_text = font.render("ПАУЗА", True, (255, 0, 0))
        screen.blit(pause_text, (10, 10))
    
    
    font = pygame.font.SysFont(None, 24)
    controls_text = font.render("Управление: ПРОБЕЛ - пауза, M - музыка вкл/выкл", True, (200, 200, 200))
    screen.blit(controls_text, (10, HEIGHT - 30))
    
    pygame.display.flip()

pygame.quit()