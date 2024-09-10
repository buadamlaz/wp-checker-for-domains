import requests
import csv
import re
from bs4 import BeautifulSoup
from tqdm import tqdm
import argparse
#
# @buadamlaz - Wordpress Checker for Domains - 10.09.2024
#

# Check WordPress version from meta tags
def get_wordpress_version_from_meta(domain):
    try:
        url = f"http://{domain}"
        response = requests.get(url, timeout=5)

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            meta_tag = soup.find('meta', attrs={'name': 'generator'})
            if meta_tag and 'WordPress' in meta_tag.get('content', ''):
                return meta_tag.get('content')  # Örnek: "WordPress 6.4.3"
    except requests.exceptions.RequestException:
        return None
    return None

# Check WordPress version at /feed/ url
def get_wordpress_version_from_feed(domain):
    try:
        url = f"http://{domain}/feed/"
        response = requests.get(url, timeout=5)

        if response.status_code == 200:
            match = re.search(r'<generator>https://wordpress.org/\?v=(\d+\.\d+\.\d+)</generator>', response.text)
            if match:
                return f"WordPress {match.group(1)}"  # Örnek: "WordPress 6.4.3"
    except requests.exceptions.RequestException:
        return None
    return None

# Function that checks WordPress (gets version information via meta and feed)
def check_wordpress_version(domain):
    version = get_wordpress_version_from_meta(domain)
    if not version:
        version = get_wordpress_version_from_feed(domain)
    return version

# Function that checks domains and saves results to CSV
def check_domains(input_file, output_file, version_info):
    with open(input_file, 'r') as file:
        domains = [line.strip() for line in file.readlines()]
    
    wordpress_sites = 0
    non_wordpress_sites = 0

    with open(output_file, 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        if version_info:
            csvwriter.writerow(['URL', 'WordPress', 'Version'])  # Başlık satırı
        else:
            csvwriter.writerow(['URL', 'WordPress'])  # Başlık satırı

        # A for loop wrapped with tqdm for the progress bar
        for domain in tqdm(domains, desc="Checking Domains", unit="domain"):
            domain = domain.strip()
            if domain and is_valid_domain(domain):
                if version_info:
                    version = check_wordpress_version(domain)
                    if version:
                        csvwriter.writerow([domain, 'YES', version])
                        wordpress_sites += 1
                    else:
                        csvwriter.writerow([domain, 'NO', 'N/A'])
                        non_wordpress_sites += 1
                else:
                    version = check_wordpress_version(domain)
                    if version:
                        csvwriter.writerow([domain, 'YES'])
                        wordpress_sites += 1
                    else:
                        csvwriter.writerow([domain, 'NO'])
                        non_wordpress_sites += 1
    
    print(f"{wordpress_sites} WordPress sites")
    print(f"{non_wordpress_sites} sites are not WordPress")

# More flexible domain validation (supports all domain extensions)
def is_valid_domain(domain):
    pattern = r'^(?!-)[A-Za-z0-9-]{1,63}(?<!-)\.[A-Za-z]{2,}\.?[A-Za-z]{0,6}$'
    return re.match(pattern, domain)

# Using argparse to process command line arguments
def main():
    parser = argparse.ArgumentParser(description="WordPress Site Checker")
    parser.add_argument('-d', '--domains', required=True, help="Path to domain list in TXT file")
    parser.add_argument('-o', '--output', required=True, help="Path to CSV file where results are saved")
    parser.add_argument('--version', action='store_true', help="With version information")

    args = parser.parse_args()

    check_domains(args.domains, args.output, args.version)

if __name__ == '__main__':
    main()
