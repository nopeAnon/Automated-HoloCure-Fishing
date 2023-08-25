# Automated HoloCure fishing
![10000 combo](https://github.com/Hexus-One/Automated-HoloCure-Fishing/assets/5473838/9d92ab91-d6f2-4f1d-8d19-3885dc5a0c7a)

This project aims to automate the fishing in HoloCure.

This works in any **windowed** resolution, and you can move the window around, resize it or have it in the background, BUT it doesn't work when the game is minimised. Works with multi-monitor setups.

# Getting Started
~~[Video Tutorial](https://drive.google.com/file/d/14Xha8OWFiv26zBD4cYjMsHLD896q8RH4/view?usp=sharing) for absolute beginners.~~ (*working on making a new one*)

1. Clone this project.
2. Execute [prepare.bat](prepare.bat) or copy content to your console (this will setup a python "test_env" environment so you do not contaminate your system wide python installation).
3. Execute [launch_python.bat](launch_python.bat) to open a console using the environment or copy the content to your console or skip this step and
4. Open HoloCure.
5. Start fishing by opening holocure_fishing.py or in your console "python holocure_fishing.py" or by any other means you want.
6. Go to Holo House and start fishing.
7. Enjoy!

# Requirements
If you have python installed, run:
`pip install -r requirements.txt`

Or

* python 3.11.4 or later
* numpy (`pip install numpy`)
* opencv-python (`pip install opencv-python`)
* pywin32 (`pip install pywin32`)

<hr>

### [Turn off Auto HDR](https://github.com/nopeAnon/Automated-HoloCure-Fishing/issues/8#issuecomment-1685914312)

<hr>

### Recommended settings when fishing

Any setting is fine! As long as the game is windowed and not fullscreen.

# License

This project is licensed under the GNU General Public License version 3.0. For the complete license text, see the file [LICENSE](LICENSE). This license applies to all files in this distribution.
