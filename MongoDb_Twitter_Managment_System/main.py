import pymongo
from pymongo import MongoClient
import sys
import re
from datetime import datetime

def connect_to_mongodb(port_number):
    client = MongoClient("localhost", int(port_number))
    db = client['291db']
    return db

def search_tweets(db):
    try:
        user_input = input("Enter one or more keywords separated by spaces: ")
        keywords = user_input.lower().split()

        keyword_patterns = [re.compile(rf'\b{re.escape(keyword)}\b', re.IGNORECASE) for keyword in keywords]


        # Search for tweets that match all keywords using AND semantics
        matching_tweets = db['tweets'].find({
            'content': {'$all': [pattern for pattern in keyword_patterns]}
        })

        matching_tweets = list(matching_tweets)

        # Display information for each matching tweet with numbering
        for i, tweet in enumerate(matching_tweets, start=1):
            print(f"\nTweet #{i} Information:")
            print(f"ID: {tweet['_id']}")
            print(f"Date: {tweet['date']}")
            print(f"Content: {tweet['content']}")
            
            # Display only the username from the nested user object
            username = tweet.get('user', {}).get('username', '')
            print(f"Username: {username}")

        if i > 0:
            while True:
                try:
                    selected_tweet_number = int(input("\nEnter the number of the tweet you would like to see more of (0 to exit): "))
                    if 0 <= selected_tweet_number <= i:
                        break
                    else:
                        print("Invalid input. Please enter a valid tweet number.")
                except ValueError:
                    print("Invalid input. Please enter a valid number.")

            if selected_tweet_number != 0:
                selected_tweet = db['tweets'].find_one({'_id': matching_tweets[selected_tweet_number - 1]['_id']})
                print("\nAll Fields:")
                for key, value in selected_tweet.items():
                    print(f"{key}: {value}")

    except Exception as e:
        print(f"Error searching tweets: {e}")

def search_users(db):
    searching = True
    while searching:
        user_input = input("Enter a keyword to search for a user or 0 to exit: ")
        if user_input == '0':
            searching = False
            return
        tweets = db['tweets']
        #case insensitive search for the keyword
        regex = f"(?i){user_input}"
        users = tweets.find({"$or": [{"user.displayname": {"$regex": regex}},{"user.location": {"$regex": regex}}]})
        count = 1
        users_displayed = []
        for user in users:
            username = user['user']['username']
            if username not in users_displayed:
                print(str(count) + f". Username: {username}")
                print(f"Display Name: {user['user']['displayname']}")
                if user['user']['location'] == '':
                    print("Location: N/A")
                else:
                    print(f"Location: {user['user']['location']}")
                print()
                count += 1
                users_displayed.append(username)
        exploring = True
        #keep looping until user doesn't want to explore anymore
        while exploring:
            try:
                continue_exploring = int(input("Enter a specific number of the user that you would like to or press 0 to not explore: "))
                if continue_exploring == 0:
                    exploring = False
                    break
                #use the index on users_displayed to identify the user to explore
                user = tweets.find_one({"user.username": users_displayed[continue_exploring - 1]})
                print()
                #print all of the users data    
                print(f"Display Name: {user['user']['displayname']}")
                print(f"User Name: {user['user']['username']}")
                print(f"ID: {user['user']['id']}")
                print(f"Description: {user['user']['rawDescription']}")
                print(f"Description URLs: {user['user']['descriptionUrls']}")
                print(f"Verified: {user['user']['verified']}")
                print(f"Created: {user['user']['created']}")
                if user['user']['location'] == '':
                    print("Location: N/A")
                else:
                    print(f"Location: {user['user']['location']}")
                print()
                print(f"Follower Count: {user['user']['followersCount']}")
                print(f"Friends Count: {user['user']['friendsCount']}")
                print(f"Statuses Count: {user['user']['statusesCount']}")
                print(f"Favourites Count: {user['user']['favouritesCount']}")
                print(f"Listed Count: {user['user']['listedCount']}")
                print(f"Media Count: {user['user']['mediaCount']}")
                print(f"Link URL: {user['user']['linkUrl']}")
                print(f"LinkTcourl: {user['user']['linkTcourl']}")
                print(f"Profile Image URL: {user['user']['profileImageUrl']}")
                print(f"Banner URL: {user['user']['profileBannerUrl']}")
                print(f"URL: {user['user']['url']}")
                
            except ValueError:
                print("That is not a valid input. Please enter a valid number")


        

def list_top_tweets(db):
    try:
        sort_field = input("Enter the field to sort by (retweetCount, likeCount, quoteCount): ").lower()
        n = int(input("Enter the number of top tweets to display: "))

        #MongoDB field to sort by based on user input
        sort_by_field = f"{sort_field}.count"

        top_tweets = list(db['tweets'].find().sort(sort_by_field, pymongo.DESCENDING).limit(n))

        for i, tweet in enumerate(top_tweets, start=1):
            print(f"\nTop Tweet #{i} Information:")
            print(f"ID: {tweet['_id']}")
            print(f"Date: {tweet['date']}")
            print(f"Content: {tweet['content']}")
            
            username = tweet.get('user', {}).get('username', '')
            print(f"Username: {username}")

        if i > 0:
            while True:
                try:
                    selected_tweet_number = int(input("\nEnter the number of the tweet you would like to see more of (0 to exit): "))
                    if 0 <= selected_tweet_number <= i:
                        break
                    else:
                        print("Invalid input. Please enter a valid tweet number.")
                except ValueError:
                    print("Invalid input. Please enter a valid number.")

            if selected_tweet_number != 0:
                selected_tweet = top_tweets[selected_tweet_number - 1]
                print("\nAll Fields:")
                for key, value in selected_tweet.items():
                    print(f"{key}: {value}")

    except Exception as e:
        print(f"Error listing top tweets: {e}")

