class Cancion:
    def __init__(self, id, titulo, artista, album, genero, duracion_seg):
        self.id = str(id)
        self.titulo = titulo
        self.artista = artista
        self.album = album
        self.genero = genero
        self.duracion_seg = int(duracion_seg)

    def resumen(self):
        return f"{self.titulo} - {self.artista} ({self.album})"

    def __str__(self):
        return self.resumen()
