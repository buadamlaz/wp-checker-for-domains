
# WordPress Checker for Domains

WordPress Site Checker is a Python script that scans a list of domains to determine if they are powered by WordPress. 

The script can optionally retrieve and report the WordPress version if specified. Results are output to a CSV file, providing a clear indication of which sites are using WordPress and their version details.

## How to Use? 
 It works with just **3 simple parameters**.

+ **-d <domain_list.txt>:** Path to the TXT file containing the list of domains to check.
+ **-o <output_file.csv>:** Path to the CSV file where results will be saved.
+ **--version (optional):** Include WordPress version information in the output.


**Example Without Version Information:**
```bash 
  python wp-checker.py -d domains.txt -o scan_result.csv
```
**Example With Version Information:**
```bash 
  python wp-checker.py -d domains.txt -o scan_result.csv --version
```

## Required Libraries:
The libraries and installation commands required for this script to work are listed below,
```
pip install requests beautifulsoup4 tqdm
```
