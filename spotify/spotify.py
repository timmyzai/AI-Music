import asyncio
import json
import base64
import re
import json
import requests
import urllib.parse
from datetime import datetime

ACCESS_TOKEN_FILE = 'spotify/access_token.txt'
SECRET_FILE = 'secret.json'
EMOTION_SONG_ATTRIBUTE_FILE = 'spotify/emotion-song-attribute/emotion-song-attribute.json'
emotion_dict = {0: "Angry", 1: "Disgusted", 2: "Fearful", 3: "Happy", 4: "Neutral", 5: "Sad", 6: "Surprised"}

class rec_song_input_dto:
    def __init__(self, limit=None, market=None, seed_artists=None, seed_genres=None, seed_tracks=None,
                 min_acousticness=None, max_acousticness=None, target_acousticness=None,
                 min_danceability=None, max_danceability=None, target_danceability=None,
                 min_duration_ms=None, max_duration_ms=None, target_duration_ms=None,
                 min_energy=None, max_energy=None, target_energy=None,
                 min_instrumentalness=None, max_instrumentalness=None, target_instrumentalness=None,
                 min_key=None, max_key=None, target_key=None,
                 min_liveness=None, max_liveness=None, target_liveness=None,
                 min_loudness=None, max_loudness=None, target_loudness=None,
                 min_mode=None, max_mode=None, target_mode=None,
                 min_popularity=None, max_popularity=None, target_popularity=None,
                 min_speechiness=None, max_speechiness=None, target_speechiness=None,
                 min_tempo=None, max_tempo=None, target_tempo=None,
                 min_time_signature=None, max_time_signature=None, target_time_signature=None,
                 min_valence=None, max_valence=None, target_valence=None):
        self.limit = limit
        self.market = market
        self.seed_artists = seed_artists
        self.seed_genres = seed_genres
        self.seed_tracks = seed_tracks
        self.min_acousticness = min_acousticness
        self.max_acousticness = max_acousticness
        self.target_acousticness = target_acousticness
        self.min_danceability = min_danceability
        self.max_danceability = max_danceability
        self.target_danceability = target_danceability
        self.min_duration_ms = min_duration_ms
        self.max_duration_ms = max_duration_ms
        self.target_duration_ms = target_duration_ms
        self.min_energy = min_energy
        self.max_energy = max_energy
        self.target_energy = target_energy
        self.min_instrumentalness = min_instrumentalness
        self.max_instrumentalness = max_instrumentalness
        self.target_instrumentalness = target_instrumentalness
        self.min_key = min_key
        self.max_key = max_key
        self.target_key = target_key
        self.min_liveness = min_liveness
        self.max_liveness = max_liveness
        self.target_liveness = target_liveness
        self.min_loudness = min_loudness
        self.max_loudness = max_loudness
        self.target_loudness = target_loudness
        self.min_mode = min_mode
        self.max_mode = max_mode
        self.target_mode = target_mode
        self.min_popularity = min_popularity
        self.max_popularity = max_popularity
        self.target_popularity = target_popularity
        self.min_speechiness = min_speechiness
        self.max_speechiness = max_speechiness
        self.target_speechiness = target_speechiness
        self.min_tempo = min_tempo
        self.max_tempo = max_tempo
        self.target_tempo = target_tempo
        self.min_time_signature = min_time_signature
        self.max_time_signature = max_time_signature
        self.target_time_signature = target_time_signature
        self.min_valence = min_valence
        self.max_valence = max_valence
        self.target_valence = target_valence

