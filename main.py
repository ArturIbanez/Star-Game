import pygame
from pygame.locals import *
from sys import exit
import random
import time

pygame.init()
pygame.mixer.init()

# Evento personalizado para parar os sons dos lasers
LASER_STOP_EVENT = pygame.USEREVENT + 1

ENEMY_FIRE_EVENT = pygame.USEREVENT + 20

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
enemy_spaceship_img = pygame.image.load("assets/spaceship/PNG_Parts&Spriter_Animation/Ship1/Ship1.png")
enemy_spaceship_img = pygame.transform.flip(enemy_spaceship_img, True, False)

enemy_laser_img_original = pygame.image.load("assets/spaceship/PNG_Animations/Shots/Shot1/shot1_asset.png")
fator_largura_laser_enemy = 1.75 
fator_altura_laser_enemy = 1.2
nova_largura = int(enemy_laser_img_original.get_width() * fator_largura_laser_enemy)
nova_altura = int(enemy_laser_img_original.get_height() * fator_altura_laser_enemy)
enemy_laser_img = pygame.transform.scale(enemy_laser_img_original, (nova_largura, nova_altura))

# Carregar frames da explosão
asteroid_explosion_images = [
    pygame.image.load(f"assets/asteroid/Asteroids/PNGs/asteroid_explosion/explosion_{i}.png").convert_alpha()
    for i in range(7)
]

