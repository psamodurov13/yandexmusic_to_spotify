import requests as rq
import time
from loguru import logger
import re
import json
from rich.progress import track
import pickle


headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'ru',
    'Accept-Encoding': 'gzip, deflate, br'
}
proxies = {
    'https': 'http://193.124.179.208:9849'
}


def start():
    s = rq.Session()
    response = s.get('https://music.yandex.ru/users/psamodurov13/playlists/3', headers=headers, proxies=proxies)
    match = re.search(r'var Mu=({.+?});', response.text)
    if not match:
        logger.debug('Not found json')
    json_tracks = json.loads(match.group(1))
    tracks_ids = json_tracks['pageData']['playlist']['trackIds']
    logger.info(f'TRACKS_IDS: {tracks_ids}')
    logger.info(f'TOTAL TRACKS: {len(tracks_ids)}')
    all_tracks = []
    collect = 0
    exceptions = []
    for track_id in track(tracks_ids, description='[green] YA-MUSIC', style='green'):
        ids = track_id.split(':')
        track_resp = s.get(f'https://music.yandex.ru/handlers/track.jsx?track={ids[0]}%3A{ids[1]}&lang=ru'
                               f'&external-domain=music.yandex.ru&overembed=false&ncrnd=0.20545402969652227',
                           headers=headers, proxies=proxies)
        track_resp.encoding = 'utf-8'
        track_json = track_resp.text
        logger.info(track_json)
        try:
            track_info = json.loads(track_json)
            all_tracks.append({'name': track_info['track']['title'], 'artist': [i['name'] for i in track_info['artists']]})
            logger.info(f'name: {track_info["track"]["title"]}, artist: {[i["name"] for i in track_info["artists"]]}')
            collect += 1
        except Exception:
            logger.exception(f'EXCEPT')
            exceptions.append(track_id)

    logger.info('COLLECT TRACKS FROM YANDEX MUSIC IS DONE')
    logger.info(f'COLLECTED - {collect}')
    logger.info(f'EXCEPTIONS - {len(exceptions)} ({exceptions})')
    with open('ya_music_tracks.pickle', 'wb') as file:
        pickle.dump(all_tracks, file)
    return all_tracks


if __name__ == '__main__':
    start()