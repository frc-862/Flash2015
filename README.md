# PyFlash
Python rewrite of FRC team 862's 2015 Robot Flash using robotpy-wpilib.

## Installing Prerequisites
#### RoboRio (everyone)
Follow the automatic install guide [here](http://robotpy.readthedocs.org/en/latest/getting_started.html#automated-installation).

#### Windows
If you're on Windows, you'll need Python 3 and then you'll need to get "wpilib" and "pyfrc" from pip. You're on your own to figure out how to get those.

#### Linux
If you're on Linux, get python(3) and pip(3) from your package manager (apt-get, yum, pacman, etc). They could either be called python3 and pip3 or python and pip.

After python and pip are installed, run "pip3 install wpilib pyfrc".

## Deploying
To deploy to the RoboRio, run the following:
#### Windows
    py robot.py deploy --wc --skip-tests
#### Linux
    python3 robot.py deploy --wc --skip-tests

## Simulating
To simulate with a GUI showing what a RoboRio would theoretically output and also allowing you to change inputs, run the following:
#### Windows
    py robot.py sim
#### Linux
    python3 robot.py sim


## Documentation
You can find documentation on robotpy [here](http://robotpy.readthedocs.org/en/latest/index.html) and non-python-specific wpilib documentation which should still be accurate [here](http://wpilib.screenstepslive.com/s/4485).

