import requests
import logging
import os
import time
from requests.exceptions import HTTPError, RequestException

# Uncomment the line below to enable caching for repeated requests
# import requests_cache
# requests_cache.install_cache('tvmaze_cache', expire_after=86400)  # 1-day cache

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Use an environment variable for the base URL, with a default if not set
BASE_URL = os.getenv("TVMAZE_API_BASE_URL", "https://api.tvmaze.com/")

def get_shows(query: str):
    """
    Search for TV shows using the TV Maze API.
    If the show is not found, return None.
    
    :param query: Name of the TV show to search for
    :return: List of shows matching the query or None if an error occurred
    """
    url = BASE_URL + "search/shows"
    payload = {'q': query}
    
    try:
        response = requests.get(url, params=payload)
        response.raise_for_status()  # Check for HTTP errors
        return response.json()
    except HTTPError as http_err:
        logging.error(f"HTTP error occurred: {http_err}")
    except RequestException as req_err:
        logging.error(f"Request error occurred: {req_err}")
    except ValueError:
        logging.error("Error: Failed to parse JSON response.")
    return None

def format_show_name(show: dict) -> str:
    """
    Format the show name.
    
    :param show: Dictionary containing show details
    :return: Formatted string with show details
    """
    details = ['name', 'premiered', 'ended', 'genres']
    result = {detail: show.get(detail, '?') or '?' for detail in details}
    
    show_name = result['name']
    premiere_year = result['premiered'].split('-')[0] if result['premiered'] != '?' else '?'
    end_year = result['ended'].split('-')[0] if result['ended'] != '?' else '?'
    genres = ', '.join(result['genres']).lower() if result['genres'] != '?' else '?'
    
    return f"{show_name} ({premiere_year} - {end_year}, {genres})"

def get_seasons(show_id: int):
    """
    Get the seasons for a given show_id.
    
    :param show_id: The ID of the show
    :return: List of seasons or None if an error occurred
    """
    url = BASE_URL + f"shows/{show_id}/seasons"
    
    # Retry logic for rate-limited requests
    for _ in range(3):  # Retry up to 3 times
        try:
            response = requests.get(url)
            if response.status_code == 429:  # Rate limit exceeded
                logging.warning("Rate limit exceeded. Retrying after delay...")
                time.sleep(1)  # Wait before retrying
                continue
            response.raise_for_status()
            return response.json()
        except HTTPError as http_err:
            logging.error(f"HTTP error occurred: {http_err}")
        except RequestException as req_err:
            logging.error(f"Request error occurred: {req_err}")
        except ValueError:
            logging.error("Error: Failed to parse JSON response.")
        break
    return None

def format_season_name(season: dict) -> str:
    """
    Format the season name.
    
    :param season: Dictionary containing season details
    :return: Formatted string with season details
    """
    details = ['number', 'episodeOrder', 'premiereDate', 'endDate']
    results = {detail: season.get(detail, '?') or '?' for detail in details}
    
    season_num = results['number']
    premiere_year = results['premiereDate'].split('-')[0] if results['premiereDate'] != '?' else '?'
    end_year = results['endDate'].split('-')[0] if results['endDate'] != '?' else '?'
    episode_num = results['episodeOrder']
    
    return f"Season {season_num} ({premiere_year} - {end_year}), {episode_num} episodes"

def get_episodes_of_season(season_id: int):
    """
    Get the episodes of a given season of a show.
    
    :param season_id: The ID of the season
    :return: List of episodes or None if an error occurred
    """
    url = BASE_URL + f"seasons/{season_id}/episodes"
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except HTTPError as http_err:
        logging.error(f"HTTP error occurred: {http_err}")
    except RequestException as req_err:
        logging.error(f"Request error occurred: {req_err}")
    except ValueError:
        logging.error("Error: Failed to parse JSON response.")
    return None

def format_episode_name(episode: dict) -> str:
    """
    Format the episode name.
    
    :param episode: Dictionary containing episode details
    :return: Formatted string with episode details
    """
    details = ["season", "number", "name", "rating"]
    result = {detail: episode.get(detail, '?') or '?' for detail in details}
    
    season_num = str(result['season'])
    episode_num = str(result['number'])
    episode_name = result['name']
    rating = result['rating']['average'] if result['rating'] and result['rating']['average'] else '?'
    
    return f"S{season_num}E{episode_num} {episode_name} (rating: {rating})"

def main():
    """
    Main function to search, display shows, and fetch details of selected show.
    """
    query = input("Search for a show: ").strip()
    results = get_shows(query)
    
    if not results:
        print("No results found.")
        return

    print("Here are the results:")
    for i, result in enumerate(results, start=1):
        show = result['show']
        show_name = format_show_name(show)
        print(f"{i}. {show_name}")
    
    while True:
        try:
            show_num = int(input("\nSelect a show by number: ").strip())
            if 1 <= show_num <= len(results):
                break
            else:
                print("Error: Invalid show selection number. Please try again.")
        except ValueError:
            print("Error: Please enter a valid number.")

    show_id = results[show_num - 1]['show']['id']
    name = results[show_num - 1]['show']['name']
    seasons = get_seasons(show_id)
    
    if not seasons:
        print("No seasons found.")
        return

    print(f"Seasons of {name}:")
    for i, season in enumerate(seasons, start=1):
        season_name = format_season_name(season)
        print(f"{i}. {season_name}")
    
    while True:
        try:
            season_num = int(input("\nSelect a season by number: ").strip())
            if 1 <= season_num <= len(seasons):
                break
            else:
                print("Error: Invalid season selection number. Please try again.")
        except ValueError:
            print("Error: Please enter a valid number.")
    
    season_id = seasons[season_num - 1]['id']
    episodes = get_episodes_of_season(season_id)
    
    if not episodes:
        print("No episodes found.")
        return

    print(f"\nEpisodes of {name} Season {season_num}:")
    for i, episode in enumerate(episodes, start=1):
        episode_name = format_episode_name(episode)
        print(f"{i}. {episode_name}")

if __name__ == '__main__':
    main()
