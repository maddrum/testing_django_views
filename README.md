# Run it

1. Copy and rename `./docker/env-sample` to `./docker/.env`
2. Adjust ENVs in `.docker/.env` as and if needed
3. Copy and rename `./django_src/settings/settings-sample.py` to `./django_src/settings/settings.py`
4. Adjust any settings, if needed
5. Run `docker-compose up --build`

> Note: Both local `.env` and `settings.py` are excluded from git, so you are free to do whatever you like.
