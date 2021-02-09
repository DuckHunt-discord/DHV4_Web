# DuckHunt V4 Website (DHV4_Web)

![Discord](https://img.shields.io/discord/195260081036591104) 
![GitHub commit activity](https://img.shields.io/github/commit-activity/w/DuckHunt-discord/DHV4_Web) 
![Website](https://img.shields.io/website?url=https%3A%2F%2Fduckhunt.me)

The website that powers [https://duckhunt.me](https://duckhunt.me).

## Technical description

This is a Django website hosted in a docker container. The website uses three main parts, one of which is routed into this app :

- The static files (`/static/*`)
- The DuckHunt API (`/api/*`)
- The DuckHunt Website (Everything else)

The DuckHunt website itself is distributed in multiple distinct parts (apps in django) :

- Public, for the homepage, status pages, command lists and more
- Botdata, for everything related to the bot database : Guilds (discord servers), Channels, Players
- Docs, that renders the markdown files in [this repo](https://github.com/DuckHunt-discord/duckhunt.me-docs) and display them on the webpages, using a specific stylesheet.

For more information about the API, you can see [this page](https://duckhunt.me/docs/the-duckhunt-api/channels-scores-and-stats).

## How to contribute

Every app is divided in two main parts : 

- The templates, in the app templates directory, are HTML files with variables added using Jinja2.
Read [this](https://jinja.palletsprojects.com/en/2.11.x/templates/) for more information what you can do in templates.
  
- The views, that handle the HTTP request and fetch useful data from the database. This is the place you should edit first 
  if you wish to add more data in the webpages.
  
If you want to make substancial changes to the app, please open an issue first to make sure your changes will get accepted.
Don't hesitate to ask questions about the code by opening an issue or asking on Discord.

