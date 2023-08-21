# Automated HoloCure fishing
![HighScore](https://github.com/nopeAnon/Automated-HoloCure-Fishing/assets/91358729/ceb6506a-19cd-493a-afcf-980f39125f8a)
This project aims to automate the fishing in HoloCure

To make this work, play HoloCure in **windowed mode at 1280x720** and **don't move/minimize** the window once you have started fishing

# To use the program, 
[Video Tutorial](https://drive.google.com/file/d/14Xha8OWFiv26zBD4cYjMsHLD896q8RH4/view?usp=sharing) for absolute beginners.

1. Clone this project
1. Open holocure_fishing.py
1. Open HoloCure and go to Holo House
1. Start fishing
1. Enjoy



# Requirements
If you have python installed, run:
`pip install -r requirements.txt`

Or

* python 3.11 or later
* pyautogui (`pip install pyautogui`)
* pywin32 (`pip install pypiwin32`)
* opencv-python (`pip install opencv-python`)

# Tips
The best area to fish is on the upper left side of the pond.
This will eliminate possible disturbances to the hit area.
![BestArea](https://github.com/nopeAnon/Automated-HoloCure-Fishing/assets/91358729/1d67594f-ae08-4777-acec-69cfd618ae51)

<hr>

### [Turn off Auto HDR](https://github.com/nopeAnon/Automated-HoloCure-Fishing/issues/8#issuecomment-1685914312)

<hr>

### Recommended settings when fishing

![Settings](https://github.com/nopeAnon/Automated-HoloCure-Fishing/assets/91358729/6e5bbc3c-2d98-4f1c-9ed1-93833103fee0)


### How to remove the "Do you want to enable multiple monitor support?(May decrease performance)[y/N]: "
comment this [line](https://github.com/nopeAnon/Automated-HoloCure-Fishing/blob/148d5ce8efee43f7a48ae869016cf555f8fed52c/holocure_fishing.py#L140)

so it should look like this
`# ask_multi_monitor_support()`
