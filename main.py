import ya_music
import spotify
from loguru import logger
import pickle


logger.add('debug.log', format='{time} {level} {message}', level="INFO", rotation="15 MB", compression="zip")



@logger.catch
def transfer_tracks():
    all_tracks = ya_music.start()
    with open('ya_music_tracks.pickle', 'rb') as file:
        all_tracks = pickle.load(file)
    uris = spotify.get_track_id(all_tracks)
    spotify.save_tracks(uris)


if __name__ == '__main__':
    transfer_tracks()

