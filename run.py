from accounts_generator import OutlookAccountGenerator
from accounts_generator import InstagramAccountGenerator
import argparse
import json


def generate_email(data=None):
    # Your code to generate an email
    account_generator = OutlookAccountGenerator(use_proxy=False)
    account_details = account_generator.create_account(data)
    account_generator.save_account_details(account_details)
    account_generator.close_driver()
    return

def generate_instagram_account(data=None):
    # Your code to generate an Instagram account
    account_generator = InstagramAccountGenerator(use_proxy=False)
    account_details = account_generator.create_account(data)
    account_generator.save_account_details(account_details)
    account_generator.close_driver()
    return

def read_json_file(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

def parse_args():
    parser = argparse.ArgumentParser(description='Read JSON file and return data as dictionary')
    parser.add_argument('-a', '--account', type=str, help='Account type to create (email/insta)')
    parser.add_argument('-j', '--json', type=str, help='Path to the JSON file')
    args = parser.parse_args()
    return args

def main():
    args = parse_args()

    if args.account and args.account == 'insta':
        data = read_json_file(args.json) if args.json else None
        generate_instagram_account(data)
        return

    data = read_json_file(args.json) if args.json else None
    generate_email(data)

if __name__ == "__main__":
    main()
