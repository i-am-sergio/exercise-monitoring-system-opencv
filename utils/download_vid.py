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
        "start_time": 120,  # Minuto 5:40 (340 segundos)
        "end_time": 155,    # Minuto 5:56 (356 segundos)
        "output_path": "detection/sentadilla.mp4"
    },
    {
        "url": "https://www.youtube.com/watch?v=CFBZ4jN1CMI&ab_channel=NationalAcademyofSportsMedicine(NASM)",
        "start_time": 0,  # Minuto 5:40 (340 segundos)
        "end_time": 18,    # Minuto 5:56 (356 segundos)
        "output_path": "detection/bicep.mp4"
    }
]

# Recorre la lista de videos y recorta cada uno
for video_info in videos:
    recortar_video(video_info["url"], video_info["start_time"], video_info["end_time"], video_info["output_path"])
