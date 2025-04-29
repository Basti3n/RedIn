# RedIn

## Description

The goal of this script is to crawl Reddit and LinkedIn.

___

## Needed

- Python version: `3.12`
- Conda

___

## Installation

- `conda create -y --name redin_3_12 python=3.12`
- `conda activate redin_3_12`
- `pip install -r requirements.txt`
- Duplicate the file `settings_default.json` and rename it to `settings.json`
- Change the values inside with the ones you need

___

## Running

- Run `docker compose up -d` to start Minio, Redis and Celery
- Run `python -m worker`
- The script should run normally.

## URLs

- [Minio](http://localhost:9001/login)

## Issues

- I got banned from reddit making too many "unprotected call" to their website.
