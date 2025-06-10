import pygame
from pygame.locals import *
from sys import exit
import random

pygame.init()

altura = 700
largura = 1000
tela = pygame.display.set_mode((largura, altura))

icon = pygame.image.load("assets/icon/icone-star-wars-game.png")
background = pygame.image.load("assets/background/Starfields/Starfield_03-1024x1024.png")

spaceship = pygame.image.load("assets/spaceship/PNG_Parts&Spriter_Animation/Ship3/Ship3.png")
spaceshipX = 80
spaceshipY = 350
changeY = 0

laserimg = pygame.image.load("assets/spaceship/PNG_Animations/Shots/Shot3/shot3_asset.png")

asteroidimg = pygame.image.load("assets/asteroid/Asteroids/PNGs/Asteroid 01 - Base.png")
asteroidX = 1100
asteroidY = random.randint(-20, 615)

pygame.display.set_icon(icon)
pygame.display.set_caption("Star Wars: Contratos Galácticos")

# === Lista de lasers ativos ===
lasers = []

def player():
    tela.blit(spaceship, (spaceshipX, spaceshipY))

def asteroid():
    tela.blit(asteroidimg, (asteroidX, asteroidY))

def disparar_lasers():
    for laser in lasers:
        tela.blit(laserimg, (laser["x"], laser["y"]))

while True:
    tela.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                changeY = -0.5
            if event.key == pygame.K_DOWN:
                changeY = 0.5
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

    # Atualiza posição dos lasers
    for laser in lasers:
        laser["x"] += 1.5

    # RECTS
    for laser in lasers[:]:
        laser_rect = pygame.Rect(laser["x"]+10, laser["y"], laserimg.get_width()*0.1, laserimg.get_height()*0.1)
        asteroid_rect = pygame.Rect(asteroidX, asteroidY, asteroidimg.get_width(), asteroidimg.get_height())

        if laser_rect.colliderect(asteroid_rect):
            print("💥 Colisão detectada!")
            lasers.remove(laser)  # remove o laser da tela
        # Aqui você pode: resetar o asteroide, somar pontos, tocar som, etc.
            asteroidX = 1000
            asteroidY = random.randint(-20, 615)
            
    

    # Remove lasers que saíram da tela
    lasers = [laser for laser in lasers if laser["x"] < largura]

    player()
    asteroid()
    disparar_lasers()

    pygame.display.update()