enemy_explosion_images = [
    pygame.image.load(f"assets/spaceship/PNG_Parts&Spriter_Animation/Explosions/Explosion1/Explosion1_{i}.png").convert_alpha()
    for i in range(11)
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
    
    
    def game_over():
            img_game_over = fonte_game_over.render("Game Over", True, "white")
            tela.blit(img_game_over, (260, 305))
            pygame.mixer.music.stop()
            pygame.display.update()
            pygame.time.delay(2000)
            exibir_menu()
            game_loop()

    # Meteoros
    asteroids = []
    for _ in range(10):
        asteroids.append({
            "x": random.randint(1000, 1500),
            "y": random.randint(-20, 615)
        })

    # Naves inimigas
    enemies_spaceship = []
    for _ in range(3):
        enemies_spaceship.append({
            "x": random.randint(1000, 1500),
            "y": random.randint(-20, 615)
        })

    lasers = []
    explosoes_asteroid = []
    explosoes_enemy = []
    enemy_lasers = []

    def disparar_lasers():
        lasers.append({
            "x": spaceshipX + 76,
            "y": spaceshipY + 36
        })

    piscar_ativo = False
    tempo_inicio_piscar = None
    ultimo_multiplo_piscado = 0
    
    def pontuacao():
        nonlocal piscar_ativo, tempo_inicio_piscar, ultimo_multiplo_piscado

        if score > 0 and score % 500 == 0 and score != ultimo_multiplo_piscado and not piscar_ativo:
            piscar_ativo = True
            tempo_inicio_piscar = pygame.time.get_ticks()
            ultimo_multiplo_piscado = score

        if piscar_ativo:
            achieve_sound = pygame.mixer.Sound("assets/sounds/achieve_sound1.wav")
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

    # --- Sons ---
    pygame.mixer.music.load("assets/sounds/Star Wars - Sound of Space Battles.mp3")
    pygame.mixer.music.set_volume(0.35)
    pygame.mixer.music.play(-1)

    explosion_sound = pygame.mixer.Sound("assets/sounds/Explosion Sound Effect.mp3")
    explosion_sound.set_volume(0.7)

    laser_sound = pygame.mixer.Sound("assets/sounds/Laser Sound.wav")
    laser_sound.set_volume(0.1)

    pygame.mixer.set_num_channels(16)
    laser_channels = [pygame.mixer.Channel(i) for i in range(10)]
    laser_channel_index = 0

    pygame.time.set_timer(ENEMY_FIRE_EVENT, 3500)
    

    # --- Loop Principal do Jogo ---
    fps= pygame.time.Clock()
    while True:
        tela.blit(background, (0, 0))

        
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()

            if event.type == ENEMY_FIRE_EVENT:
                for enemy in enemies_spaceship:
                    # O laser sai da frente da nave inimiga (que está à esquerda, pois a imagem foi invertida)
                    pos_x = enemy["x"]-40
                    pos_y = enemy["y"] + (enemy_spaceship_img.get_height() / 2) - 18.5 # Ajuste para sair do meio
                    enemy_lasers.append({"x": pos_x, "y": pos_y})

            if event.type == KEYDOWN:
                if event.key == K_UP:
                    changeY = -8
                if event.key == K_DOWN:
                    changeY = 8
                if event.key == K_SPACE:
                    disparar_lasers()
                    canal = laser_channels[laser_channel_index]
                    canal.play(laser_sound)
                    pygame.time.set_timer(LASER_STOP_EVENT + laser_channel_index, 310)
                    laser_channel_index = (laser_channel_index + 1) % len(laser_channels)

            if event.type == KEYUP and event.key in (K_UP, K_DOWN):
                changeY = 0

            if LASER_STOP_EVENT <= event.type < LASER_STOP_EVENT + len(laser_channels):
                canal_index = event.type - LASER_STOP_EVENT
                laser_channels[canal_index].stop()
                pygame.time.set_timer(event.type, 0)

        spaceshipY += changeY
        if spaceshipY < -40:
            spaceshipY = -40
        if spaceshipY > 615:
            spaceshipY = 615
        
        # --- Lógica e Renderização ---

        player_rect = pygame.Rect(spaceshipX, spaceshipY, spaceship.get_width()*0.68, spaceship.get_height())
        padding_cima= 45
        padding_baixo= 45
        padding_esquerdo= 20
        player_rect.left+=padding_esquerdo
        player_rect.height -= padding_baixo
        player_rect.top += padding_cima
        player_rect.height -= padding_cima
        pygame.draw.rect(tela, "green", player_rect, 2)
        
        # Asteroide: Movimento, Colisão com Jogador e Renderização
        for asteroid in asteroids:
            asteroid["x"] -= 3
            tela.blit(asteroidimg, (asteroid["x"], asteroid["y"]))
            if asteroid["x"] < -100:
                asteroid["x"] = random.randint(1000, 1500)
                asteroid["y"] = random.randint(-20, 615)
            
            asteroid_rect = pygame.Rect(asteroid["x"], asteroid["y"], asteroidimg.get_width()*0.4, asteroidimg.get_height())
            padding_cima= 33
            padding_baixo= 32
            padding_esquerdo= 27
            asteroid_rect.top += padding_cima
            asteroid_rect.height -= padding_cima
            asteroid_rect.height -= padding_baixo
            asteroid_rect.left+=padding_esquerdo
            pygame.draw.rect(tela, "blue", asteroid_rect, 2)

            if player_rect.colliderect(asteroid_rect):
                explosion_sound.play()
                # LÓGICA DE GAME OVER APLICADA DIRETAMENTE AQUI
                game_over()
                return

        # Inimigos: Movimento, Colisão com Jogador e Renderização
        
        for enemy in enemies_spaceship:
            enemy["x"] -= 1.5
            tela.blit(enemy_spaceship_img, (enemy["x"], enemy["y"]))
            if enemy["x"] < -100:
                enemy["x"] = random.randint(1000, 1500)
                enemy["y"] = random.randint(-20, 615)

            enemy_rect = pygame.Rect(enemy["x"], enemy["y"], enemy_spaceship_img.get_width(), enemy_spaceship_img.get_height()*0.7)
            padding_cima= 16
            enemy_rect.top += padding_cima
            enemy_rect.height -= padding_cima
            pygame.draw.rect(tela, "yellow", enemy_rect, 2)

            if player_rect.colliderect(enemy_rect):
                explosion_sound.play()
                # LÓGICA DE GAME OVER APLICADA DIRETAMENTE AQUI
                game_over()
                return

        for enemy_laser in enemy_lasers[:]:
            enemy_laser["x"] -= 5  # Move da direita para a esquerda
            tela.blit(enemy_laser_img, (enemy_laser["x"], enemy_laser["y"]))

            # Remove o laser se ele sair da tela
            if enemy_laser["x"] < -laserimg.get_width():
                enemy_lasers.remove(enemy_laser)
                continue

            # Verifica colisão com o jogador
            enemy_laser_rect = pygame.Rect(enemy_laser["x"], enemy_laser["y"], enemy_laser_img.get_width()*0.44, enemy_laser_img.get_height())
            padding_cima= 16
            padding_baixo= 15
            padding_esquerdo= 20
            enemy_laser_rect.top += padding_cima
            enemy_laser_rect.height -= padding_cima
            enemy_laser_rect.height -= padding_baixo
            enemy_laser_rect.left+=padding_esquerdo
            pygame.draw.rect(tela, "orange", enemy_laser_rect, 2)
            if player_rect.colliderect(enemy_laser_rect):
                enemy_lasers.remove(enemy_laser) # Remove o laser para não causar múltiplos game overs
                explosion_sound.play()

        # Lasers: Movimento, Colisão com Asteroides e Renderização
        for laser in lasers[:]:
            laser["x"] += 7
            tela.blit(laserimg, (laser["x"], laser["y"]))
            if laser["x"] > 1200:
                lasers.remove(laser)
                continue # Pula para o próximo laser do loop
            
            laser_rect = pygame.Rect(laser["x"], laser["y"], laserimg.get_width()*0.35, laserimg.get_height())
            padding_cima= 26
            padding_baixo= 23
            padding_esquerdo= 30
            laser_rect.top += padding_cima
            laser_rect.height -= padding_cima
            laser_rect.height -= padding_baixo
            laser_rect.left+=padding_esquerdo
            pygame.draw.rect(tela, "red", laser_rect, 2)
            for asteroid in asteroids:
                asteroid_rect = pygame.Rect(asteroid["x"], asteroid["y"], asteroidimg.get_width()*0.4, asteroidimg.get_height())
                padding_cima= 33
                padding_baixo= 32
                padding_esquerdo= 27
                asteroid_rect.top += padding_cima
                asteroid_rect.height -= padding_cima
                asteroid_rect.height -= padding_baixo
                asteroid_rect.left+=padding_esquerdo
                pygame.draw.rect(tela, "blue", asteroid_rect, 2)
                if laser_rect.colliderect(asteroid_rect):
                    explosoes_asteroid.append({"x": asteroid["x"], "y": asteroid["y"], "frame": 0, "contador": 0})
                    lasers.remove(laser)
                    asteroid["x"] = random.randint(1000, 1500)
                    asteroid["y"] = random.randint(-20, 615)
                    score += 5
                    break # Interrompe o loop de asteroides, já que o laser foi removido

            for enemy in enemies_spaceship:
                enemy_rect = pygame.Rect(enemy["x"], enemy["y"], enemy_spaceship_img.get_width(), enemy_spaceship_img.get_height()*0.7)
                padding_cima= 16
                enemy_rect.top += padding_cima
                enemy_rect.height -= padding_cima
                if laser_rect.colliderect(enemy_rect):
                    explosoes_enemy.append({"x": enemy["x"], "y": enemy["y"], "frame": 0, "contador": 0})
                    lasers.remove(laser)
                    enemy["x"] = random.randint(1000, 1500)
                    enemy["y"] = random.randint(-20, 615)
                    score += 10
                    break # Interrompe o loop de asteroides, já que o laser foi removido

        # Explosões
        for explosao_asteroid in explosoes_asteroid[:]:
            explosao_asteroid["contador"] += 2.5
            if explosao_asteroid["contador"] % 5 == 0:
                explosao_asteroid["frame"] += 1
            if explosao_asteroid["frame"] < len(asteroid_explosion_images):
                img = asteroid_explosion_images[explosao_asteroid["frame"]]
                tela.blit(img, (explosao_asteroid["x"], explosao_asteroid["y"]))
            else:
                explosoes_asteroid.remove(explosao_asteroid)

        for explosao_enemy in explosoes_enemy:
            explosao_enemy["contador"] += 2.5
            if explosao_enemy["contador"] % 5 == 0:
                explosao_enemy["frame"] += 1
            if explosao_enemy["frame"] < len(enemy_explosion_images):
                img = enemy_explosion_images[explosao_enemy["frame"]]
                tela.blit(img, (explosao_enemy["x"]-40, explosao_enemy["y"]-34))
            else:  
                explosoes_enemy.remove(explosao_enemy)

        player()
        pontuacao()
        pygame.display.update()
        fps.tick(60)
# Execução
while True:
    exibir_menu()
    game_loop()