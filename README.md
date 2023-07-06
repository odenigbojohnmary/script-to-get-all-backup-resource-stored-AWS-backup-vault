# script-to-get-all-backup-resource-stored-AWS-backup-vault
This script fetches all the resources in your AWS Backup Vault.
You can filter and fetch the resources based on specific date range.
It will also delete all the resources filter.

Comment out the delete script if you only want to fetch the details and save in Csv format.

# Pre-requisites Installation

Install latest version of python

Install packages:

Clone the repo

Create a virtual environment in project directory and activate it. Documentation (https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/#creating-a-virtual-environmention)

Run following command to install packages

pip3 install -r requirements.txt

Generate an AWS ACCE KEY and SECRET KEY and replace with the values in the file.

Run with command
python3 delete_backups.py