from gtts import gTTS
from playsound import playsound
from bs4 import BeautifulSoup
from datetime import date, datetime
from os import remove
from glob import glob
from pathlib import Path
import requests

BASE_URL = "https://itla.edu.do"
AUTHOR_NAME = ""
AUTHOR_ENROLLMENT = ""

gTTS('Bienvenido al ITLA, ¿cuál es tu nombre?', lang='es').save('bienvenida.mp3')
playsound('bienvenida.mp3')

nombre = input("Ingresa tu nombre: ")

i = 0

while True:
    gTTS(f'¿{nombre} qué deseas preguntar? Si deseas preguntar sobre una carrera específica, escribe su nombre correctamente', lang='es').save(f'pregunta{i}.mp3')
    playsound(f'pregunta{i}.mp3')

    entrada = input("Escribe tu pregunta recordando que si quieres saber sobre una carrera debes escribir su nombre correctamente: ")

    res = requests.get(f"{BASE_URL}/carreras-tecnologicas/")
    html = BeautifulSoup(res.text, "html.parser")
    carreras = html.find_all("label", { "class": "text-red" })

    if 'carreras' in entrada.lower() in entrada.lower():
        gTTS(f'Hay {len(carreras)} carreras', lang='es').save(f'carreras{i}.mp3')
        playsound(f'carreras{i}.mp3')

    elif 'rector' in entrada.lower():
        res = requests.get(f"{BASE_URL}/despacho-del-rector/")
        html = BeautifulSoup(res.text, "html.parser")
        rector = html.find("h4", { "class": "text-blue" })
        gTTS(f'El nombre del rector del ITLA es: {rector.text}', lang='es').save(f'rector{i}.mp3')
        playsound(f'rector{i}.mp3')

    elif 'día' in entrada.lower() or 'dia' in entrada.lower() or 'hoy' in entrada.lower():
        fecha = date.today()
        gTTS(f'Hoy es: {fecha.day} del mes {fecha.month} del año {fecha.year}', lang='es').save(f'hoy{i}.mp3')
        playsound(f'hoy{i}.mp3')

    elif 'hora' in entrada.lower():
        hora = datetime.now().hour
        if int(hora) == 0:
            gTTS(f'Son las 12 am', lang='es').save(f'hora{i}.mp3')
        elif int(hora) < 13:
            gTTS(f'Son las {hora} am', lang='es').save(f'hora{i}.mp3')
        else:
            gTTS(f'Son las {int(hora) - 12} pm', lang='es').save(f'hora{i}.mp3')
        playsound(f'hora{i}.mp3')

    elif 'donde' in entrada.lower() and 'itla' in entrada.lower():
        gTTS('El ITLA se encuentra en la Caleta, Boca Chica', lang='es').save(f'ubicacion{i}.mp3')
        playsound(f'ubicacion{i}.mp3')

    elif 'nota' in entrada.lower():
        gTTS('La nota final de mi autor es un 100', lang='es').save(f'nota{i}.mp3')
        playsound(f'nota{i}.mp3')

    elif 'autor' in entrada.lower():
        gTTS(f'Mi creador es el estudiante de la carrera de desarrollo de software {AUTHOR_NAME} con la matrícula: {AUTHOR_ENROLLMENT}', lang='es').save(f'autor{i}.mp3')
        playsound(f'autor{i}.mp3')

    elif 'amadis' in entrada.lower():
        gTTS(f'Amadis Suarez es uno de los profesores de la materia de fundamentos de programación del ITLA.', lang='es').save(f'amadis{i}.mp3')
        playsound(f'amadis{i}.mp3')

    else:
        print("\nBuscando...\n")
        for carrera in carreras:
            if entrada.lower() in carrera.text.lower():
                res = requests.get(carrera.parent["href"])
                html = BeautifulSoup(res.text, "html.parser")
                info_carrera = html.find_all("p")[0]
                gTTS(info_carrera.text, lang='es').save(f'carrera{i}.mp3')
                playsound(f'carrera{i}.mp3')

    gTTS("¿Deseas preguntar algo más?", lang="es").save(f"fin{i}.mp3")
    playsound(f"fin{i}.mp3")

    eleccion = input("¿Deseas preguntar algo más? (S/N): ")

    if eleccion == "N" or eleccion == "n":
        gTTS(f"Que tengas felíz resto del día {nombre}.", lang="es").save(f"fin.mp3")
        playsound(f"fin.mp3")
        audio_files = glob(f"{Path().resolve()}/*.mp3")
        for audio in audio_files:
            remove(audio)
        break
    
    i+=1