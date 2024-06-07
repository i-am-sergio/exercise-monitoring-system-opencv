from pytube import YouTube
import moviepy.editor as mp

# URL del video de YouTube
url = 'https://www.youtube.com/watch?v=jKTxe236-4U'

# Rango de tiempo en segundos (inicio, final)
start_time = 58  # Minuto 0:58 (120 segundos)
end_time = 68  # Minuto 1:08 (150 segundos)

# Crea un objeto YouTube
yt = YouTube(url)

# Descarga el video completo (temporal)
# video = yt.streams.first()
video = yt.streams.get_lowest_resolution()
video.download(filename="video_completo.mp4")

# Abre el video completo
video_clip = mp.VideoFileClip("video_completo.mp4")

# Selecciona el fragmento
fragmento = video_clip.subclip(start_time, end_time)

# Guarda el fragmento como un nuevo archivo
fragmento.write_videofile("flexion_fragment.mp4")
