
# MongoDB Twitter Management System

This project provides a command-line application for managing and interacting with tweets stored in a MongoDB database. The application includes functions for searching tweets, listing top tweets, and composing new tweets, as well as loading tweets from JSON data.

## Table of Contents

- [Features](#features)
- [Requirements](#requirements)
- [Setup](#setup)
- [Usage](#usage)
  - [Loading JSON Data](#loading-json-data)
  - [Running the Program](#running-the-program)
  - [Menu Options](#menu-options)
- [Example JSON Data Format](#example-json-data-format)

## Features

1. **Search Tweets**: Find tweets by keywords.
2. **Search Users**: Search for users by display name or location.
3. **List Top Tweets**: List tweets with the most retweets, likes, or quotes.
4. **List Top Users**: Display users with the highest follower count.
5. **Compose a Tweet**: Add a new tweet to the database.
6. **Load JSON Data**: Load tweet data from a JSON file into MongoDB.

## Requirements

- Python 3.x
- MongoDB
- `pymongo` library

## Setup

1. Clone the repository.
2. Install the required Python package:
   ```bash
   pip install pymongo
   ```
3. Ensure MongoDB is running on your system. If not installed, download and run it as instructed in the MongoDB documentation.

## Usage

### Loading JSON Data

To load tweets from a JSON file into MongoDB, run:

```bash
python load-json.py <json_file_name> <mongodb_port>
```

Replace `<json_file_name>` with the path to your JSON file and `<mongodb_port>` with the port MongoDB is listening on (default is `27017`).

### Running the Program

Start the main application using:

```bash
python program.py <mongodb_port>
```

Replace `<mongodb_port>` with the port MongoDB is listening on.

### Menu Options

1. **Search Tweets**: Enter keywords to search for tweets. Results are displayed, and you can view detailed information about each tweet.
2. **Search Users**: Search for users by display name or location. You can select a user to see detailed information.
3. **List Top Tweets**: Enter the metric to sort by (`retweetCount`, `likeCount`, or `quoteCount`) and the number of top tweets to display.
4. **List Top Users**: Enter the number of users to list by follower count. You can select a user to view more details.
5. **Compose a Tweet**: Enter text to create a new tweet, which will be saved to MongoDB.

## Example JSON Data Format

Here’s a sample format for a JSON tweet entry:

```json
{
    "url": "https://twitter.com/ShashiRajbhar6/status/1376739399593910273",
    "date": "2021-03-30T03:33:46+00:00",
    "content": "Support #FarmersProtest",
    "user": {
        "username": "ShashiRajbhar6",
        "displayname": "Shashi Rajbhar",
        "id": 1015969769760096256,
        "description": "Satya presan ho Sakta but prajit nhi",
        "followersCount": 1788,
        "location": "Azm Uttar Pradesh, India"
    },
    "retweetCount": 0,
    "likeCount": 0,
    "quoteCount": 0
}
```

## Example Commands

- Load data: `python load-json.py tweets.json 27017`
- Run program: `python program.py 27017`

## Notes

- The JSON file should follow the format of the `tweets` collection.
- MongoDB needs to be running locally on the specified port.
- MongoDB data is persistent, meaning tweets will remain in the database even after exiting the application.

---

This README.md provides a guide to set up, run, and use the MongoDB Twitter Management System.