async def get_access_token():
    with open(SECRET_FILE) as f:
        config_data = json.load(f)
    client_id = config_data['client_id']
    client_secret = config_data['client_secret']

    auth_header = base64.b64encode(
        f"{client_id}:{client_secret}".encode('ascii')).decode('ascii')

    auth_options = {
        'url': 'https://accounts.spotify.com/api/token',
        'headers': {
            'Authorization': f'Basic {auth_header}'
        },
        'form': {
            'grant_type': 'client_credentials'
        }
    }

    response = requests.post(
        auth_options['url'], headers=auth_options['headers'], data=auth_options['form'])
    response_data = response.json()

    if response.status_code != 200:
        raise Exception(
            f"Failed to retrieve access token, status code: {response.status_code}")

    access_token = response_data['access_token']

    with open(ACCESS_TOKEN_FILE, 'w') as f:
        f.write(f"{access_token}\n{datetime.now().isoformat()}")

    print(f"access_token: {access_token}")
    return access_token

async def read_access_token():
    try:
        with open(ACCESS_TOKEN_FILE, 'r') as f:
            access_token, timestamp_val = f.read().strip().split('\n')
            if not access_token or not timestamp_val:
                raise ValueError('Access token or timestamp is missing')
            timestamp = datetime.strptime(timestamp_val, '%Y-%m-%dT%H:%M:%S.%f')
            time_diff = (datetime.now() - timestamp).total_seconds()
            if time_diff < 3600: #60 minutes
                return access_token
            else:
                raise Exception('Access token has expired')
    except (FileNotFoundError, ValueError, Exception):
        pass
    return await get_access_token()

async def get_recommendation_songs(input_params: rec_song_input_dto):
    try:
        access_token = await read_access_token()
        url = process_get_recommended_songs_url(input_params)
        print("Going to get data from " + url)
        response = requests.get(url, headers={"Authorization": f"Bearer {access_token}"})
        response.raise_for_status()
        data = response.json()
        print(data)
        return data
    except Exception as error:
        print(error)
            
