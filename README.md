# DuckHunt V4 Website (DHV4_Web)

![Discord](https://img.shields.io/discord/195260081036591104) 
![GitHub commit activity](https://img.shields.io/github/commit-activity/w/DuckHunt-discord/DHV4_Web) 
![Website](https://img.shields.io/website?url=https%3A%2F%2Fduckhunt.me)

The website that powers https://duckhunt.me.

## Technical description

This is a Django website hosted in a docker container. The website uses three main parts, one of which is routed into this app :

- The static files (`/static/*`)
- The DuckHunt API (`/api/*`)
- The DuckHunt Website (Everything else)

The DuckHunt website itelf is distributed in multiple distinct parts (apps in django) :

- Public, for the homepage, status pages, command lists and more
- Botdata, for everything related to the bot database : Guilds (discord servers), Channels, Players
- Docs, that renders the markdown files in [this repo](https://github.com/DuckHunt-discord/duckhunt.me-docs) and display them on the webpages, using a specific stylesheet.

