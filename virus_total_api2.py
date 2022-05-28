"""

This script was written following instructions for a potential job opportunity.

Instructions

•	Write a Python or PowerShell script that accepts a file hash value (MD5 or SHA256) from the user and submits the
    hash to VirusTotal via an API call.

•	If VirusTotal finds more than 5 AV engines detected the file as malicious, output a message that informs the user
    and tells them how many AV engines detected the file.

•	If VirusTotal finds that less than 5 AV engines reported the file as malicious, output a message that indicates
    the file may be malicious and tells the user how many AV engines detected the file.

•	If no AV engines indicate the file is malicious, output a message that tells the user that the file is clean.

This script should also:
•	Validate user input to verify that the user has entered a valid hash.
•	Require the user to enter their API information (required to make API calls to VirusTotal).
•	Return an error message if an invalid hash is entered by the user or if they do not input their API information.
•	Output the API call's status code (200, 404, etc.)
•	Inform the user that the API call failed if status code is not 200.

"""

import hashlib
import os
import argparse
import re
from virus_total_apis import PublicApi as VirusTotalPublicApi


def check_hash(input_to_check):
    """ Checks if a valid hash has been provided """

    length_of = len(input_to_check)

    if length_of == 64:
        return re.search(r"([a-fA-F\d]{64})", input_to_check)
    elif length_of == 32:
        return re.search(r"([a-fA-F\d]{32})", input_to_check)
    else:
        if '\\' not in input_to_check and '/' not in input_to_check and '.' not in input_to_check:
            print("\n(+) You entered an invalid hash. Please check the hash and try again.")
        return None


def check_api_key(api_key_to_check):
    """ Ensures the API key is in the right format """

    length_of = len(api_key_to_check)

    if length_of == 64:
        return re.search(r"([a-fA-F\d]{64})", api_key_to_check)


def hash_file(file_path):
    """ Hashes the file if given a file path """

    if os.path.isfile(file_path):
        read_file = open(file_path, "rb")
        file_content = read_file.read()
        read_file.close()
        md5_hash = hashlib.md5(file_content).hexdigest()
        print(f'\n(+) The MD5 hash of {file_path} is {md5_hash}\n')
        return md5_hash
    elif "\\" in file_path or "/" in file_path:
        print(f'\n(+) Error: The file {file_path} does not exist.\n')
        return None
    else:
        return None


def upload_hash(key_to_check, hash_to_check):
    """ Uploads the hash to Virus Total """

    vt = VirusTotalPublicApi(key_to_check)
    response = vt.get_file_report(hash_to_check)

    if response["response_code"] != 200:
        print(f'\n(+) API call failed with status code {response["response_code"]}. Check your API key.')

    else:
        print(f'\n(+) Status Code: {response["response_code"]}\n')
        print(f'\n(+) Results for the {hash_to_check} hash value...\n')

        if response["results"]["response_code"] == 0:
            print("\nThis file has not been uploaded to Virus Total yet. This means it could be benign or"
                  " malicious. If it is malicious, it is either new or unique. Further analysis may be needed.\n")
        else:
            positives = response["results"]["positives"]

            if positives > 5:
                print(f'\nThis file is malicious. {positives} AV engines detected the file as malicious.\n')
            elif positives > 0:
                print(f'\nIt is possible that this file is malicious. {positives} AV engines detected the'
                      f' file as malicious.\n')
            else:
                print("\nNo AV engines detected the file as malicious. The file is clean.\n")


def missing_arguments(missing_args_api_key):
    """ Prompts the user for information if script is run without arguments """

    user_input = input("Enter either a valid SHA256 or MD5 hash or the path to the file you want to"
                       " upload to Virus Total: ")

    print()

    is_hash = check_hash(user_input)

    if is_hash:
        upload_hash(missing_args_api_key, user_input)
    else:
        no_args_file_hash = hash_file(user_input)
        if no_args_file_hash:
            upload_hash(missing_args_api_key, no_args_file_hash)


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Upload an MD5 or SHA256 hash to Virus Total for analysis.')

    parser.add_argument("-s", "--hash", type=str, required=False, help="The MD5 or SHA256 hash you want to upload to"
                                                                       " Virus Total.")
    parser.add_argument("-k", "--key", type=str, required=False, help="Your Virus Total API key.")
    parser.add_argument("-f", "--file", type=str, required=False, help="The full path of the file you want to hash"
                                                                       " and upload.")

    args = parser.parse_args()
    hash_string = args.hash
    api_key = args.key
    full_path = args.file

    while not api_key:
        api_key = input("\nEnter your Virus Total API key: ")
        print()

    check_api_key = check_api_key(api_key)

    if check_api_key:

        if full_path:
            file_hash = hash_file(full_path)
            if file_hash:
                upload_hash(api_key, file_hash)

        if hash_string:
            valid_hash = check_hash(hash_string)
            if valid_hash:
                upload_hash(api_key, hash_string)

        if not full_path and not hash_string:
            missing_arguments(api_key)
    else:
        print("\n(+) You entered an invalid API key. Check Virus Total again for correct API key.")
