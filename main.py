import pygame
from pygame.locals import *
from sys import exit
import random
import time
import tkinter as tk
from tkinter import ttk
from tkinter import font as tkFont
from recursos.funcoes import inicializarBancoDeDados
import json
from datetime import datetime
import speech_recognition as sr
import pyttsx3

pygame.init()
pygame.mixer.init()

LASER_STOP_EVENT = pygame.USEREVENT + 1

ENEMY_FIRE_EVENT = pygame.USEREVENT + 20

altura = 700
largura = 1000
tela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption("Star Game")

icon = pygame.image.load("assets/icon/icone-star-wars-game.png")
background = pygame.image.load("assets/background/Starfields/Starfield_03-1024x1024.png")
spaceship = pygame.image.load("assets/spaceship/PNG_Parts&Spriter_Animation/Ship3/Ship3.png")
laserimg = pygame.image.load("assets/spaceship/PNG_Animations/Shots/Shot3/shot3_asset.png")
asteroidimg = pygame.image.load("assets/asteroid/Asteroids/PNGs/Asteroid 01 - Base.png")
enemy_spaceship_img = pygame.image.load("assets/spaceship/PNG_Parts&Spriter_Animation/Ship1/Ship1.png")
enemy_spaceship_img = pygame.transform.flip(enemy_spaceship_img, True, False)

final_enemy_spaceship_img = pygame.image.load("assets/spaceship/PNG_Parts&Spriter_Animation/Ship6/Ship6.png")
final_enemy_spaceship_img = pygame.transform.flip(final_enemy_spaceship_img, True, False)
final_enemy_laser_img = pygame.image.load("assets/spaceship/PNG_Animations/Shots/Shot6/shot6_1.png")
final_enemy_laser_img = pygame.transform.flip(final_enemy_laser_img, True, False)

enemy_laser_img_original = pygame.image.load("assets/spaceship/PNG_Animations/Shots/Shot1/shot1_asset.png")
fator_largura_laser_enemy = 1.75
fator_altura_laser_enemy = 1.2
nova_largura = int(enemy_laser_img_original.get_width() * fator_largura_laser_enemy)
nova_altura = int(enemy_laser_img_original.get_height() * fator_altura_laser_enemy)
enemy_laser_img = pygame.transform.scale(enemy_laser_img_original, (nova_largura, nova_altura))

planet_element_images = [
    pygame.image.load(f"assets/planet/planet_{i}.png").convert_alpha()
    for i in range(100)
]
asteroid_explosion_images = [
    pygame.image.load(f"assets/asteroid/Asteroids/PNGs/asteroid_explosion/explosion_{i}.png").convert_alpha()
    for i in range(7)
]

enemy_explosion_images = [
    pygame.image.load(f"assets/spaceship/PNG_Parts&Spriter_Animation/Explosions/Explosion1/Explosion1_{i}.png").convert_alpha()
    for i in range(11)
]

fonte = pygame.font.SysFont("Arial", 26, bold=True)
fonte_game_over = pygame.font.SysFont("Arial", 90, bold=True)
fonte_menu = pygame.font.SysFont("Arial", 50, bold=True)

pygame.display.set_icon(icon)

