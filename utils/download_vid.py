from pytube import YouTube

# URL del video de YouTube
url = 'https://www.youtube.com/watch?v=jKTxe236-4U'

# Crea un objeto YouTube
yt = YouTube(url)

# Descarga el video en la máxima resolución disponible
video = yt.streams.get_highest_resolution()
video.download(filename="video1")
