import { createRequire } from 'module';
const require = createRequire(import.meta.url);

import fetch from 'node-fetch';
const request = require('request');

let access_token = null;

async function getAccessToken() {
    var client_id = '2e3752f95e1542e0a829a8ff35197192';
    var client_secret = '5966f5c271c84333828298a2e39e940c';

    var authOptions = {
        url: 'https://accounts.spotify.com/api/token',
        headers: {
            'Authorization': 'Basic ' + (new Buffer.from(client_id + ':' + client_secret).toString('base64'))
        },
        form: {
            grant_type: 'client_credentials'
        },
        json: true
    };

    request.post(authOptions, function (error, response, body) {
        if (!error && response.statusCode === 200) {
            access_token = body.access_token;
        }
    });
}

function getArtist() {
    var id = "0TnOYISbd1XYRBk9myaseg";
    fetch(`https://api.spotify.com/v1/artists/${id}`, {
        headers: {
            'Authorization': `Bearer ${access_token}`
        }
    })
        .then(response => response.json())
        .then(data => {
            console.log(data);
        })
        .catch(error => {
            console.error(error);
        });
}

function getRecommendationSongs(limit = 10, market = "ES", seed_artists, seed_genres, seed_tracks, min_acousticness, max_acousticness, target_acousticness, min_danceability, max_danceability, target_danceability, min_duration_ms, max_duration_ms, target_duration_ms, min_energy, max_energy, target_energy, min_instrumentalness, max_instrumentalness, target_instrumentalness, min_key, max_key, target_key, min_liveness, max_liveness, target_liveness, min_loudness, max_loudness, target_loudness, min_mode, max_mode, target_mode, min_popularity, max_popularity, target_popularity, min_speechiness, max_speechiness, target_speechiness, min_tempo, max_tempo, target_tempo, min_time_signature, max_time_signature, target_time_signature, min_valence, max_valence, target_valence, target = null, targetNetwork = null, amount = null) {
    var url_ = "https://api.spotify.com/v1/recommendations?";
    if (limit === null) {
        throw new Error("The parameter 'limit' cannot be null.");
    } else if (limit !== undefined) {
        url_ += "limit=" + encodeURIComponent("" + limit) + "&";
    }
    if (market === null) {
        throw new Error("The parameter 'market' cannot be null.");
    } else if (market !== undefined) {
        url_ += "market=" + encodeURIComponent("" + market) + "&";
    }
    if (seed_artists === null) {
        throw new Error("The parameter 'seed_artists' cannot be null.");
    } else if (seed_artists !== undefined) {
        url_ += "seed_artists=" + encodeURIComponent("" + seed_artists) + "&";
    }
    if (seed_genres === null) {
        throw new Error("The parameter 'seed_genres' cannot be null.");
    } else if (seed_genres !== undefined) {
        url_ += "seed_genres=" + encodeURIComponent("" + seed_genres) + "&";
    }
    if (seed_tracks === null) {
        throw new Error("The parameter 'seed_tracks' cannot be null.");
    } else if (seed_tracks !== undefined) {
        url_ += "seed_tracks=" + encodeURIComponent("" + seed_tracks) + "&";
    }
    if (min_acousticness !== undefined) {
        if (typeof min_acousticness !== 'number' || min_acousticness < 0 || min_acousticness > 1) {
            throw new Error("The parameter 'min_acousticness' must be a number between 0 and 1.");
        }
        url_ += "min_acousticness=" + encodeURIComponent("" + min_acousticness) + "&";
    }
    if (max_acousticness !== undefined) {
        if (typeof max_acousticness !== 'number' || max_acousticness < 0 || max_acousticness > 1) {
            throw new Error("The parameter 'max_acousticness' must be a number between 0 and 1.");
        }
        url_ += "max_acousticness=" + encodeURIComponent("" + max_acousticness) + "&";
    }
    if (target_acousticness !== undefined) {
        if (typeof target_acousticness !== 'number' || target_acousticness < 0 || target_acousticness > 1) {
            throw new Error("The parameter 'target_acousticness' must be a number between 0 and 1.");
        }
        url_ += "target_acousticness=" + encodeURIComponent("" + target_acousticness) + "&";
    }
    if (min_danceability !== undefined) {
        if (typeof min_danceability !== 'number' || min_danceability < 0 || min_danceability > 1) {
            throw new Error("The parameter 'min_danceability' must be a number between 0 and 1.");
        }
        url_ += "min_danceability=" + encodeURIComponent("" + min_danceability) + "&";
    }
    if (max_danceability !== undefined) {
        if (typeof max_danceability !== 'number' || max_danceability < 0 || max_danceability > 1) {
            throw new Error("The parameter 'max_danceability' must be a number between 0 and 1.");
        }
        url_ += "max_danceability=" + encodeURIComponent("" + max_danceability) + "&";
    }
    if (target_danceability !== undefined) {
        if (typeof target_danceability !== 'number' || target_danceability < 0 || target_danceability > 1) {
            throw new Error("The parameter 'target_danceability' must be a number between 0 and 1.");
        }
        url_ += "target_danceability=" + encodeURIComponent("" + target_danceability) + "&";
    }
    if (min_duration_ms !== undefined) {
        if (!Number.isInteger(min_duration_ms)) {
            throw new Error("The parameter 'min_duration_ms' must be an integer.");
        }
        url_ += "min_duration_ms=" + encodeURIComponent("" + min_duration_ms) + "&";
    }
    if (max_duration_ms !== undefined) {
        if (!Number.isInteger(max_duration_ms)) {
            throw new Error("The parameter 'max_duration_ms' must be an integer.");
        }
        url_ += "max_duration_ms=" + encodeURIComponent("" + max_duration_ms) + "&";
    }
    if (target_duration_ms !== undefined) {
        if (!Number.isInteger(target_duration_ms)) {
            throw new Error("The parameter 'target_duration_ms' must be an integer.");
        }
        url_ += "target_duration_ms=" + encodeURIComponent("" + target_duration_ms) + "&";
    }
    if (min_energy !== undefined) {
        if (typeof min_energy !== 'number' || min_energy < 0 || min_energy > 1) {
            throw new Error("The parameter 'min_energy' must be a number between 0 and 1.");
        }
        url_ += "min_energy=" + encodeURIComponent("" + min_energy) + "&";
    }
    if (max_energy !== undefined) {
        if (typeof max_energy !== 'number' || max_energy < 0 || max_energy > 1) {
            throw new Error("The parameter 'max_energy' must be a number between 0 and 1.");
        }
        url_ += "max_energy=" + encodeURIComponent("" + max_energy) + "&";
    }
    if (target_energy !== undefined && (target_energy < 0 || target_energy > 1)) {
        throw new Error("The parameter 'target_energy' must be a number between 0 and 1.");
    } else if (target_energy !== undefined) {
        url_ += "target_energy=" + encodeURIComponent("" + target_energy) + "&";
    }
    if (min_instrumentalness !== undefined && (min_instrumentalness < 0 || min_instrumentalness > 1)) {
        throw new Error("The parameter 'min_instrumentalness' must be a number between 0 and 1.");
    } else if (min_instrumentalness !== undefined) {
        url_ += "min_instrumentalness=" + encodeURIComponent("" + min_instrumentalness) + "&";
    }
    if (max_instrumentalness !== undefined && (max_instrumentalness < 0 || max_instrumentalness > 1)) {
        throw new Error("The parameter 'max_instrumentalness' must be a number between 0 and 1.");
    } else if (max_instrumentalness !== undefined) {
        url_ += "max_instrumentalness=" + encodeURIComponent("" + max_instrumentalness) + "&";
    }
    if (target_instrumentalness !== undefined && (target_instrumentalness < 0 || target_instrumentalness > 1)) {
        throw new Error("The parameter 'target_instrumentalness' must be a number between 0 and 1.");
    } else if (target_instrumentalness !== undefined) {
        url_ += "target_instrumentalness=" + encodeURIComponent("" + target_instrumentalness) + "&";
    }
    if (min_key !== undefined && (min_key < 0 || min_key > 11)) {
        throw new Error("The parameter 'min_key' must be an integer between 0 and 11.");
    } else if (min_key !== undefined) {
        url_ += "min_key=" + encodeURIComponent("" + min_key) + "&";
    }
    if (max_key !== undefined && (max_key < 0 || max_key > 11)) {
        throw new Error("The parameter 'max_key' must be an integer between 0 and 11.");
    } else if (max_key !== undefined) {
        url_ += "max_key=" + encodeURIComponent("" + max_key) + "&";
    }
    if (target_key !== undefined) {
        if (typeof target_key !== 'number' || target_key < 0 || target_key > 11) {
            throw new Error("The parameter 'target_key' must be an integer between 0 and 11.");
        }
        url_ += "target_key=" + encodeURIComponent("" + target_key) + "&";
    }
    if (min_liveness !== undefined) {
        if (typeof min_liveness !== 'number' || min_liveness < 0 || min_liveness > 1) {
            throw new Error("The parameter 'min_liveness' must be a number between 0 and 1.");
        }
        url_ += "min_liveness=" + encodeURIComponent("" + min_liveness) + "&";
    }
    if (max_liveness !== undefined) {
        if (typeof max_liveness !== 'number' || max_liveness < 0 || max_liveness > 1) {
            throw new Error("The parameter 'max_liveness' must be a number between 0 and 1.");
        }
        url_ += "max_liveness=" + encodeURIComponent("" + max_liveness) + "&";
    }
    if (target_liveness !== undefined) {
        if (typeof target_liveness !== 'number' || target_liveness < 0 || target_liveness > 1) {
            throw new Error("The parameter 'target_liveness' must be a number between 0 and 1.");
        }
        url_ += "target_liveness=" + encodeURIComponent("" + target_liveness) + "&";
    }
    if (min_loudness !== undefined) {
        if (typeof min_loudness !== 'number') {
            throw new Error("The parameter 'min_loudness' must be a number.");
        }
        url_ += "min_loudness=" + encodeURIComponent("" + min_loudness) + "&";
    }
    if (max_loudness !== undefined) {
        if (typeof max_loudness !== 'number') {
            throw new Error("The parameter 'max_loudness' must be a number.");
        }
        url_ += "max_loudness=" + encodeURIComponent("" + max_loudness) + "&";
    }
    if (target_loudness !== undefined) {
        if (typeof target_loudness !== 'number') {
            throw new Error("The parameter 'target_loudness' must be a number.");
        }
        url_ += "target_loudness=" + encodeURIComponent("" + target_loudness) + "&";
    }
    if (min_mode !== undefined) {
        if (typeof min_mode !== 'number' || min_mode < 0 || min_mode > 1) {
            throw new Error("The parameter 'min_mode' must be an integer between 0 and 1.");
        }
        url_ += "min_mode=" + encodeURIComponent("" + min_mode) + "&";
    }
    if (max_mode !== undefined) {
        if (typeof max_mode !== 'number' || max_mode < 0 || max_mode > 1) {
            throw new Error("The parameter 'max_mode' must be an integer between 0 and 1.");
        }
        url_ += "max_mode=" + encodeURIComponent("" + max_mode) + "&";
    }
    if (target_mode !== undefined) {
        if (typeof target_mode !== 'number' || target_mode < 0 || target_mode > 1) {
            throw new Error("The parameter 'target_mode' must be an integer between 0 and 1.");
        }
        url_ += "target_mode=" + encodeURIComponent("" + target_mode) + "&";
    }
    if (min_popularity !== undefined) {
        if (typeof min_popularity !== 'number' || min_popularity < 0 || min_popularity > 100 || !Number.isInteger(min_popularity)) {
            throw new Error("The parameter 'min_popularity' must be an integer between 0 and 100.");
        }
        url_ += "min_popularity=" + encodeURIComponent("" + min_popularity) + "&";
    }
    if (max_popularity !== undefined) {
        if (typeof max_popularity !== 'number' || max_popularity < 0 || max_popularity > 100 || !Number.isInteger(max_popularity)) {
            throw new Error("The parameter 'max_popularity' must be an integer between 0 and 100.");
        }
        url_ += "max_popularity=" + encodeURIComponent("" + max_popularity) + "&";
    }
    if (target_popularity !== undefined) {
        if (typeof target_popularity !== 'number' || target_popularity < 0 || target_popularity > 100 || !Number.isInteger(target_popularity)) {
            throw new Error("The parameter 'target_popularity' must be an integer between 0 and 100.");
        }
        url_ += "target_popularity=" + encodeURIComponent("" + target_popularity) + "&";
    }
    if (min_speechiness !== undefined) {
        if (typeof min_speechiness !== 'number' || min_speechiness < 0 || min_speechiness > 1) {
            throw new Error("The parameter 'min_speechiness' must be a number between 0 and 1.");
        }
        url_ += "min_speechiness=" + encodeURIComponent("" + min_speechiness) + "&";
    }
    if (max_speechiness !== undefined) {
        if (typeof max_speechiness !== 'number' || max_speechiness < 0 || max_speechiness > 1) {
            throw new Error("The parameter 'max_speechiness' must be a number between 0 and 1.");
        }
        url_ += "max_speechiness=" + encodeURIComponent("" + max_speechiness) + "&";
    }
    if (target_speechiness !== undefined) {
        if (typeof target_speechiness !== 'number' || target_speechiness < 0 || target_speechiness > 1) {
            throw new Error("The parameter 'target_speechiness' must be a number between 0 and 1.");
        }
        url_ += "target_speechiness=" + encodeURIComponent("" + target_speechiness) + "&";
    }
    if (min_tempo !== undefined) {
        if (typeof min_tempo !== 'number' || min_tempo < 0) {
            throw new Error("The parameter 'min_tempo' must be a number greater than or equal to 0.");
        }
        url_ += "min_tempo=" + encodeURIComponent("" + min_tempo) + "&";
    }
    if (max_tempo !== undefined) {
        if (typeof max_tempo !== 'number' || max_tempo < 0) {
            throw new Error("The parameter 'max_tempo' must be a number greater than or equal to 0.");
        }
        url_ += "max_tempo=" + encodeURIComponent("" + max_tempo) + "&";
    }
    if (target_tempo !== undefined) {
        if (typeof target_tempo !== 'number' || target_tempo < 0) {
            throw new Error("The parameter 'target_tempo' must be a positive number.");
        }
        url_ += "target_tempo=" + encodeURIComponent("" + target_tempo) + "&";
    }
    if (min_time_signature !== undefined) {
        if (!Number.isInteger(min_time_signature) || min_time_signature < 0 || min_time_signature > 11) {
            throw new Error("The parameter 'min_time_signature' must be an integer between 0 and 11.");
        }
        url_ += "min_time_signature=" + encodeURIComponent("" + min_time_signature) + "&";
    }
    if (max_time_signature !== undefined) {
        if (!Number.isInteger(max_time_signature) || max_time_signature < 0 || max_time_signature > 11) {
            throw new Error("The parameter 'max_time_signature' must be an integer between 0 and 11.");
        }
        url_ += "max_time_signature=" + encodeURIComponent("" + max_time_signature) + "&";
    }
    if (target_time_signature !== undefined) {
        if (!Number.isInteger(target_time_signature) || target_time_signature < 0 || target_time_signature > 11) {
            throw new Error("The parameter 'target_time_signature' must be an integer between 0 and 11.");
        }
        url_ += "target_time_signature=" + encodeURIComponent("" + target_time_signature) + "&";
    }
    if (min_valence !== undefined) {
        if (typeof min_valence !== 'number' || min_valence < 0 || min_valence > 1) {
            throw new Error("The parameter 'min_valence' must be a number between 0 and 1.");
        }
        url_ += "min_valence=" + encodeURIComponent("" + min_valence) + "&";
    }
    if (max_valence !== undefined) {
        if (typeof max_valence !== 'number' || max_valence < 0 || max_valence > 1) {
            throw new Error("The parameter 'max_valence' must be a number between 0 and 1.");
        }
        url_ += "max_valence=" + encodeURIComponent("" + max_valence) + "&";
    }
    if (target_valence !== undefined) {
        if (typeof target_valence !== 'number' || target_valence < 0 || target_valence > 1) {
            throw new Error("The parameter 'target_valence' must be a number between 0 and 1.");
        }
        url_ += "target_valence=" + encodeURIComponent("" + target_valence) + "&";
    }
    url_ = url_.replace(/[?&]$/, "");

    fetch(url_, {
        headers: {
            'Authorization': `Bearer ${access_token}`
        }
    })
        .then(response => response.json())
        .then(data => {
            console.log(data);
        })
        .catch(error => {
            if (error.message === 'The access token expired') {
                getAccessToken().then(() => {
                    console.log("try again");
                    console.log(access_token);
                    getRecommendationSongs(limit, market, seed_artists, seed_genres, seed_tracks, min_acousticness, max_acousticness, target_acousticness, min_danceability, max_danceability, target_danceability, min_duration_ms, max_duration_ms, target_duration_ms, min_energy, max_energy, target_energy, min_instrumentalness, max_instrumentalness, target_instrumentalness, min_key, max_key, target_key, min_liveness, max_liveness, target_liveness, min_loudness, max_loudness, target_loudness, min_mode, max_mode, target_mode, min_popularity, max_popularity, target_popularity, min_speechiness, max_speechiness, target_speechiness, min_tempo, max_tempo, target_tempo, min_time_signature, max_time_signature, target_time_signature, min_valence, max_valence, target_valence, target, targetNetwork, amount);
                });
            } else {
                console.error(error);
            }
        });
}

getRecommendationSongs();