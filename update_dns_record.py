import requests
import json
import time
import os
import logging
from dotenv import load_dotenv

load_dotenv()


# Get the current public IP address
def get_public_ip():
    response = requests.get('https://api.ipify.org?format=json')
    return json.loads(response.text)['ip']


# Update the DNS record on Cloudflare
def update_dns_record(domain_name, ip_address, record_id):
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {api_key}'
    }

    data = {
        'type': 'A',
        'name': domain_name,
        'content': ip_address
    }
    url = f'https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records/{record_id}'
    response = requests.patch(url, headers=headers, json=data)

    if response.status_code == 200:
        logging.info(f'DNS record updated for {domain_name}')
    else:
        logging.error(f'Error updating DNS record for {domain_name}')


def get_dns_record_id():
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {api_key}'
    }

    url = f'https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records/'
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        list_record = response.json()["result"]
        return get_id_by_name(list_record, domain_names)
    else:
        logging.error(f'Error get DNS record for {zone_id}')


def get_id_by_name(dns_dict, names):
    records = []
    for name in names:
        for dns_data in dns_dict:
            if dns_data['name'] == name:
                records.append({'id': dns_data['id'], 'name': name})
    return records


# Get the domain names, zone ID, and API key from environment variables
domain_names = os.getenv('DOMAIN_NAMES').split(',')
zone_id = os.getenv('ZONE_ID')
api_key = os.getenv('API_KEY')
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Run the script every hour
while True:
    dns_records = get_dns_record_id()
    ip = get_public_ip()
    for record in dns_records:
        update_dns_record(record["name"], ip, record["id"])
    time.sleep(3600)  # wait for an hour before running the script again
