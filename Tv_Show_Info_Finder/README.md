# TV Show Information Finder

This project is a command-line application that allows users to search for TV shows, retrieve season and episode details, and display formatted information using the **TVMaze API**.

## Features

1. **Show Search**: Search for TV shows by name, retrieving relevant details like premiere year, end year, and genres.
2. **Season Listing**: View all seasons of a selected show, including premiere year, end year, and episode count.
3. **Episode Listing**: Retrieve all episodes of a selected season, with episode number, title, and average rating.
4. **Caching and Retry Logic**: Avoids rate limits by enabling optional request caching.

## Table of Contents

- [Features](#features)
- [Requirements](#requirements)
- [Setup](#setup)
- [Usage](#usage)
- [Functions Overview](#functions-overview)

## Requirements

- Python 3.x
- `requests` library
- `requests_cache` library (optional for caching)

Install the dependencies with:

```bash
pip install requests requests_cache
```

## Setup

- Clone the repository:
  ```bash
  git clone https://github.com/YourUsername/TV-Show-Finder.git
  cd TV-Show-Finder
  ```

## Usage

Run the script using:

```bash
python tv_show_finder.py
```

### Example Workflow

1. **Search for a show**: Enter the name of a show you’re interested in.
2. **Select a show**: Choose from a list of search results.
3. **View seasons**: Select a season to display all episodes.
4. **View episodes**: See a detailed list of episodes for the selected season.

## Functions Overview

- **get_shows(query)**: Searches for shows based on a query.
- **format_show_name(show)**: Formats show name with premiere/end years and genres.
- **get_seasons(show_id)**: Retrieves seasons for a show.
- **format_season_name(season)**: Formats season name with premiere/end years and episode count.
- **get_episodes_of_season(season_id)**: Retrieves all episodes for a season.
- **format_episode_name(episode)**: Formats episode information with season/episode numbers, title, and rating.

## API Information

This project uses the [TVMaze API](https://www.tvmaze.com/api) to retrieve show, season, and episode data.

---
