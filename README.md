# CityPass Astana Telegram Bot

## Overview
CityPass Astana is a Telegram bot designed to assist tourists and residents in navigating the city of Astana more efficiently. The bot uses machine learning to recognize places from photos or text queries and provides directions or displays the location on a map. This project combines a Python Flask backend with a Telegram bot frontend to deliver a seamless user experience.

## Features

- **Place Recognition**: Identify places based on user-submitted photos or text descriptions.
- **Route Generation**: Provide users with directions to recognized or specified locations.
- **Map Integration**: Mark identified places on a map for easy visualization.

## Technologies Used

- **Python**: Primary programming language for backend and bot development.
- **Flask**: Lightweight WSGI web application framework used to handle requests from the Telegram bot.
- **Machine Learning**: Utilizes ML models to process and recognize images and text.
- **Telegram Bot API**: Interface for bot operations like receiving messages and sending responses.

## Libraries Used

- `python-telegram-bot`: Library to handle interactions with the Telegram Bot API.
- `flask`: Serves the backend application and handles HTTP requests.
- `numpy`: Supports data manipulation and serves as a backbone for other libraries handling more complex mathematical operations.
- `tensorflow`: For implementing and running machine learning models.
- `keras`: High-level neural networks API, running on top of TensorFlow.
- `pillow`: For image file manipulations.
- `pydantic`: Data validation and settings management using python type annotations.
- `fuzzywuzzy`: Python library for string matching.

Install the dependencies by this command ```pip install -r requirements.txt``` 

## Prerequisites

- Python 3.8-3.11
- pip for package installation
