import spotify_token
from urllib.parse import urlencode
import requests as rq
import secrets
from loguru import logger

access_token = spotify_token.get_access_token()


def get_track_id(all_tracks):
    uris = []
    headers = {
        'Authorization': f'Bearer {access_token}'
    }
    endpoint = 'https://api.spotify.com/v1/search'
    finded = 0
    exceptions = []
    for track in all_tracks:
        try:
            full_name = f'{track["name"]} {" ".join(track["artist"])}'
            logger.info(f'YA-NAME: {full_name}')
            data = urlencode({'q': f'{track["name"]} {" ".join(track["artist"])}', 'type': 'track'})
            lookup_url = f'{endpoint}?{data}'
            r = rq.get(lookup_url, headers=headers)
            logger.info(f'STATUS CODE - {r.status_code}')
            uri = r.json()['tracks']['items'][0]['uri']
            artists = [i['name'] for i in r.json()['tracks']['items'][0]['artists']]
            name = r.json()['tracks']['items'][0]['name']
            spotify_name = name + ' ' + ' '.join(artists)
            logger.info(f'SP-NAME: {spotify_name}')
            logger.info(f'{"-"*40}')
            uris.append(uri.split(':')[-1])
            finded += 1
        except Exception:
            logger.exception(f'EXCEPT {track}')
            exceptions.append(track)
    logger.info(f'FINDED - {finded}')
    logger.info(f'EXCEPTIONS - {len(exceptions)} ({exceptions})')
    return uris


def save_tracks(uris):
    logger.info(f'TOTAL TRACKS: {len(uris)}')
    count = len(uris) / 50
    if count % 1 != 0:
        count = int(count) + 1
    else:
        count = int(count)
    start_position = 0
    access_token = secrets.token_for_add
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }
    endpoint = 'https://api.spotify.com/v1/me/tracks'
    for i in range(count):
        if len(uris[start_position:]) > 50:
            to_add = uris[start_position:start_position + 50]
        else:
            to_add = uris[start_position:]
        data = urlencode({'ids': f'{",".join(to_add)}'})
        lookup_url = f'{endpoint}?{data}'
        r = rq.put(lookup_url, headers=headers)
        if r.status_code == 200:
            logger.info(f'{to_add} - ADDED')
        else:
            logger.info(r.status_code)
            logger.info(r.json())
        start_position += 50


if __name__ == '__main__':
    uris = get_track_id([{"name": "Anna", "artist": ['Jupiter One']},
                  {"name": "Fades Away", "artist": ['Avicii', 'Noonie Bao']}])
    logger.info(uris)
    save_tracks(uris)
