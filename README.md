# Disclaimer
This project is used to demonstrate concerns related to problems related with Django
testing project based on Server-Side rendering.


# Project details
In this project, we have a form that requires users to input working times
for their magnificent shops.
We expect most of the users to input times like: `10:00 - 18:00`.

There are also several extra cases:
-input: `10:00 - 24:00` or `10:00 - 00:00` marks shop will be open from some time to midnight. Both inputs should be allowed
- input: `00:00` - `24:00`, `00:00 - 00:00` marks shop will be open all day or is a "non-stop". Both inputs should be allowed

Shops must be opened at least for the specified minimal working hours/subject to a configurable setting/
Working times:
- should be in 24 hours format.
- format is set to be `%H:%M`, e.g. `10:00` or `13:45`,
- should be easily changeable/subject to a configurable setting/




# Run it

1. Copy and rename `./docker/env-sample` to `./docker/.env`
2. Adjust ENVs in `.docker/.env` as and if needed
3. Copy and rename `./django_src/settings/settings-sample.py` to `./django_src/settings/settings.py`
4. Adjust any settings, if needed
5. Run `docker-compose up --build`

> Note: Both local `.env` and `settings.py` are excluded from git, so you are free to do whatever you like.
