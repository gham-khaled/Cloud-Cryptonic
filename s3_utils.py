import os

import boto3

from keys import load_key_from_file, encrypt_file, decrypt_file, list_keys

s3 = boto3.client("s3")


def upload_encrypted_file_to_s3(bucket_name, input_file, s3_object_key, key_name):
    if not key_name:
        return s3.upload_file(
            Filename=input_file,
            Bucket=bucket_name,
            Key=s3_object_key
        )

    # If Encrypted
    key = load_key_from_file(key_name)
    encrypted_filename = input_file + "_encrypted"

    encrypt_file(input_file, encrypted_filename, key)

    s3.upload_file(
        Filename=encrypted_filename,
        Bucket=bucket_name,
        Key=s3_object_key,
        ExtraArgs={"Tagging": f"encrypted={key_name}"}
    )

    os.remove(encrypted_filename)


def download_and_decrypt_file_from_s3(bucket_name, s3_object_key, output_file):
    # Download the object
    response = s3.get_object_tagging(Bucket=bucket_name, Key=s3_object_key)
    tags = {tag["Key"]: tag["Value"] for tag in response["TagSet"]}
    print(tags)
    key_name = tags.get("encrypted", None)
    if not key_name or key_name not in list_keys():
        return s3.download_file(bucket_name, s3_object_key, output_file)
    key = load_key_from_file(key_name)
    encrypted_file = output_file + "_encrypted"
    s3.download_file(bucket_name, s3_object_key, encrypted_file)
    decrypt_file(encrypted_file, output_file, key)
    os.remove(encrypted_file)
