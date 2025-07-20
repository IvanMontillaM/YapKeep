# YapKeep
Telegram bot that stores messages.

## How to build and deploy
DigitalOcean builds it for us in their [App Platform](https://cloud.digitalocean.com/apps/).

(TODO: specify path to AppSpec)

### Environment variables required to run
- `BOT_WEBHOOK_KEY`: Part of the URL that Telegram hits when sending us notifications. Used as an anti-spam measure, security-through-obscurity (Currently, Telegram doesn't support a better way).
  - Example: `https://<app_fdqn>/cf/<bot_webhook_key>`
- `DB_DATABASE`: Application's database.
- `DB_HOSTNAME`: Application's database hostname.
- `DB_OPT_ECHO`: Output SQLAlchemy's generated SQL statements in console/logs, set to `True` for debugging purposes.
- `DB_OPT_TRACK_MODIFICATIONS`: Set to `False` as we don't use this, see more at: [Flask-SQLAlchemy#Tracking Modifications](https://flask-sqlalchemy.palletsprojects.com/en/3.0.x/track-modifications/#tracking-modifications).
- `DB_PASSWORD`: Application's database password.
- `DB_PORT`: Application's database port.
- `DB_USERNAME`: Application's database username.
- `OPT_PRETTYPRINT`: Pretty-print output JSONs on HTTP requests.
- `TG_API_KEY`: Telegram's main bot API key. Obtained through [BotFather](https://t.me/BotFather).
- `THREAD_EXCEPTIONS_ECHO`: Propagate thread's exceptions to console/logs. Set to `True` for debugging purposes, or most errors will be hidden. See more at: [Flask-Executor#Propagate Exceptions](https://flask-executor.readthedocs.io/en/latest/#propagate-exceptions)
