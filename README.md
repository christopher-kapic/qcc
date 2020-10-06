# qcc
Python script for converting a selfie video into a simple lip-synced animation

**This project is not finished yet (as of October 6, 2020). I still need to add the map for phonemes to mouth shapes and stitch the frames together into a new video.
I would also like to structure the code more intuitively. Right now, everything I wrote is baked into the main.py script, which isn't great for organization and abstraction.**

I was inspired by [carykh's Automatic Lip Syncer](https://youtu.be/y3B8YqeLCpY) to create my own lip syncer. Carykh's is specific for scripted videos, and as far as I know it is closed-source. My version is designed for a more generic, non-scripted use.

In order to use this, you'll need to install the [Gentle Forced Aligner](https://lowerquality.com/gentle/). I couldn't figure out how to get the command line version to work, so you'll have to run the server for main.py to work. As of October 6, 2020 the easiest way to do this is run the Gentle app from the downloadable .dmg (on mac) before running main.py. If you are on Windows or Linux, you'll have to run the Gentle webapp with Docker.

First, you'll need to use pip to install all of the dependencies (it might help to make a virtual environment too):

<code>cd ~/your/path/qcc</code>

<code>python3 -m venv [name of environment]</code>

<code>source [name of environment]/bin/activate</code>

<code>pip3 install -r requirements.txt</code>

Then start Gentle (either with Docker or simply by running the app installed from the .dmg).

Then run main.py:

<code>python3 main.py [name of video] [neckless, or whatever your character is called]</code>

Then, in case you're new to virtual environments, you can exit the environment by simply running

<code>deactivate</code>

Things to do:
* Map phonemes to mouth shapes.
* Stitch frames together for new video
* Abstract out the code so different processes have their own scripts