def jogar():
    global nome
    
    root = tk.Tk()
    root.title("Informe seu nome")
    
    largura_janela = 400
    altura_janela = 150
    largura_tela = root.winfo_screenwidth()
    altura_tela = root.winfo_screenheight()
    pos_x = (largura_tela - largura_janela) // 2
    pos_y = (altura_tela - altura_janela) // 2
    root.geometry(f"{largura_janela}x{altura_janela}+{pos_x}+{pos_y}")
    root.configure(bg='black')

    cor_texto = "yellow"
    cor_fundo_botao = "white"
    fonte_instrucao = tkFont.Font(family="Arial", size=12)
    fonte_botao = tkFont.Font(family="Arial", size=12, weight="bold")

    label_instrucao = tk.Label(
        root,
        text="Clique no botão e diga seu nome",
        fg=cor_texto,
        bg="black",
        font=fonte_instrucao
    )
    label_instrucao.pack(pady=20)

    def ouvir_e_reconhecer_nome():
        global nome

        r = sr.Recognizer()
        with sr.Microphone() as source:
            label_instrucao.config(text="Ajustando ruído ambiente...")
            root.update()
            r.adjust_for_ambient_noise(source)
            
            label_instrucao.config(text="Ouvindo...")
            root.update()
            
            try:
                audio = r.listen(source, timeout=5, phrase_time_limit=5)
                label_instrucao.config(text="Reconhecendo...")
                root.update()
                
                recognized_text = r.recognize_google(audio, language='pt-BR')
                
                nome = recognized_text.capitalize()
                
                label_instrucao.config(text=f"Bem vindo: Piloto {nome}")
                root.update()
                time.sleep(3)
                root.destroy()

            except sr.WaitTimeoutError:
                label_instrucao.config(text="Tempo esgotado. Tente novamente.")
            except sr.UnknownValueError:
                label_instrucao.config(text="Não foi possível entender o áudio. Tente novamente.")
            except sr.RequestError as e:
                label_instrucao.config(text=f"Erro de serviço. Verifique a conexão.\n {e}")
            
    botao = tk.Button(
        root,
        text="🎤  Falar",
        command=ouvir_e_reconhecer_nome,
        font=fonte_botao,
        bg=cor_fundo_botao,
        fg="black"
    )
    botao.pack(pady=10)

    root.mainloop()


def tela_boas_vindas():
    largura_janela = 600
    altura_janela = 400

    root = tk.Tk()
    root.configure(bg='black')

    cor_texto = "yellow"
    cor_fundo = "black"
    fonte_titulo = tkFont.Font(family="Arial", size=16, weight="bold")
    fonte_corpo = tkFont.Font(family="Arial", size=12)
    fonte_destaque = tkFont.Font(family="Arial", size=13, weight="bold")

    label_titulo = tk.Label(
        root,
        text=f"Boas vindas",
        fg=cor_texto,
        bg=cor_fundo,
        font=fonte_titulo
    )
    label_titulo.pack(pady=(20, 10))

    label_missao = tk.Label(
        root,
        text="Sua missão é sobreviver o máximo possível nos campos de asteroides\ne eliminar os contratos hostis.",
        fg=cor_texto,
        bg=cor_fundo,
        font=fonte_corpo
    )
    label_missao.pack(pady=10)

    label_mecanica_titulo = tk.Label(
        root,
        text="MECÂNICA DO JOGO:",
        fg=cor_texto,
        bg=cor_fundo,
        font=fonte_destaque
    )
    label_mecanica_titulo.pack(pady=(20, 5))

    texto_mecanicas = (
        "• Use as SETAS (CIMA e BAIXO) para mover sua nave.\n\n"
        "• Pressione a tecla ESPAÇO para atirar lasers.\n\n"
        "• Cuidado! Os inimigos também atiram."
    )
    label_mecanicas = tk.Label(
        root,
        text=texto_mecanicas,
        fg=cor_texto,
        bg=cor_fundo,
        font=fonte_corpo,
        justify=tk.LEFT
    )
    label_mecanicas.pack(pady=5)

    label_sorte = tk.Label(
        root,
        text="Boa sorte, em sua jornada!.",
        fg=cor_texto,
        bg=cor_fundo,
        font=fonte_corpo
    )
    label_sorte.pack(pady=(20, 30))

    largura_tela = root.winfo_screenwidth()
    altura_tela = root.winfo_screenheight()
    pos_x = (largura_tela - largura_janela) // 2
    pos_y = (altura_tela - altura_janela) // 2
    root.geometry(f"{largura_janela}x{altura_janela}+{pos_x}+{pos_y}")
    

    botao = tk.Button(
        root,
        text="Iniciar Jogo",
        command=root.destroy,
        fg="black",
        bg="white",
        font=fonte_destaque,
        activeforeground="black",
        activebackground="yellow"
    )
    botao.pack()

    root.mainloop()

def exibir_menu():
    while True:
        tela.blit(background, (0, 0))
        titulo = fonte_menu.render("Star Game: Uma Aventura Galáctica", True, "yellow")
        iniciar = fonte.render("Pressione ESPAÇO para começar", True, "white")
        tela.blit(titulo, (75, 250))
        tela.blit(iniciar, (298, 350))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()
            if event.type == KEYDOWN and event.key == K_SPACE:
                jogar()
                tela_boas_vindas()
                return


