from google.cloud import storage

def upload_to_gcs(bucket_name, source_file_path, destination_blob_name, credentials_file):
    # Initialize the Google Cloud Storage client with the credentials
    storage_client = storage.Client.from_service_account_json(credentials_file)

    # Get the target bucket
    bucket = storage_client.bucket(bucket_name)

    # Upload the file to the bucket
    blob = bucket.blob(destination_blob_name)
    blob.upload_from_filename(source_file_path)

    print(f"File {source_file_path} uploaded to gs://{bucket_name}/{destination_blob_name}")

def get_string_from_blob(bucket_name, source_blob_name, credentials_file):
    # Initialize the Google Cloud Storage client with the credentials
    storage_client = storage.Client.from_service_account_json(credentials_file)

    # Get the source bucket
    bucket = storage_client.bucket(bucket_name)

    # Get the source blob
    blob = bucket.blob(source_blob_name)

    return blob.download_as_text()

def get_all_blobs(bucket_name, credentials_file):
    # Initialize the Google Cloud Storage client with the credentials
    storage_client = storage.Client.from_service_account_json(credentials_file)

    blobs = storage_client.list_blobs(bucket_name)
    sorted_blobs = sorted(blobs, key=lambda blob: blob.time_created)
    return sorted_blobs

def get_most_recent_blob(bucket_name, credentials_file):
    # Initialize the Google Cloud Storage client with the credentials
    sorted_blobs = get_all_blobs(bucket_name, credentials_file)
    return sorted_blobs[-1]

def check_blob_existence(bucket_name, blob_name, credentials_file):
    storage_client = storage.Client.from_service_account_json(credentials_file)
    
    # Get the bucket
    bucket = storage_client.bucket(bucket_name)
    
    # Check if the blob exists
    blob = bucket.blob(blob_name)
    return blob.exists()