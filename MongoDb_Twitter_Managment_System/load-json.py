import json
import pymongo
from pymongo import MongoClient
import sys

MAX_SIZE = 5000 #For reading and inserting JSON into chunks

def connect_to_mongodb(port_number):

    client = MongoClient('localhost', int(port_number))
    db = client['291db']
    return db

def create_tweets_collection(db):

    if 'tweets' in db.list_collection_names():
        db['tweets'].drop()
    return db['tweets']

def load_json_file(file_name, tweets_collection):

    with open(file_name, 'r') as file:
        tweets_to_insert = []

        for line in file:
            tweet = json.loads(line)
            tweets_to_insert.append(tweet)

            if len(tweets_to_insert) >= MAX_SIZE: # Read and Insert in chunks 
                tweets_collection.insert_many(tweets_to_insert) #inserting list of json lines
                tweets_to_insert = []

        if tweets_to_insert:  # Insert any remaining tweets
            tweets_collection.insert_many(tweets_to_insert)

def main():
    if len(sys.argv) != 3:
        print("Usage: python load-json.py <json_file_name> <mongodb_port>") 
        sys.exit(1)

    file_name = sys.argv[1]  #JSON File command line arg
    port_number = sys.argv[2]  #Port number command line arg

    db = connect_to_mongodb(port_number)
    tweets_collection = create_tweets_collection(db)
    load_json_file(file_name, tweets_collection)

if __name__ == '__main__':
    main()