#!/bin/sh

open --url http://127.0.0.1:8000/index.html
python -m http.server 8000 --bind 127.0.0.1 --directory $PWD/_site/html

