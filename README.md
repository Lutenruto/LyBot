# LyBot
## Bot Discord en Python

##Nécessaire à avoir
- installer la lib discord.py
- installer la lib python-dotenv
- installer la lib pynacl
- installer la lib youtube_dl
- installer la lib python-binance
- installer la lib requests

###Si vous êtes sur Windows il vous faut installer ffmpeg
- installer ce dossier : https://github.com/BtbN/FFmpeg-Builds/releases/download/autobuild-2021-07-06-12-37/ffmpeg-N-102848-gb7ba472f43-win64-gpl-shared.zip
- le déziper et le copier dans votre répertoire racine du disque C:\
- aller dans variable global de votre PC, puis PATH et renseigner le dossier bin du dossier ffmpeg

###Pour créer le .env, faire :
``py -m venv .env (pour Windows)``<br>
``python3.6 -m venv .env (pour Linux/MacOS)``
###Ensuite le sourcer avec :
``source .env\Script\activate (pour Windows)``<br>
``source .env/bin/activate (pour Linux/MAcOS)``