import requests
from azure.storage.blob import BlobServiceClient

# Your Facebook App's credentials
APP_ID = ''
APP_SECRET = ''
SHORT_LIVED_TOKEN = ''

try:
    # Construct the URL for token exchange
    url = f"https://graph.facebook.com/v13.0/oauth/access_token?" \
          f"grant_type=fb_exchange_token&" \
          f"client_id={APP_ID}&" \
          f"client_secret={APP_SECRET}&" \
          f"fb_exchange_token={SHORT_LIVED_TOKEN}"

    # Make a GET request to exchange the token
    response = requests.get(url)
    data = response.json()

    if 'access_token' in data:
        long_lived_token = data['access_token']
    else:
        print("Error exchanging token. Check your credentials and token.")

except Exception as e:
    print(f"An error occurred: {e}")

# Create a BlobServiceClient using the connection string
connection_string = ""
blob_service_client = BlobServiceClient.from_connection_string(connection_string)

# Azure Blob Storage container and blob details
container_name = "processed/output"
blob_name = "long_lived_access_token.csv"

# Convert the long-lived token to bytes
csv_content = long_lived_token.encode('utf-8')

# Get a container client and upload the CSV content to the blob
container_client = blob_service_client.get_container_client(container_name)
blob_client = container_client.get_blob_client(blob_name)
blob_client.upload_blob(csv_content, overwrite=True)
