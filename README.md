<a name="readme-top"></a>
<!-- PROJECT SHIELDS -->
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]
[![LinkedIn][linkedin-shield]][linkedin-url]


<!-- PROJECT LOGO -->
<br />
<p align="center">
  <a href="https://github.com/ferisystem/WhisperBot">
    <img src="https://raw.githubusercontent.com/ferisystem/ferisystem/files/files/whisperbot/logo.jpg" alt="Logo" width="250" height="250">
  </a>

  <h1 align="center">💌 Whisper Bot 💬</h3>

  <p align="center">
    Send Anonymous messages and Whisper messages in Telegram app
    <br />
    <a href="#getting-started"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="https://telegram.me/WhisAnoBot">View Demo</a>
    ·
    <a href="https://github.com/ferisystem/WhisperBot/issues">Report Bug</a>
    ·
    <a href="https://github.com/ferisystem/WhisperBot/issues">Request Feature</a>
  </p>
</p>



<!-- TABLE OF CONTENTS -->
<details open="open">
  <summary><h2 style="display: inline-block">Table of Contents</h2></summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgements">Acknowledgements</a></li>
  </ol>
</details>
<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- ABOUT THE PROJECT -->
## About The Project

<p align="center">
<img src="https://raw.githubusercontent.com/ferisystem/ferisystem/files/files/whisperbot/Capture.JPG" alt="Sample" align="center">
</p>

An efficient [Telegram-bot](https://core.telegram.org/bots/api) for send **Anonymous messages** and **Whisper messages** in regular type or special type that can be hide content or send to user' PV
<p align="right">(<a href="#readme-top">back to top</a>)</p>


### Built With

This section should list any major frameworks that you built your project using. Leave any add-ons/plugins for the acknowledgements section. Here are a few examples.
* [Python](https://python.org) 3.7v
* [Telegram-Bot Api](https://core.telegram.org/bots/api)
* [Aiogram Framework](https://github.com/aiogram/aiogram)
* [Telethon Framework](https://github.com/LonamiWebs/Telethon)
* [Redis](https://github.com/andymccurdy/redis-py)
<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- GETTING STARTED -->
## Getting Started

This is a help for installation.

<ul>

### Prerequisites

<ul>

* Ubuntu 16.04+ (I prefer 16.04)
* You have to installed Python3.6 because [Telethon](https://github.com/LonamiWebs/Telethon) need Python3.6. so follow helps on google for "install Python3.6 on ubuntu"
* Get ```API_HASH``` & ```API_ID``` at [my.telegram.org](https://my.telegram.org/)
* Get Bot_Token from [@Botfather](https://telegram.me/botfather)
* send ```/setprivacy``` to [@Botfather](https://telegram.me/botfather) and click on your bot username then click on **Disable**
* send ```/setinline``` to [@Botfather](https://telegram.me/botfather) and click on your bot username then send a short message that show on inline queries
* send ```/setinlinefeedback``` to [@Botfather](https://telegram.me/botfather) and click on your bot username then click on **Enabled**
* Get Channel ID from Telegram with forwarding a message to [@userinfobot](https://telegram.me/userinfobot) use this ID for bot logs message
* Get Group(Supergroup type) ID from Telegram with adding [@myidbot](https://telegram.me/myidbot) and send ```/getgroupid``` in group and take group ID. bot use this ID for Support messages
</ul>
<p align="right">(<a href="#readme-top">back to top</a>)</p>



### Installation

<ul>

1. Clone the repo
   ```sh
   git clone https://github.com/ferisystem/WhisperBot.git
   ```
2. in `config_bot.py` you have to change these values:
     - Enter your database name
       ```PY
       db = 'name_database'
       ```
       **note**: is optional. but you must change it for each bot you launch
     - Enter your Bot_Token
       ```PY
       "botToken": "Bot_Token"
       ```
    - Enter your numbericID and other admins numbericID
       ```PY
       sudo_users = (777000, telegram_datas['botToken'].split(':')[0], numbericID2, 3, 4, 5, ...) # PUT_YOUR_ADMINS_HERE
       ```
       **note**: don't delete ```777000, telegram_datas['botToken'].split(':')[0]```
    - Enter your ID again as SUDO(full admin)
       ```PY
       "sudo_id": SUDO_ID,
       ```
    - Enter your channel username and invite-link
       ```PY
       "chUsername": "YOUR_CHANNEL_USERNAME", # for force join
       "chLink": "YOUR_CHANNEL_LINK", # for force join
       ```
    - Enter your server IP
       ```PY
       "ip": "YOUR_SERVER_IP",
       ```
8. Now you have to run this command for first time to take Bot_Token
   ```sh
   python3.6 cron_jobs.py
   ```
   then enter bot_token here
9. And then you have to add this command in `crontab -e` on ubuntu terminal
   ```sh
   * * * * * python3.6 ./WhisperBot/cron_jobs.py
   ```
10. you should install modules in `docs/modules_python37.py` with this command on **WhisperBot folder**:
   ```sh
   python3.7 -m pip install -r docs/modules_python37.py
   ```
11. Now you can run your bot with `screen` for keep bot power on or without it on **WhisperBot folder**:
   ```sh
   python3.7 bot_main.py
   ```
   or
   ```sh
   screen -S whisperbot python3.7 bot_main.py
   ```
12. If you want to power off the bot, you should kill that process after use `screen` command:
   ```sh
   kill whisperbot
   ```


</ul>
</ul>
<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- ROADMAP -->
## Roadmap

- [x] Anti-save for special Whispers
- [x] Delete all Whisper sent before
- [x] Block user from recent list user
- [ ] Multi-language Support
    - [x] Persian
    - [x] English
    - [ ] Detusch

also you can see the [open issues](https://github.com/ferisystem/WhisperBot/issues) for a list of proposed features (and known issues).
<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- CONTRIBUTING -->
## Contributing

Dear programmer, you can help me in this project. how? read this text.
Contributions are what make the open source community such an amazing place to be learn, inspire, and create. Any contributions you make are **greatly appreciated**.

1. Fork the project
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a pull request
<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE` for more information.
<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- CONTACT -->
## Contact

Alireza Fereidouni (Feri) - [@ferisystem](https://telegram.me/ferisystem) - alirezafereidouni@protonmail.com

Project Link: [github.com/ferisystem/WhisperBot](https://github.com/ferisystem/WhisperBot)

Example Bot: [@WhisAnoBot](https://telegram.me/WhisAnoBot)
<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- ACKNOWLEDGEMENTS -->
## Acknowledgements
* [Iman Seyed](https://github.com/mzd245)
<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- MARKDOWN LINKS & IMAGES -->
[forks-shield]: https://img.shields.io/github/forks/ferisystem/WhisperBot.svg?style=for-the-badge
[forks-url]: https://github.com/ferisystem/WhisperBot/network/members
[stars-shield]: https://img.shields.io/github/stars/ferisystem/WhisperBot.svg?style=for-the-badge
[stars-url]: https://github.com/ferisystem/WhisperBot/stargazers
[issues-shield]: https://img.shields.io/github/issues/ferisystem/WhisperBot.svg?style=for-the-badge
[issues-url]: https://github.com/ferisystem/WhisperBot/issues
[license-shield]: https://img.shields.io/github/license/ferisystem/WhisperBot.svg?style=for-the-badge
[license-url]: https://github.com/ferisystem/WhisperBot/blob/main/LICENSE
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://linkedin.com/in/alireza-fereidouni-852bb11b1
[product-screenshot]: img/screenshot.png
