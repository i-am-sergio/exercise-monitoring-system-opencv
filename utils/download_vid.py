from pytube import YouTube
import moviepy.editor as mp
import os

TEMP_VIDEO = "video_completo.mp4"

def recortar_video(url, start_time, end_time, output_path):
    yt = YouTube(url)

    name = "video_completo.mp4"

    # Descarga el video completo (temporal)
    video = yt.streams.get_highest_resolution()
    video.download(filename=name)

    # Abre el video completo
    video_clip = mp.VideoFileClip(name)

    # Selecciona el fragmento
    fragmento = video_clip.subclip(start_time, end_time)

    # Guarda el fragmento como un nuevo archivo
    fragmento.write_videofile(output_path)

    # Intenta eliminar el archivo temporal del video completo
    try:
        os.remove(name)
    except PermissionError as e:
        print(f"Error al eliminar el archivo temporal: {e}")

# Array con los enlaces de los videos y los tiempos de inicio y final
videos = [
    {
        "url": "https://www.youtube.com/watch?v=imzQa2hy8YU",
        "start_time": 0,  # Minuto 5:40 (340 segundos)
        "end_time": 12,    # Minuto 5:56 (356 segundos)
        "output_path": "detection/flexion.mp4"
    },
    {
        "url": "https://www.youtube.com/watch?v=1HyXlzqrJEs",
        "start_time": 3,  # Minuto 5:40 (340 segundos)
        "end_time": 10,    # Minuto 5:56 (356 segundos)
        "output_path": "detection/abdominal.mp4"
    },
    {
        "url": "https://www.youtube.com/shorts/-GrQe7ho1P4 ",
        "start_time": 0,  # Minuto 5:40 (340 segundos)
        "end_time": 17,    # Minuto 5:56 (356 segundos)
        "output_path": "detection/estocada.mp4"
    },
    {
        "url": "https://www.youtube.com/watch?v=5ZShK3AlGCk",
        "start_time": 127.3,  # Minuto 2:04 (122 segundos)
        "end_time": 155,    # Minuto 2:35 (155 segundos)
        "output_path": "detection/sentadilla.mp4"
    },
    {
        "url": "https://www.youtube.com/watch?v=CFBZ4jN1CMI&ab_channel=NationalAcademyofSportsMedicine(NASM)",
        "start_time": 0,  # Minuto 0:00 (0 segundos)
        "end_time": 18,    # Minuto 0:18 (18 segundos)
        "output_path": "detection/bicep.mp4"
    },
    {
        "url": "https://www.youtube.com/watch?v=2J2g7XOr2i4",
        "start_time": 115,  # Minuto 1:55 
        "end_time": 138,    # Minuto 2:18
        "output_path": "detection/jumping_jack.mp4"
    }
]

# Recorre la lista de videos y recorta cada uno
for video_info in videos:
    recortar_video(video_info["url"], video_info["start_time"], video_info["end_time"], video_info["output_path"])

# only cut last video of the list
#index = 3 # video 3
#recortar_video(videos[index]["url"], videos[index]["start_time"], videos[index]["end_time"], videos[index]["output_path"])