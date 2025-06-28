from pymongo import MongoClient
import sys
sys.stdout.reconfigure(encoding='utf-8')

uri = "mongodb+srv://test:test@venkatesh.nvutauw.mongodb.net/?retryWrites=true&w=majority&appName=venkatesh"

client = MongoClient(
    uri,
    tls=True,
    tlsCAFile="C:/Users/venka/OneDrive/Documents/AJ/New folder (2)/log page/isrgrootx1.pem"
)

try:
    print(client.server_info())
    print("✅ Connection successful!")
except Exception as e:
    print("❌ Connection error:", e)
