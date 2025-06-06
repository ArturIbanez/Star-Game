import pygame
from pygame.locals import *
from sys import exit
import random

pygame.init()

# -=-=-TELA-=-=-
altura = 700
largura = 1000
tela = pygame.display.set_mode((largura, altura))

pygame.display.set_icon(icon)
pygame.display.set_caption("Star Wars: Contratos Galácticos")


# -=-=-IMAGES_LOAD-=-=-
icon = pygame.image.load("assets/icon/icone-star-wars-game.png")
background = pygame.image.load("assets/background/Starfields/Starfield_03-1024x1024.png")
spaceship = pygame.image.load("assets/spaceship/PNG_Parts&Spriter_Animation/Ship3/Ship3.png")
laserimg = pygame.image.load("assets/spaceship/PNG_Animations/Shots/Shot3/shot3_asset.png")
asteroidimg = pygame.image.load("assets/asteroid/Asteroids/PNGs/Asteroid 01 - Base.png")
explosion_images = [
    pygame.image.load(f"assets/asteroid/Asteroids/PNGs/asteroid_explosion/explosion_{i}.png").convert_alpha()
    for i in range(7)
]


# -=-=-ELEMENT_POSITION-=-=-
spaceshipX = 80
spaceshipY = 350
changeY = 0

asteroidX = 1100
asteroidY = random.randint(-20, 615)


# -=-=-GRUPOS-=-=-
lasers = []
explosoes= []


# -=-=-FUNÇÕES-=-=-
def player():
    tela.blit(spaceship, (spaceshipX, spaceshipY))

def asteroid():
    tela.blit(asteroidimg, (asteroidX, asteroidY))

def disparar_lasers():
    for laser in lasers:
        tela.blit(laserimg, (laser["x"], laser["y"]))


# -=-=-GAME-=-=-
while True:
    tela.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                changeY = -0.45
            if event.key == pygame.K_DOWN:
                changeY = 0.45
            if event.key == pygame.K_SPACE:
                lasers.append({
                    "x": spaceshipX + 76,
                    "y": spaceshipY + 36
                })
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                changeY = 0

    spaceshipY += changeY
    if spaceshipY <= -40:
        spaceshipY = -40
    if spaceshipY >= 615:
        spaceshipY = 615

    asteroidX += -0.15

    # LASER MOVIMENTO
    for laser in lasers:
        laser["x"] += 1.5

    # RETIRAR LASER AO SAIR DA TELA
    lasers = [laser for laser in lasers if laser["x"] < largura]

    # RECTS
    for laser in lasers[:]:
        laser_rect = pygame.Rect(laser["x"]+10, laser["y"], laserimg.get_width()*0.1, laserimg.get_height()*0.1)
        asteroid_rect = pygame.Rect(asteroidX, asteroidY, asteroidimg.get_width(), asteroidimg.get_height())

    # COLISÃO COM ASTEROID
    if laser_rect.colliderect(asteroid_rect):
        explosoes.append({
            "x": asteroidX,
            "y": asteroidY,
            "frame": 0,
            "contador": 0
        })
        lasers.remove(laser)
        asteroidX = 1000
        asteroidY = random.randint(-20, 615)
    elif laser["x"] > largura:
        lasers.remove(laser)
        
    for explosao in explosoes[:]:
        explosao["contador"] += 0.25
        if explosao["contador"] % 5 == 0:
            explosao["frame"] += 1
        if explosao["frame"] < len(explosion_images):
            img = explosion_images[explosao["frame"]]
            tela.blit(img, (explosao["x"], explosao["y"]))
        else:
            explosoes.remove(explosao)
    

    
    

    player()
    asteroid()
    disparar_lasers()

    pygame.display.update()
