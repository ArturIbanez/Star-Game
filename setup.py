from cx_Freeze import setup, Executable
import os

base = None
caminho_do_icone= os.path.join("assets", "icone-star-wars-game.ico")
executables = [
    Executable(
        "main.py",  
        base=base,
        target_name="stargame",
        icon= caminho_do_icone
    )
]
build_exe_options = {
    "packages": ["os", "pygame", "tkinter", "aifc", "chunk", "audioop", "pyttsx3"],
    "includes": ["pyttsx3.drivers.sapi5"],
    "include_files": ["assets/", "recursos"]
}

setup(
    name="stargame",
    version="1.0",
    description="Jogo de nave no estilo Space Shooter de rolagem lateral. O objetivo do jogador é sobreviver o maior tempo possível, destruindo asteroides e naves inimigas para acumular pontos.",
    options={"build_exe": build_exe_options},
    executables=executables
)