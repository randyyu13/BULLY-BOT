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

def get_string_from_gcs_bucket(bucket_name, source_blob_name, credentials_file):
    # Initialize the Google Cloud Storage client with the credentials
    storage_client = storage.Client.from_service_account_json(credentials_file)

    # Get the source bucket
    bucket = storage_client.bucket(bucket_name)

    # Get the source blob
    blob = bucket.blob(source_blob_name)

    return blob.download_as_text()