def list_top_users(db):
    n = int(input("Enter the number of users you want to list: "))

    # Aggregate the users, group by username, and sort by followers count in descending order
    pipeline = [
        {"$group": {
            "_id": "$user.username",
            "displayname": {"$first": "$user.displayname"},
            "followersCount": {"$first": "$user.followersCount"}
        }},
        {"$sort": {"followersCount": -1}},
        {"$limit": n}
    ]

    # Executing the aggregation pipeline
    aggregated_users = list(db['tweets'].aggregate(pipeline))

    print()
    for i, user in enumerate(aggregated_users, start=1):
        print(str(i) + f". Username: {user['_id']}")
        print(f"Display Name: {user['displayname']}")
        print(f"Followers Count: {user['followersCount']}")
        print()

    exploring = True
    while exploring:
        try:
            continue_exploring = int(input("Enter a specific number of the user that you would like to or press 0 to not explore: "))
            if continue_exploring == 0:
                exploring = False
                return
            if continue_exploring > 0 and continue_exploring <= len(aggregated_users):
                username = aggregated_users[continue_exploring - 1]['_id']
                user = db['tweets'].find_one({"user.username": username})
                print()
                #print all of the users data    
                print(f"Display Name: {user['user']['displayname']}")
                print(f"User Name: {user['user']['username']}")
                print(f"ID: {user['user']['id']}")
                print(f"Description: {user['user']['rawDescription']}")
                print(f"Description URLs: {user['user']['descriptionUrls']}")
                print(f"Verified: {user['user']['verified']}")
                print(f"Created: {user['user']['created']}")
                if user['user']['location'] == '':
                    print("Location: N/A")
                else:
                    print(f"Location: {user['user']['location']}")
                print()
                print(f"Follower Count: {user['user']['followersCount']}")
                print(f"Friends Count: {user['user']['friendsCount']}")
                print(f"Statuses Count: {user['user']['statusesCount']}")
                print(f"Favourites Count: {user['user']['favouritesCount']}")
                print(f"Listed Count: {user['user']['listedCount']}")
                print(f"Media Count: {user['user']['mediaCount']}")
                print(f"Link URL: {user['user']['linkUrl']}")
                print(f"LinkTcourl: {user['user']['linkTcourl']}")
                print(f"Profile Image URL: {user['user']['profileImageUrl']}")
                print(f"Banner URL: {user['user']['profileBannerUrl']}")
                print(f"URL: {user['user']['url']}")
            else:
                print("That user is not available! ")
        except ValueError:
            print("That is not a valid input. Please enter a valid number")

def compose_tweet(db):
    try:
        tweet_content = input("Compose your tweet: ")

        # Prepare the tweet document
        new_tweet = {
            "url": None,
            "date": datetime.utcnow().isoformat(),
            "content": tweet_content,
            "renderedContent": None,
            "id": None,
            "user": {
                "username": "291user",
                "displayname": None,
                "id": None,
                "description": None,
                "rawDescription": None,
                "descriptionUrls": [],
                "verified": False,
                "created": None,
                "followersCount": None,
                "friendsCount": None,
                "statusesCount": None,
                "favouritesCount": None,
                "listedCount": None,
                "mediaCount": None,
                "location": None,
                "protected": False,
                "linkUrl": None,
                "linkTcourl": None,
                "profileImageUrl": None,
                "profileBannerUrl": None,
                "url": None
            },
            "outlinks": [],
            "tcooutlinks": [],
            "replyCount": 0,
            "retweetCount": 0,
            "likeCount": 0,
            "quoteCount": 0,
            "conversationId": None,
            "lang": None,
            "source": None,
            "sourceUrl": None,
            "sourceLabel": None,
            "media": None,
            "retweetedTweet": None,
            "quotedTweet": None,
            "mentionedUsers": None
        }

        # Insert the tweet into the database
        db['tweets'].insert_one(new_tweet)

        print("\nTweet successfully composed and inserted!")

    except Exception as e:
        print(f"Error composing tweet: {e}")

def display_menu():
    print("\nMain Menu:")
    print("1. Search Tweets")
    print("2. Search Users")
    print("3. List Top Tweets")
    print("4. List Top Users")
    print("5. Compose a Tweet")
    print("6. Exit")

def main():
    if len(sys.argv) != 2:
        print("Usage: python program.py <mongodb_port>")
        sys.exit(1)

    port_number = sys.argv[1] # Port number as command line arg
    db = connect_to_mongodb(port_number)

    while True: # Main loop
        display_menu()
        choice = input("\nEnter your choice: (1/2/3/4/5/6) ")

        if choice == '1':
            search_tweets(db)
        elif choice == '2':
            search_users(db)
        elif choice == '3':
            list_top_tweets(db)
        elif choice == '4':
            list_top_users(db)
        elif choice == '5':
            compose_tweet(db)
        elif choice == '6':
            print("\nExited Successfully.")
            break
        else:
            print("\nInvalid choice. Please try again.")

if __name__ == '__main__':
    main()