# Favorite traks from YandexMusic to Spotify
This programm copy favorite tracks from your YandexMusic account to Spotify account

## For perform this task:
- open link https://developer.spotify.com/dashboard/login and log in. Than accept the terms
- create an app (fill name and description).
- copy client_id and client_secret and paste in appropriate rows in secrets.py
- open link https://developer.spotify.com/console/put-current-user-saved-tracks/ and press button "get token". In popup window activate checkbox "user-library-modify" and press button "request token". Copy token and paste into secrets.py ('token_for_add')
- in secrets.py fill 'ya_login'
- launch main.py and wait.
