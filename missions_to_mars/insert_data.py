import pymongo
from scrape_mars import mars_data

# Set up Mongo Connection / DB
conn = 'mongodb://localhost:27017'
client = pymongo.MongoClient(conn)

# Recreate DB without Duplicates
mars_db = client.mars_db

# Drops collection if available to remove duplicates
mars_db.items.drop()

# Create Collection again
collection = mars_db.items

# Add to Mongo # 
collection.insert_one(mars_data)