def game_loop():
    spaceshipX = 80
    spaceshipY = 350
    changeY = 0
    score = 0
    velocidade_base_asteroide = 3.0
    incremento_por_500_pontos = 0.25
    velocidade_base_laser_inimigo = 7.0
    incremento_velocidade_laser = 0.05
    planet_frame = 0
    planet_contador = 0
    
    pausado = False

    def escreverDados():
        dadosDict = {}
        try:
            with open("log.dat", "r") as banco:
                dados = banco.read()
                if dados:
                    dadosDict = json.loads(dados)
        except (FileNotFoundError, json.JSONDecodeError):
            dadosDict = {}
            
        data_br = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        nova_pontuacao = (score, data_br)
        
        if nome in dadosDict:
            dadosDict[nome].append(nova_pontuacao)
        else:
            dadosDict[nome] = [nova_pontuacao]
        
        with open("log.dat", "w") as banco:
            banco.write(json.dumps(dadosDict, indent=4)) 

    def game_over():
        try:
            engine = pyttsx3.init()
            voices = engine.getProperty('voices')
            for voice in voices:
                if "brazil" in voice.name.lower() or "portuguese" in voice.name.lower():
                    engine.setProperty('voice', voice.id)
                    break
            
            engine.setProperty('rate', 160)
            
            mensagem = "Game Over"
            engine.say(mensagem)
            engine.runAndWait()
            engine.stop()
        except Exception as e:
            return
        
        todos_os_registros = []
        try:
            with open("log.dat", "r") as banco:
                dados_log = json.load(banco)
            
            for nome_jogador, lista_partidas in dados_log.items():
                for partida in lista_partidas:
                    score_partida, data_partida = partida
                    todos_os_registros.append((nome_jogador, score_partida, data_partida))
            
            formato_data = "%d/%m/%Y %H:%M:%S"
            todos_os_registros.sort(key=lambda registro: datetime.strptime(registro[2], formato_data), reverse=True)

        except (FileNotFoundError, json.JSONDecodeError):
            pass

        ultimos_cinco = todos_os_registros[:5]

        titulo_fim_de_jogo = fonte_game_over.render("GAME OVER", True, "red")
        score_texto_atual = fonte.render(f"Sua pontuação nesta partida: {score}", True, "white")
        titulo_log = fonte_menu.render("Últimas Partidas", True, "yellow")
        
        iniciar = fonte.render("Pressione ESPAÇO para jogar novamente", True, "green")
        saindo = fonte.render("Pressione ESC para sair", True, "white")

        waiting = True
        while waiting:
            tela.blit(background, (0, 0))

            tela.blit(titulo_fim_de_jogo, (titulo_fim_de_jogo.get_rect(center=(largura / 2, 80))))
            tela.blit(score_texto_atual, (score_texto_atual.get_rect(center=(largura / 2, 140))))
            tela.blit(titulo_log, (titulo_log.get_rect(center=(largura / 2, 220))))

            pos_y_instrucoes = 0
            if not ultimos_cinco:
                    # Lógica para quando não há scores
                texto_sem_log = fonte.render("Nenhum registro de partida encontrado.", True, "gray")
                tela.blit(texto_sem_log, (texto_sem_log.get_rect(center=(largura / 2, 300))))
                # Define a posição das instruções com base no texto acima
                pos_y_instrucoes = 300 + 80
            else:
                # Lógica para quando HÁ scores
                pos_y_inicial = 280
                formato_data = "%d/%m/%Y %H:%M:%S"
                
                for i, registro in enumerate(ultimos_cinco):
                    nome_log, score_log, data_log = registro
                    data_display = datetime.strptime(data_log, formato_data).strftime("%d/%m/%y %H:%M:%S")
                    
                    texto_linha = f"{i+1}. {nome_log}: {score_log} pontos ({data_display})"
                    linha_renderizada = fonte.render(texto_linha, True, "white")
                    
                    pos_y = pos_y_inicial + (i * 40)
                    tela.blit(linha_renderizada, (linha_renderizada.get_rect(center=(largura / 2, pos_y))))

                # Define a posição das instruções com base na lista de scores
                pos_y_instrucoes = pos_y_inicial + (len(ultimos_cinco) * 40) + 60
            
            # Agora que 'pos_y_instrucoes' tem um valor garantido, desenhamos os botões
            tela.blit(iniciar, (iniciar.get_rect(center=(largura / 2, pos_y_instrucoes))))
            tela.blit(saindo, (saindo.get_rect(center=(largura / 2, pos_y_instrucoes + 50))))

            pygame.display.update()

            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    exit()
                if event.type == KEYDOWN:
                    if event.key == K_SPACE:
                        waiting = False
                    elif event.key == K_ESCAPE:
                        pygame.quit()
                        exit()

    def get_pontos_por_destruicao(score_atual):
        if score_atual >= 2000:
            return 100
        elif score_atual >= 1000:
            return 50
        elif score_atual >= 500:
            return 25
        else:
            return 10 # Pontuação base

    asteroids = []
    for _ in range(5):
        asteroids.append({
            "x": random.randint(1000, 1500),
            "y": random.randint(-20, 615)
        })

    enemies_spaceship = []
    for _ in range(4):
        enemies_spaceship.append({
            "x": random.randint(1000, 1500),
            "y": random.randint(-20, 615),
            "vida": 2
        })

    final_enemies_spaceship = []
    for _ in range (3):
        final_enemies_spaceship.append({
            "x": random.randint(1000, 1500),
            "y": random.randint(-20, 615),
            "vida": 3
        })

    lasers = []
    explosoes_asteroid = []
    explosoes_enemy = []
    enemy_lasers = []
    final_enemy_lasers = []

    def disparar_lasers():
        lasers.append({
            "x": spaceshipX + 76,
            "y": spaceshipY + 36
        })

    piscar_ativo = False
    tempo_inicio_piscar = None
    ultimo_multiplo_piscado = 0
    
    achieve_sound = pygame.mixer.Sound("assets/sounds/achieve_sound1.wav")
    achieve_sound.set_volume(0.05)
    
    def pontuacao():
        nonlocal piscar_ativo, tempo_inicio_piscar, ultimo_multiplo_piscado

        if score > 0 and score % 1000 == 0 and score != ultimo_multiplo_piscado and not piscar_ativo:
            piscar_ativo = True
            tempo_inicio_piscar = pygame.time.get_ticks()
            ultimo_multiplo_piscado = score

        if piscar_ativo:
            achieve_sound.play()
            
            tempo_atual = pygame.time.get_ticks()
            if tempo_atual - tempo_inicio_piscar <= 1500:
                tempo = tempo_atual // 150
                cor = "yellow" if tempo % 2 == 0 else "white"
                img_score = fonte.render(f'Score: {score} | Press ESC to Pause Game', True, cor)
            else:
                piscar_ativo = False
                img_score = fonte.render(f'Score: {score} | Press ESC to Pause Game', True, "white")
        else:
            img_score = fonte.render(f'Score: {score} | Press ESC to Pause Game', True, "white")

        tela.blit(img_score, (10, 10))

    def player():
        tela.blit(spaceship, (spaceshipX, spaceshipY))

    pygame.mixer.music.load("assets/sounds/Star Wars - Sound of Space Battles.mp3")
    pygame.mixer.music.set_volume(0.20)
    pygame.mixer.music.play(-1)

    explosion_sound = pygame.mixer.Sound("assets/sounds/Explosion Sound Effect.mp3")
    explosion_sound.set_volume(0.7)

    laser_sound = pygame.mixer.Sound("assets/sounds/Laser Sound.wav")
    laser_sound.set_volume(0.1)

    pygame.mixer.set_num_channels(16)
    laser_channels = [pygame.mixer.Channel(i) for i in range(10)]
    laser_channel_index = 0

    pygame.time.set_timer(ENEMY_FIRE_EVENT, 3500)
    
    fps= pygame.time.Clock()
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()
            
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pausado = not pausado
                    if pausado:
                        pygame.mixer.music.pause()
                    else:
                        pygame.mixer.music.unpause()

            if not pausado:
                if event.type == ENEMY_FIRE_EVENT:
                    for enemy in enemies_spaceship:
                        pos_x = enemy["x"]-40
                        pos_y = enemy["y"] + (enemy_spaceship_img.get_height() / 2) - 18.5
                        enemy_lasers.append({"x": pos_x, "y": pos_y})

                    for final_enemy in final_enemies_spaceship:
                        pos_x = final_enemy["x"] - 20
                        pos_y = final_enemy["y"] + (final_enemy_spaceship_img.get_height() / 2) - (final_enemy_laser_img.get_height() / 2)
                        final_enemy_lasers.append({"x": pos_x, "y": pos_y})

                if event.type == KEYDOWN:
                    if event.key == K_UP:
                        changeY = -6.25
                    if event.key == K_DOWN:
                        changeY = 6.25
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

        if not pausado:
            spaceshipY += changeY
            if spaceshipY < -40:
                spaceshipY = -40
            if spaceshipY > 615:
                spaceshipY = 615
            
            player_rect = pygame.Rect(spaceshipX, spaceshipY, spaceship.get_width() * 0.68, spaceship.get_height())
            padding_cima, padding_baixo, padding_esquerdo = 45, 45, 20
            player_rect.left += padding_esquerdo
            player_rect.height -= (padding_baixo + padding_cima)
            player_rect.top += padding_cima
            
            niveis_de_pontos = score // 500
            velocidade_asteroide = velocidade_base_asteroide + (niveis_de_pontos * incremento_por_500_pontos)

            velocidade_laser_inimigo = velocidade_base_laser_inimigo + (niveis_de_pontos * incremento_velocidade_laser)

            for asteroid in asteroids:
                asteroid["x"] -= velocidade_asteroide
                
                if asteroid["x"] < -100:
                    asteroid["x"] = random.randint(1000, 1500)
                    asteroid["y"] = random.randint(-40, 615)
                
                asteroid_rect = pygame.Rect(asteroid["x"], asteroid["y"], asteroidimg.get_width() * 0.4, asteroidimg.get_height())
                padding_cima_ast, padding_baixo_ast, padding_esquerdo_ast = 33, 32, 27
                asteroid_rect.top += padding_cima_ast
                asteroid_rect.height -= (padding_cima_ast + padding_baixo_ast)
                asteroid_rect.left += padding_esquerdo_ast

                if player_rect.colliderect(asteroid_rect):
                    explosion_sound.play()
                    escreverDados()
                    game_over()
                    return

            if score >= 200:
                for i in range(len(enemies_spaceship)):
                    enemy = enemies_spaceship[i]
                    enemy["x"] -= 1.5

                    if enemy["x"] < -100:
                        enemies_spaceship[i]["x"] = random.randint(1000, 1500)
                        enemies_spaceship[i]["y"] = random.randint(-40, 615)
                    
                    enemy_rect = pygame.Rect(enemy["x"], enemy["y"], enemy_spaceship_img.get_width(), enemy_spaceship_img.get_height() * 0.7)
                    padding_cima_enemy = 16
                    enemy_rect.top += padding_cima_enemy
                    enemy_rect.height -= padding_cima_enemy
                    if player_rect.colliderect(enemy_rect):
                        explosion_sound.play()
                        escreverDados()
                        game_over()
                        return

                for enemy_laser in enemy_lasers[:]:
                    enemy_laser["x"] -= velocidade_laser_inimigo
                    
                    if enemy_laser["x"] < -enemy_laser_img.get_width():
                        enemy_lasers.remove(enemy_laser)
                        continue

                    enemy_laser_rect = pygame.Rect(enemy_laser["x"], enemy_laser["y"], enemy_laser_img.get_width()*0.44, enemy_laser_img.get_height())
                    padding_cima_laser, padding_baixo_laser, padding_esq_laser = 16, 15, 20
                    enemy_laser_rect.top += padding_cima_laser
                    enemy_laser_rect.height -= (padding_cima_laser + padding_baixo_laser)
                    enemy_laser_rect.left += padding_esq_laser
                    if player_rect.colliderect(enemy_laser_rect):
                        enemy_lasers.remove(enemy_laser)
                        explosion_sound.play()
                        escreverDados()
                        game_over()
                        return
            
            if score >= 500:
                for final_enemy in final_enemies_spaceship:
                    final_enemy["x"] -= 1.5

                    if final_enemy["x"] < -100:
                        final_enemy["x"] = random.randint(1000, 1500)
                        final_enemy["y"] = random.randint(-40, 615)
                    
                    final_enemy_rect = pygame.Rect(final_enemy["x"], final_enemy["y"], final_enemy_spaceship_img.get_width()*0.85, final_enemy_spaceship_img.get_height() * 0.7)
                    padding_cima_final_enemy = 35
                    padding_esquerdo_final_enemy= 10
                    final_enemy_rect.left += padding_esquerdo_final_enemy
                    final_enemy_rect.top += padding_cima_final_enemy
                    final_enemy_rect.height -= padding_cima_final_enemy
                    if player_rect.colliderect(final_enemy_rect):
                        explosion_sound.play()
                        escreverDados()
                        game_over()
                        return

                for final_enemy_laser in final_enemy_lasers[:]:
                    final_enemy_laser["x"] -= velocidade_laser_inimigo

                    if final_enemy_laser["x"] < -final_enemy_laser_img.get_width():
                        final_enemy_lasers.remove(final_enemy_laser)
                        continue

                    final_enemy_laser_rect = pygame.Rect(final_enemy_laser["x"], final_enemy_laser["y"], final_enemy_laser_img.get_width()*0.4, final_enemy_laser_img.get_height())
                    padding_cima_laser, padding_baixo_laser, padding_esq_laser = 59, 62, 65
                    final_enemy_laser_rect.top += padding_cima_laser
                    final_enemy_laser_rect.height -= (padding_cima_laser + padding_baixo_laser)
                    final_enemy_laser_rect.left += padding_esq_laser
                    if player_rect.colliderect(final_enemy_laser_rect):
                        final_enemy_lasers.remove(final_enemy_laser)
                        explosion_sound.play()
                        escreverDados()
                        game_over()
                        return

            for laser in lasers[:]:
                laser["x"] += 7
                if laser["x"] > 1200:
                    lasers.remove(laser)
                    continue

                laser_rect = pygame.Rect(laser["x"], laser["y"], laserimg.get_width() * 0.35, laserimg.get_height())
                padding_cima = 26
                padding_baixo = 23
                padding_esquerdo = 30
                laser_rect.top += padding_cima
                laser_rect.height -= (padding_cima + padding_baixo)
                laser_rect.left += padding_esquerdo

                laser_colidiu = False

                for asteroid in asteroids:
                    asteroid_rect = pygame.Rect(asteroid["x"], asteroid["y"], asteroidimg.get_width() * 0.4, asteroidimg.get_height())
                    padding_cima_ast = 33
                    padding_baixo_ast = 32
                    padding_esquerdo_ast = 27
                    asteroid_rect.top += padding_cima_ast
                    asteroid_rect.height -= (padding_cima_ast + padding_baixo_ast)
                    asteroid_rect.left += padding_esquerdo_ast
                    
                    if laser_rect.colliderect(asteroid_rect):
                        explosoes_asteroid.append({"x": asteroid["x"], "y": asteroid["y"], "frame": 0, "contador": 0})
                        asteroid["x"] = random.randint(1000, 1500)
                        asteroid["y"] = random.randint(-20, 615)
                        score += get_pontos_por_destruicao(score)
                        laser_colidiu = True
                        break

                if not laser_colidiu:
                    for enemy in enemies_spaceship:
                        enemy_rect = pygame.Rect(enemy["x"], enemy["y"], enemy_spaceship_img.get_width(), enemy_spaceship_img.get_height() * 0.7)
                        padding_cima_en = 16
                        enemy_rect.top += padding_cima_en
                        enemy_rect.height -= padding_cima_en
                        if laser_rect.colliderect(enemy_rect):
                            explosoes_enemy.append({"x": enemy["x"], "y": enemy["y"], "frame": 0, "contador": 0})
                            laser_colidiu = True
                            enemy["vida"] -= 1
                            if enemy["vida"] <= 0:
                                explosoes_enemy.append({"x": enemy["x"], "y": enemy["y"], "frame": 0, "contador": 0})
                                enemy["x"] = random.randint(1000, 1500)
                                enemy["y"] = random.randint(-20, 615)
                                enemy["vida"] = 2
                                score += get_pontos_por_destruicao(score)
                            break

                if not laser_colidiu:
                    for final_enemy in final_enemies_spaceship:
                        final_enemy_rect = pygame.Rect(final_enemy["x"], final_enemy["y"], final_enemy_spaceship_img.get_width(), final_enemy_spaceship_img.get_height() * 0.7)
                        padding_cima_final = 16
                        final_enemy_rect.top += padding_cima_final
                        final_enemy_rect.height -= padding_cima_final

                        if laser_rect.colliderect(final_enemy_rect):
                            explosoes_enemy.append({"x": final_enemy["x"]+20, "y": final_enemy["y"]+30, "frame": 0, "contador": 0})
                            laser_colidiu = True
                            final_enemy["vida"] -= 1
                            if final_enemy["vida"] <= 0:
                                explosoes_enemy.append({"x": final_enemy["x"]+20, "y": final_enemy["y"]+30, "frame": 0, "contador": 0})
                                final_enemy["x"] = random.randint(1000, 1500)
                                final_enemy["y"] = random.randint(-20, 615)
                                final_enemy["vida"] = 3
                                score += get_pontos_por_destruicao(score)
                            break
                
                if laser_colidiu:
                    lasers.remove(laser)

            for explosao_asteroid in explosoes_asteroid[:]:
                explosao_asteroid["contador"] += 2.5
                if explosao_asteroid["contador"] % 5 == 0:
                    explosao_asteroid["frame"] += 1
                if explosao_asteroid["frame"] >= len(asteroid_explosion_images):
                    explosoes_asteroid.remove(explosao_asteroid)

            for explosao_enemy in explosoes_enemy[:]:
                explosao_enemy["contador"] += 2.5
                if explosao_enemy["contador"] % 5 == 0:
                    explosao_enemy["frame"] += 1
                if explosao_enemy["frame"] >= len(enemy_explosion_images):
                    explosoes_enemy.remove(explosao_enemy)

        tela.blit(background, (0, 0))
        planet_contador += 1
        if planet_contador % 7 == 0:
            planet_frame += 1
        if planet_frame >= len(planet_element_images):
            planet_frame = 0
        tela.blit(planet_element_images[planet_frame], (885, 15))

        for asteroid in asteroids:
            tela.blit(asteroidimg, (asteroid["x"], asteroid["y"]))

        if score >= 200:
            for enemy in enemies_spaceship:
                tela.blit(enemy_spaceship_img, (enemy["x"], enemy["y"]))
            for enemy_laser in enemy_lasers:
                tela.blit(enemy_laser_img, (enemy_laser["x"], enemy_laser["y"]))

        if score >= 500:
            for final_enemy in final_enemies_spaceship:
                tela.blit(final_enemy_spaceship_img, (final_enemy["x"], final_enemy["y"]))
            for final_enemy_laser in final_enemy_lasers:
                tela.blit(final_enemy_laser_img, (final_enemy_laser["x"], final_enemy_laser["y"]))

        for laser in lasers:
            tela.blit(laserimg, (laser["x"], laser["y"]))
        
        for explosao_asteroid in explosoes_asteroid:
            if explosao_asteroid["frame"] < len(asteroid_explosion_images):
                img = asteroid_explosion_images[explosao_asteroid["frame"]]
                tela.blit(img, (explosao_asteroid["x"], explosao_asteroid["y"]))

        for explosao_enemy in explosoes_enemy:
            if explosao_enemy["frame"] < len(enemy_explosion_images):
                img = enemy_explosion_images[explosao_enemy["frame"]]
                tela.blit(img, (explosao_enemy["x"]-40, explosao_enemy["y"]-34))
        
        player()
        pontuacao()

        if pausado:
            fundo_pausa = pygame.Surface((largura, altura), pygame.SRCALPHA)
            fundo_pausa.fill((0, 0, 0, 150))
            tela.blit(fundo_pausa, (0,0))

            texto_pausa = fonte_menu.render("JOGO PAUSADO", True, "yellow")
            pos_texto = texto_pausa.get_rect(center=(largura / 2, altura / 2))
            tela.blit(texto_pausa, pos_texto)

        pygame.display.update()
        fps.tick(60)

while True:
    exibir_menu()
    game_loop()