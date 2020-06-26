# music-server
[self-hosted] a flask-powered music server that can cache youtube audio and organise them into playlists

## setup
* install [ffmpeg](https://ffmpeg.org/download.html)
* install [python dependencies](./requirements.txt)
* initialize database files using flask-migrate
  ```
  $ flask db init
  $ flask db migrate
  $ flask db upgrade
  ```

## run
* start flask app
  ```
  $ flask run
    (or)
  $ flask run --host=0.0.0.0 --port=8080
  ```

## todo
* package
* flask production server?
* audio player on the same page as library: [APlayer fixed mode](https://aplayer.js.org/#/home?id=fixed-mode)
* recently added/played playlists
* better search
* dark mode
* ...
