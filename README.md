# Screen Stream Application

## Overview

This application streams the screen and audio from a server to a client using Flask. It allows remote control of the server's mouse and keyboard.

## Features

- Stream screen and audio from the server.
- Remote control of mouse and keyboard.
- Adjustable image quality.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/DJJJNabba/screen-stream.git
   ```
2. Navigate into the project directory:
   ```bash
   cd screen-stream
   ```
3. Install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. Run the application:
   ```bash
   python app.py
   ```
2. Access the application in your web browser at `http://<SERVER_IPV4_ADDRESS>:5000`.

## Configuration

- Set the `SECRET_KEY` and `PASSWORD` in `config.py` for security.
- Adjust the `IMAGE_QUALITY` in `app.py` or via the login page.

## Contributing

Feel free to submit issues or pull requests to improve the project.

## License

This project is licensed under the MIT License. 