import pygame
from pygame.locals import *
from sys import exit
import random
import time

pygame.init()
pygame.mixer.init()

# Evento personalizado para parar os sons dos lasers
LASER_STOP_EVENT = pygame.USEREVENT + 1

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

# Fonte
fonte = pygame.font.SysFont("Arial", 26, bold=True)
fonte_game_over = pygame.font.SysFont("Arial", 90, bold=True)
fonte_menu = pygame.font.SysFont("Arial", 50, bold=True)

# Ícone
pygame.display.set_icon(icon)

def exibir_menu():
    while True:
        tela.blit(background, (0, 0))
        titulo = fonte_menu.render("Star Wars: Contratos Galácticos", True, "yellow")
        iniciar = fonte.render("Pressione ESPAÇO para começar", True, "white")
        tela.blit(titulo, (120, 250))
        tela.blit(iniciar, (298, 350))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()
            if event.type == KEYDOWN and event.key == K_SPACE:
                return

def game_loop():
    spaceshipX = 80
    spaceshipY = 350
    changeY = 0
    score = 0
    colisao_ocorreu = False

    # Meteoros
    asteroids = []
    for _ in range(12):
        asteroids.append({
            "x": random.randint(1000, 1500),
            "y": random.randint(-20, 615)
        })

    lasers = []
    explosoes = []

    def disparar_lasers():
        lasers.append({
            "x": spaceshipX + 76,
            "y": spaceshipY + 36
        })

    def pontuacao():
        nonlocal piscar_ativo, tempo_inicio_piscar, ultimo_multiplo_piscado

        if score > 0 and score % 500 == 0 and score != ultimo_multiplo_piscado and not piscar_ativo:
            piscar_ativo = True
            tempo_inicio_piscar = pygame.time.get_ticks()
            ultimo_multiplo_piscado = score

        if piscar_ativo:
            achieve_sound=pygame.mixer.Sound("assets/sounds/achieve_sound1.wav")
            achieve_sound.set_volume(0.020)
            achieve_sound.play()
            
            
            tempo_atual = pygame.time.get_ticks()
            if tempo_atual - tempo_inicio_piscar <= 1500:
                tempo = tempo_atual // 150
                cor = "yellow" if tempo % 2 == 0 else "white"
                img_score = fonte.render(f'Score: {score}', True, cor)
            else:
                piscar_ativo = False
                img_score = fonte.render(f'Score: {score}', True, "white")
        else:
            img_score = fonte.render(f'Score: {score}', True, "white")

        tela.blit(img_score, (10, 10))

    def player():
        tela.blit(spaceship, (spaceshipX, spaceshipY))

    def game_over():
        img = fonte_game_over.render("Game Over", True, "white")
        tela.blit(img, (260, 305))
        pygame.mixer.music.stop()
        pygame.display.update()
        time.sleep(1)
        exibir_menu()
        game_loop()

    
    pygame.mixer.music.load("assets/sounds/Star Wars - Sound of Space Battles.mp3")
    pygame.mixer.music.set_volume(0.35)
    pygame.mixer.music.play(-1)

    explosion_sound = pygame.mixer.Sound("assets/sounds/Explosion Sound Effect.mp3")
    explosion_sound.set_volume(0.7)

    laser_sound = pygame.mixer.Sound("assets/sounds/Laser Sound.wav")
    laser_sound.set_volume(0.1)

    # Define 10 canais de áudio
    pygame.mixer.set_num_channels(16)

    # Canais para sons simultâneos
    laser_channels = [pygame.mixer.Channel(i) for i in range(10)]
    laser_channel_index = 0

    piscar_ativo = False
    tempo_inicio_piscar = None
    ultimo_multiplo_piscado = 0

    while True:
        tela.blit(background, (0, 0))

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()

            if event.type == KEYDOWN:
                if event.key == K_UP:
                    changeY = -0.6
                if event.key == K_DOWN:
                    changeY = 0.6
                if event.key == K_SPACE:
                    disparar_lasers()
                    canal = laser_channels[laser_channel_index]
                    canal.play(laser_sound)
                    pygame.time.set_timer(LASER_STOP_EVENT + laser_channel_index, 310)
                    laser_channel_index = (laser_channel_index + 1) % len(laser_channels)

            if event.type == KEYUP and event.key in (K_UP, K_DOWN):
                changeY = 0

            # Parar som do laser após 1.5 segundos
            if LASER_STOP_EVENT <= event.type < LASER_STOP_EVENT + len(laser_channels):
                canal_index = event.type - LASER_STOP_EVENT
                laser_channels[canal_index].stop()
                pygame.time.set_timer(event.type, 0)

        spaceshipY += changeY
        if spaceshipY < -40:
            spaceshipY = -40
        if spaceshipY > 615:
            spaceshipY = 615

        if not colisao_ocorreu:
            player_rect = pygame.Rect(spaceshipX, spaceshipY, spaceship.get_width() * 0.5, spaceship.get_height() * 0.3)

            for asteroid in asteroids:
                asteroid_rect = pygame.Rect(asteroid["x"], asteroid["y"], asteroidimg.get_width()*0.4, asteroidimg.get_height()*0.2)
                if player_rect.colliderect(asteroid_rect):
                    explosion_sound.play()
                    colisao_ocorreu = True

            for asteroid in asteroids:
                asteroid["x"] -= 0.4
                if asteroid["x"] < -100:
                    asteroid["x"] = random.randint(1000, 1500)
                    asteroid["y"] = random.randint(-20, 615)

            for laser in lasers[:]:
                laser["x"] += 1
                laser_rect = pygame.Rect(laser["x"] + 10, laser["y"] + 5, 20, 10)

                for asteroid in asteroids:
                    asteroid_rect = pygame.Rect(asteroid["x"], asteroid["y"], asteroidimg.get_width()*0.5, asteroidimg.get_height()*0.5)
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
                        score += 5

                if laser["x"] > 1200:
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
            for asteroid in asteroids:
                tela.blit(asteroidimg, (asteroid["x"], asteroid["y"]))
            for laser in lasers:
                tela.blit(laserimg, (laser["x"], laser["y"]))
            pontuacao()
            pygame.display.update()
        else:
            game_over()

# Execução
exibir_menu()
game_loop()
