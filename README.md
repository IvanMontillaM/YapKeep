# YapKeep
Telegram bot that stores messages.

## How to build and deploy on DigitalOcean
DigitalOcean builds it for us in their [App Platform](https://cloud.digitalocean.com/apps/).

1. Create a new DigitalOcean App:
   1. Ensure _"Git repository"_ tab is selected.
   2. Select a _"Git provider"_ and _"Repository"_ where this source code is hosted.
   3. Select the _"Branch"_ this application runs from. Usually, the default is fine.
   4. Leave _"Source directories (Optional)"_ empty.
   5. Enable automatic deployments if you don't have a separate application for tests.
   6. Proceed to next step.
2. Set up resource settings:
   1. It's optional to change resource's name (Defaults to `yapkeep`).
   2. Change app's _"Instance size"_ to minimal (`512 MB RAM | 1 Shared vCPU  | 50 GB bandwidth` at `$5.00/mo`).
   3. At _Deployment settings_ set the _Run command_ to the one specified at the end of this section.
   4. Leave _Network settings_ at their defaults (_Public HTTP port_ at `8080`, no internal ports defined, and _HTTP request routes_ with 1 route set at `/`).
   5. Add environment variables on the resource, by clicking on the _"Add from .env"_ button.
      1. Copy the template from [.env-sample](/.env-sample) and fill in the values. Click on _"Save"_ button once done.
      2. Recommended: Set all environment variables to `Run time` in the _"Scope"_ setting for each one.
      3. Recommended: Enable encryption for every variable that ends with `_KEY`.
3. Skip creating _"App-level environment variables"_, as these are not necessary for this project.
4. Select a _"Region"_ for your app to be deployed.
   1. The closer to Telegram servers, the better. A reference: [What are the IP addresses of Telegram Data Centers?](https://docs.pyrogram.org/faq/what-are-the-ip-addresses-of-telegram-data-centers).
5. Finalize step:
   1. Choose a unique app name. The default setting is fine.
   2. Select a project. It defaults to the one you're currently at.
      1. Can be left as is if this is your first time using DigitalOcean.
   3. Click on the _"Create app"_ button on the right sidebar.

**Run command:** `gunicorn --worker-tmp-dir /dev/shm --pythonpath 'bot' --workers=3 --capture-output --enable-stdio-inheritance "app:app"`

### Environment variables required to run
- `BOT_WEBHOOK_KEY`: Part of the URL that Telegram hits when sending us notifications. Used as an anti-spam measure, security-through-obscurity (Currently, Telegram doesn't support a better way).
  - Example: `https://<app_fdqn>/webhook/<bot_webhook_key>`
- `OPT_PRETTYPRINT`: Pretty-print output JSONs on HTTP requests.
- `TG_API_KEY`: Telegram's main bot API key. Obtained through [BotFather](https://t.me/BotFather).
- `TG_OUTPUT_CHAT_ID`: Output of the logging activity. It could be a channel, group or individual account.

Refer to [.env-sample](/.env-sample) file for an updated environment variables template.