def process_get_recommended_songs_url(input: rec_song_input_dto):
    url = "https://api.spotify.com/v1/recommendations?"
    limit = input.limit
    market = input.market
    seed_artists = input.seed_artists
    seed_genres = input.seed_genres
    seed_tracks = input.seed_tracks
    min_acousticness = input.min_acousticness
    max_acousticness = input.max_acousticness
    target_acousticness = input.target_acousticness
    min_danceability = input.min_danceability
    max_danceability = input.max_danceability
    target_danceability = input.target_danceability
    min_duration_ms = input.min_duration_ms
    max_duration_ms = input.max_duration_ms
    target_duration_ms = input.target_duration_ms
    min_energy = input.min_energy
    max_energy = input.max_energy
    target_energy = input.target_energy
    min_instrumentalness = input.min_instrumentalness
    max_instrumentalness = input.max_instrumentalness
    target_instrumentalness = input.target_instrumentalness
    min_key = input.min_key
    max_key = input.max_key
    target_key = input.target_key
    min_liveness = input.min_liveness
    max_liveness = input.max_liveness
    target_liveness = input.target_liveness
    min_loudness = input.min_loudness
    max_loudness = input.max_loudness
    target_loudness = input.target_loudness
    min_mode = input.min_mode
    max_mode = input.max_mode
    target_mode = input.target_mode
    min_popularity = input.min_popularity
    max_popularity = input.max_popularity
    target_popularity = input.target_popularity
    min_speechiness = input.min_speechiness
    max_speechiness = input.max_speechiness
    target_speechiness = input.target_speechiness
    min_tempo = input.min_tempo
    max_tempo = input.max_tempo
    target_tempo = input.target_tempo
    min_time_signature = input.min_time_signature
    max_time_signature = input.max_time_signature
    target_time_signature = input.target_time_signature
    min_valence = input.min_valence
    max_valence = input.max_valence
    target_valence = input.target_valence
    if limit is not None:
        url += "limit=" + str(limit) + "&"
    if market is not None:
        url += f"market={market}&"
    if seed_artists is None:
        seed_artists_encoded = "4NHQUGzhtTLFvgF5SZesLK"
    url += f"seed_artists={seed_artists_encoded}&"
    if seed_genres is None:
        seed_genres ="classical,country"
    seed_genres_str = ",".join(seed_genres)
    seed_genres_encoded = urllib.parse.quote(seed_genres_str, safe="")
    url += f"seed_genres={seed_genres_encoded}&"
    if seed_tracks is None:
        seed_tracks = "0c6xIDDpzE81m2q797ordA"
    url += f"seed_tracks={seed_tracks}&"
    if min_acousticness is not None:
        if not isinstance(min_acousticness, (int, float)) or min_acousticness < 0 or min_acousticness > 1:
            raise ValueError("min_acousticness must be a number between 0 and 1")
        url += f"min_acousticness={min_acousticness}&"
    if max_acousticness is not None:
        if not isinstance(max_acousticness, (int, float)) or max_acousticness < 0 or max_acousticness > 1:
            raise ValueError("max_acousticness must be a number between 0 and 1")
        url += f"max_acousticness={max_acousticness}&"
    if target_acousticness is not None:
        if not isinstance(target_acousticness, (int, float)) or target_acousticness < 0 or target_acousticness > 1:
            raise ValueError("target_acousticness must be a number between 0 and 1")
        url += f"target_acousticness={target_acousticness}&"
    if min_danceability is not None:
        if not isinstance(min_danceability, (int, float)) or min_danceability < 0 or min_danceability > 1:
            raise ValueError("min_danceability must be a number between 0 and 1")
        url += f"min_danceability={min_danceability}&"
    if max_danceability is not None:
        if type(max_danceability) != float or max_danceability < 0 or max_danceability > 1:
            raise ValueError("max_danceability must be a float between 0 and 1")
        url += f"max_danceability={max_danceability}&"
        
    if target_danceability is not None:
        if type(target_danceability) != float or target_danceability < 0 or target_danceability > 1:
            raise ValueError("target_danceability must be a float between 0 and 1")
        url += f"target_danceability={target_danceability}&"
        
    if min_duration_ms is not None:
        if type(min_duration_ms) != int or min_duration_ms < 0:
            raise ValueError("min_duration_ms must be a non-negative integer")
        url += f"min_duration_ms={min_duration_ms}&"
        
    if max_duration_ms is not None:
        if type(max_duration_ms) != int or max_duration_ms < 0:
            raise ValueError("max_duration_ms must be a non-negative integer")
        url += f"max_duration_ms={max_duration_ms}&"
        
    if target_duration_ms is not None:
        if type(target_duration_ms) != int or target_duration_ms < 0:
            raise ValueError("target_duration_ms must be a non-negative integer")
        url += f"target_duration_ms={target_duration_ms}&"
        
    if min_energy is not None:
        if type(min_energy) != float or min_energy < 0 or min_energy > 1:
            raise ValueError("min_energy must be a float between 0 and 1")
        url += f"min_energy={min_energy}&"
        
    if max_energy is not None:
        if type(max_energy) != float or max_energy < 0 or max_energy > 1:
            raise ValueError("max_energy must be a float between 0 and 1")
        url += f"max_energy={max_energy}&"
        
    if target_energy is not None:
        if type(target_energy) != float or target_energy < 0 or target_energy > 1:
            raise ValueError("target_energy must be a float between 0 and 1")
        url += f"target_energy={target_energy}&"
        
    if min_instrumentalness is not None:
        if type(min_instrumentalness) != float or min_instrumentalness < 0 or min_instrumentalness > 1:
            raise ValueError("min_instrumentalness must be a float between 0 and 1")
        url += f"min_instrumentalness={min_instrumentalness}&"
        
    if max_instrumentalness is not None:
        if type(max_instrumentalness) != float or max_instrumentalness < 0 or max_instrumentalness > 1:
            raise ValueError("max_instrumentalness must be a float between 0 and 1")
        url += f"max_instrumentalness={max_instrumentalness}&"
        
    if min_key is not None:
        if type(min_key) != int or min_key < 0 or min_key > 11:
            raise ValueError("min_key must be an integer between 0 and 11")
        url += f"min_key={min_key}&"
    if target_instrumentalness is not None:
        if type(target_instrumentalness) != float or target_instrumentalness < 0 or target_instrumentalness > 1:
            raise ValueError("target_instrumentalness must be a float between 0 and 1")
        url += f"target_instrumentalness={target_instrumentalness}&"
        
    if max_key is not None:
        if type(max_key) != int or max_key < 0 or max_key > 11:
            raise ValueError("max_key must be an integer between 0 and 11")
        url += f"max_key={max_key}&"
        
    if target_key is not None:
        if type(target_key) != int or target_key < 0 or target_key > 11:
            raise ValueError("target_key must be an integer between 0 and 11")
        url += f"target_key={target_key}&"
        
    if min_liveness is not None:
        if type(min_liveness) != float or min_liveness < 0 or min_liveness > 1:
            raise ValueError("min_liveness must be a float between 0 and 1")
        url += f"min_liveness={min_liveness}&"
        
    if max_liveness is not None:
        if type(max_liveness) != float or max_liveness < 0 or max_liveness > 1:
            raise ValueError("max_liveness must be a float between 0 and 1")
        url += f"max_liveness={max_liveness}&"
        
    if target_liveness is not None:
        if type(target_liveness) != float or target_liveness < 0 or target_liveness > 1:
            raise ValueError("target_liveness must be a float between 0 and 1")
        url += f"target_liveness={target_liveness}&"
        
    if min_loudness is not None:
        if type(min_loudness) != float or min_loudness < -60 or min_loudness > 0:
            raise ValueError("min_loudness must be a float between -60 and 0")
        url += f"min_loudness={min_loudness}&"
        
    if max_loudness is not None:
        if type(max_loudness) != float or max_loudness < -60 or max_loudness > 0:
            raise ValueError("max_loudness must be a float between -60 and 0")
        url += f"max_loudness={max_loudness}&"
        
    if target_loudness is not None:
        if type(target_loudness) != float or target_loudness < -60 or target_loudness > 0:
            raise ValueError("target_loudness must be a float between -60 and 0")
        url += f"target_loudness={target_loudness}&"
        
    if min_mode is not None:
        if type(min_mode) != int or (min_mode != 0 and min_mode != 1):
            raise ValueError("min_mode must be either 0 or 1")
        url += f"min_mode={min_mode}&"
        
    if max_mode is not None:
        if type(max_mode) != int or (max_mode != 0 and max_mode != 1):
            raise ValueError("max_mode must be either 0 or 1")
        url += f"max_mode={max_mode}&"
        
    if target_mode is not None:
        if type(target_mode) != int or (target_mode != 0 and target_mode != 1):
            raise ValueError("target_mode must be either 0 or 1")
        url += f"target_mode={target_mode}&"
        
    if min_popularity is not None:
        if type(min_popularity) != int or min_popularity < 0 or min_popularity > 100:
            raise ValueError("min_popularity must be an integer between 0 and 100")
        url += f"min_popularity={min_popularity}&"
        
    if max_popularity is not None:
        if type(max_popularity) != int or max_popularity < 0 or max_popularity > 100:
            raise ValueError("max_popularity must be an integer between 0 and 100")
        url += f"max_popularity={max_popularity}&"

    if target_popularity is not None:
        if type(target_popularity) != int or target_popularity < 0 or target_popularity > 100:
            raise ValueError("target_popularity must be an integer between 0 and 100")
        url += f"target_popularity={target_popularity}&"

    if min_speechiness is not None:
        if type(min_speechiness) != float or min_speechiness < 0 or min_speechiness > 1:
            raise ValueError("min_speechiness must be a float between 0 and 1")
        url += f"min_speechiness={min_speechiness}&"

    if max_speechiness is not None:
        if type(max_speechiness) != float or max_speechiness < 0 or max_speechiness > 1:
            raise ValueError("max_speechiness must be a float between 0 and 1")
        url += f"max_speechiness={max_speechiness}&"

    if target_speechiness is not None:
        if type(target_speechiness) != float or target_speechiness < 0 or target_speechiness > 1:
            raise ValueError("target_speechiness must be a float between 0 and 1")
        url += f"target_speechiness={target_speechiness}&"

    if min_tempo is not None:
        if type(min_tempo) != int or min_tempo < 0 or min_tempo > 1000:
            raise ValueError("min_tempo must be a int between 0 and 1000")
        url += f"min_tempo={min_tempo}&"

    if max_tempo is not None:
        if type(max_tempo) != int or max_tempo < 0 or max_tempo > 1000:
            raise ValueError("max_tempo must be a int between 0 and 1000")
        url += f"max_tempo={max_tempo}&"

    if target_tempo is not None:
        if type(target_tempo) != int or target_tempo < 0 or target_tempo > 1000:
            raise ValueError("target_tempo must be a int between 0 and 1000")
        url += f"target_tempo={target_tempo}&"

    if min_time_signature is not None:
        if type(min_time_signature) != int or min_time_signature < 0 or min_time_signature > 7:
            raise ValueError("min_time_signature must be an integer between 0 and 7")
        url += f"min_time_signature={min_time_signature}&"

    if max_time_signature is not None:
        if type(max_time_signature) != int or max_time_signature < 0 or max_time_signature > 7:
            raise ValueError("max_time_signature must be an integer between 0 and 7")
        url += f"max_time_signature={max_time_signature}&"

    if target_time_signature is not None:
        if type(target_time_signature) != int or target_time_signature < 0 or target_time_signature > 7:
            raise ValueError("target_time_signature must be an integer between 0 and 7")
        url += f"target_time_signature={target_time_signature}&"

    if min_valence is not None:
        if type(min_valence) != float or min_valence < 0 or min_valence > 1:
            raise ValueError("min_valence must be a float between 0 and 1")
        url += f"min_valence={min_valence}&"

    if max_valence is not None:
        if type(max_valence) != float or max_valence < 0 or max_valence > 1:
            raise ValueError("max_valence must be a float between 0 and 1")
        url += f"max_valence={max_valence}&"

    if target_valence is not None:
        if type(target_valence) != float or target_valence < 0 or target_valence > 1:
            raise ValueError("target_valence must be a float between 0 and 1")
        url += f"target_valence={target_valence}&"
        
    url = re.sub(r'[?&]$', '', url)
    return url

