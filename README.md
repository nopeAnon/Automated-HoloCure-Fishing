# Automated HoloCure fishing
![10000 combo](https://github.com/Hexus-One/Automated-HoloCure-Fishing/assets/5473838/9d92ab91-d6f2-4f1d-8d19-3885dc5a0c7a)

This project aims to automate the fishing in HoloCure.

This works in any **windowed** resolution, and you can move the window around, resize it or have it in the background, BUT it doesn't work when the game is minimised. Works with multi-monitor setups.

# Getting Started on Windows
~~[Video Tutorial](https://drive.google.com/file/d/14Xha8OWFiv26zBD4cYjMsHLD896q8RH4/view?usp=sharing) for absolute beginners.~~ (*working on making a new one*)

1. Clone this project.
2. Execute [prepare.bat](prepare.bat) or copy content to your console (this will setup a python "test_env" environment so you do not contaminate your system wide python installation).
3. Execute [launch_python.bat](launch_python.bat) to open a console using the environment or copy the content to your console or skip this step and
4. Open HoloCure.
5. Start fishing by opening holocure_fishing.py or in your console "python holocure_fishing.py" or by any other means you want.
6. Go to Holo House and start fishing.
7. Enjoy!

# Getting Started on Linux

1. Make sure you have Python installed.
2. Install `Xwininfo` from your distribution's package manager.
 Might already be preinstalled on a lot of systems.
3. Clone or download this repo.
4. Open HoloCure and head to the fishing area.
5. Execute the run.sh script. (on some systems you might have to make the script executable first)
```shell
$ chmod +x run.sh
$ ./run.sh
```
6. Start fishing!

Notes (read first before running!)
- This has only been tested on X11. On Wayland, Holocure runs under the Xwayland compatibility layer so it **might** work, but I don't have a machine to test.
- Due to privacy issues, modern Linux applications and window managers don't listen to X key events when the window isn't focused. I am looking into workarounds but for now you'll have to keep the HoloCure window focused for the script to work.
- If you don't use WASD to move, you'll have to edit the script for it to pick up your custom keybinds:
    1. Locate HoloCure's `settings.json` file. Should be located under
    ```<steam install dir>/steamapps/compatdata/2420510/pfx/drive_c/users/steamuser/AppData/Local/HoloCure/settings.json```
    2. Open `platform_linux.py` and head over to the function named *def config_file_path*. Change the line so that it points to your settings.json file path.
    3. (Re-)start the script using run.sh. 
<hr>

### [Turn off Auto HDR](https://github.com/nopeAnon/Automated-HoloCure-Fishing/issues/8#issuecomment-1685914312)

<hr>

### Recommended settings when fishing

Any setting is fine! As long as the game is windowed and not fullscreen.


# Building from source
If you have python installed, run:
`pip install -r requirements.txt`

Or

* python 3.11.4 or later
* numpy (`pip install numpy`)
* opencv-python (`pip install opencv-python`)
* pywin32 (`pip install pywin32`)


# License

This project is licensed under the GNU General Public License version 3.0. For the complete license text, see the file [LICENSE](LICENSE). This license applies to all files in this distribution.
