import pygame
from pygame.locals import *
from sys import exit
import random

pygame.init()

# Configurações da tela
altura = 700
largura = 1000
tela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption("Star Wars: Contratos Galácticos")

# Imagens
icon = pygame.image.load("assets/icon/icone-star-wars-game.png")
background = pygame.image.load("assets/background/Starfields/Starfield_03-1024x1024.png")
spaceship = pygame.image.load("assets/spaceship/PNG_Parts&Spriter_Animation/Ship3/Ship3.png")
laserimg = pygame.image.load("assets/spaceship/PNG_Animations/Shots/Shot3/shot3_asset.png")
asteroidimg = pygame.image.load("assets/asteroid/Asteroids/PNGs/Asteroid 01 - Base.png")

# Carregar frames da explosão
explosion_images = [
    pygame.image.load(f"assets/asteroid/Asteroids/PNGs/asteroid_explosion/explosion_{i}.png").convert_alpha()
    for i in range(7)
]

# Nave
spaceshipX = 80
spaceshipY = 350
changeY = 0

# Meteoros
asteroids = []
for _ in range(20):  # quantidade de meteoros simultâneos
    asteroids.append({
        "x": random.randint(1000, 1500),
        "y": random.randint(-20, 615)
    })

# Outros elementos
lasers = []
explosoes = []
score= 0
colisao_ocorreu= False

# Pontuação
fonte=pygame.font.SysFont("Arial", 26, "bold")
fonte_game_over=pygame.font.SysFont("Arial", 90, "bold")

# Ícone
pygame.display.set_icon(icon)

# Funções
def player():
    tela.blit(spaceship, (spaceshipX, spaceshipY))

def disparar_lasers():
    lasers.append({
        "x": spaceshipX + 76,
        "y": spaceshipY + 36
    })

def pontuação():
    img=fonte.render(f'Score: {score}', True, "white")
    tela.blit(img,(10,10))

def game_over():
    img=fonte_game_over.render("Game Over", True, "white")
    tela.blit(img,(295,305))
    

# Loop principal
while True:
    tela.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()

        if event.type == KEYDOWN:
            if event.key == K_UP:
                changeY = -0.7
            if event.key == K_DOWN:
                changeY = 0.7
            if event.key == K_SPACE:
                disparar_lasers()

        if event.type == KEYUP:
            if event.key in (K_UP, K_DOWN):
                changeY = 0

    # Movimento da nave
    spaceshipY += changeY
    if spaceshipY < -40:
        spaceshipY = -40
    if spaceshipY > 615:
        spaceshipY = 615

    if not colisao_ocorreu:
        
        # Atualizar meteoros
        for asteroid in asteroids:
            asteroid["x"] -= 0.4
            if asteroid["x"] < -100:
                asteroid["x"] = random.randint(1000, 1500)
                asteroid["y"] = random.randint(-20, 615)

                
        # Atualizar lasers e detectar colisões
        for laser in lasers[:]:
            laser["x"] += 1.25
            laser_rect = pygame.Rect(laser["x"] + 10, laser["y"] + 5, 20, 10)

            for asteroid in asteroids:
                asteroid_rect = pygame.Rect(asteroid["x"], asteroid["y"], asteroidimg.get_width()*0.5, asteroidimg.get_height()*0.5)
                
                # Contato do laser no asteroid
                if laser_rect.colliderect(asteroid_rect):
                    explosoes.append({
                        "x": asteroid["x"],
                        "y": asteroid["y"],
                        "frame": 0,
                        "contador": 0
                    })
                    lasers.remove(laser)
                    asteroid["x"] = random.randint(1000, 1500)
                    asteroid["y"] = random.randint(-20, 615)
                    
                    score+=5
                    print(score)



            if laser["x"] > largura:
                lasers.remove(laser)


        # Atualizar explosões
        for explosao in explosoes[:]:
            explosao["contador"] += 0.25
            if explosao["contador"] % 5 == 0:
                explosao["frame"] += 1
            if explosao["frame"] < len(explosion_images):
                img = explosion_images[explosao["frame"]]
                tela.blit(img, (explosao["x"], explosao["y"]))
            else:
                explosoes.remove(explosao)

        # Desenhar elementos
        player()
        for asteroid in asteroids:
            tela.blit(asteroidimg, (asteroid["x"], asteroid["y"]))
        for laser in lasers:
            tela.blit(laserimg, (laser["x"], laser["y"]))

        # Rect do player
        player_rect = pygame.Rect(spaceshipX, spaceshipY, spaceship.get_width()*0.5, spaceship.get_height()*0.3)

        # Verificar colisão do meteoro com a nave
        for asteroid in asteroids:
            asteroid_rect = pygame.Rect(asteroid["x"], asteroid["y"], asteroidimg.get_width()*0.2, asteroidimg.get_height()*0.1)

            if player_rect.colliderect(asteroid_rect):
                colisao_ocorreu=True
                game_over()

        pontuação()
        pygame.display.update()
