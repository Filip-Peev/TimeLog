## Download

You can download the latest `.exe` version of the app from the [Releases page](https://github.com/Filip-Peev/TimeLog/releases).

- **Download** -> [TimeLog v3.1](https://github.com/Filip-Peev/TimeLog/releases/download/v3.1-EXE/Worker.Logger.v3.1.-.EXE.zip)

## Installation

1. Extract anywhere and click "Start.bat" file.
2. It will run the App and open your browser.

## Preview of the app
![App Screenshot](https://filip-peev.com/home/timelog/images/appPreview1.webp)

Running the source on Windows or [in Docker ](#docker-setup)
==========================

To start the app on Windows, follow these steps:

1\. Download the archive from here - 
<a href="https://github.com/Filip-Peev/TimeLog/releases/download/v3.1/TimeLog_v3.1.zip" target="_blank">TimeLog_v3.1</a>

2\. Extract the archive somewhere.


3\. To run the app, double-click on the `app.exe` file.

4\. Open your Browser


Once the app is running, open your browser and go to:

    http://127.0.0.1:5000

4a\. Or use the included Start file, that will run the exe and open the Browser for you.

5\. Input worker IDs

You can use a Handheld Scanner or manually add them and click Log button or press Enter

6\. To close the app, click the X of the window. No worries, the data will be saved.

--------------------

# Docker Setup

1\. Download and Install <a href="https://docs.docker.com/desktop/setup/install/windows-install/" target="_blank">Docker Desktop</a>
---------------

Docker Desktop relies on WSL 2 (Windows Subsystem for Linux 2) for its functionality.

Docker installs a Linux kernel inside WSL 2 to manage containers.

You will need to install WSL 2, which Docker Desktop will set up during installation.

2\. Download <a href="https://github.com/Filip-Peev/TimeLog/releases/download/v0.2/Worker.Logger.-.Docker.zip" target="_blank">Worker Logger - Docker.zip</a>
---------------

Extract the zip archive to C:\Worker-Logger for example

3\. Open CMD or Terminal inside that folder
---------------

You can change the Docker file with text editor if you want.

To build a Docker Image with the info from the Dockerfile,
type this command:

    docker build -t worker-logger .


4\. Run the Docker Image to start the Container
---------------
After the Image is created, type this command:

    docker run -p 5000:5000 worker-logger

The App runs on Docker, so you can delete the C:\Worker-Logger folder.

5\. Open your Browser
---------------
Once the Container is running, open your browser and go to:

    http://127.0.0.1:5000

6\. Input worker IDs
--------------------
You can use a Handheld Scanner or manually add them and click Log button or press Enter