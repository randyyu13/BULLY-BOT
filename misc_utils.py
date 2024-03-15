from gcp_proxy import *
import os

def write_array_to_file(array, filename):
    with open(filename, 'w') as file:
        for item in array:
            file.write(str(item) + '\n')
    upload_to_gcs('plays-bucket', filename, filename, "google-credentials.json")
    os.remove(filename)

