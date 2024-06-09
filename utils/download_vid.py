from pytube import YouTube
import moviepy.editor as mp
import os

TEMP_VIDEO = "video_completo.mp4"

def recortar_video(url, start_time, end_time, output_path):
    yt = YouTube(url)
    video = yt.streams.get_highest_resolution()
    video.download(filename=TEMP_VIDEO)
    video_clip = mp.VideoFileClip(TEMP_VIDEO)
    fragmento = video_clip.subclip(start_time, end_time)
    fragmento.write_videofile(output_path, codec='libx264')
    fragmento.close()
    video_clip.close()
    try:
        os.remove(TEMP_VIDEO)
    except PermissionError as e:
        print(f"No se pudo eliminar el archivo temporal: {e}")

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
        "start_time": 122,  # Minuto 2:02 (122 segundos)
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
# for video_info in videos:
#     recortar_video(video_info["url"], video_info["start_time"], video_info["end_time"], video_info["output_path"])

# only cut last video of the list
recortar_video(videos[-3]["url"], videos[-3]["start_time"], videos[-3]["end_time"], videos[-3]["output_path"])