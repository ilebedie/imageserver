# Imageserver

## Overview
Image server is a microservice that can do basic image processing and store images.
Stores uploaded jpeg images, detects duplicates, makes thumbnails from jpeg.


## How to run
### Run server
To start server run:

    cd <project_dir>
    pip3 install -r requirements.txt
    python3 main.py [--host <host> --port <port>]

### Run tests
To run tests:

    cd <project_dir>
    pip3 install -r requirements.txt
    pytest

## TODO:
Add various mime types

Add s3 storage