def process_rec_song_input(emotion: str):
    param = rec_song_input_dto()

    with open(EMOTION_SONG_ATTRIBUTE_FILE) as f:
        data = json.load(f)

    emotion_data = data.get(emotion, {})

    param.seed_genres = emotion_data.get('seed_genres')
    param.min_energy = emotion_data.get('min_energy')
    param.max_energy = emotion_data.get('max_energy')
    param.target_acousticness = emotion_data.get('target_acousticness')
    param.min_danceability = emotion_data.get('min_danceability')
    param.max_valence = emotion_data.get('max_valence')
    param.target_valence = emotion_data.get('target_valence')
    param.target_energy = emotion_data.get('target_energy')
    param.min_tempo = emotion_data.get('min_tempo')
    param.max_tempo = emotion_data.get('max_tempo')
    param.min_instrumentalness = emotion_data.get('min_instrumentalness')
    param.max_instrumentalness = emotion_data.get('max_instrumentalness')

    return param

async def main(emotion: str):
    if emotion not in emotion_dict.values():
        raise ValueError(f"Invalid emotion: {emotion}. Please choose from: {', '.join(emotion_dict.values())}")
    param = process_rec_song_input(emotion)
    # print(json.dumps(param.__dict__, indent=4))
    result = await get_recommendation_songs(param)
    return result

