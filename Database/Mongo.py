from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

uri = "mongodb+srv://tranduythuc2003:jsTp9zHUrDejvmDO@cluster.rxxscwr.mongodb.net/?retryWrites=true&w=majority&appName=Cluster"

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    db = client.get_database('Leaf')

except Exception as e:
    print(e)