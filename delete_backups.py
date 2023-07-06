import boto3
from time import sleep
# import datetime
from datetime import datetime
import csv

AWS_ACCESS_KEY_ID="xxxxxxxxx" 
AWS_SECRET_ACCESS_KEY="xxxxxxxx"

def get_recovery_points(vault_name: str ) -> list:
    pagination = True
    restore_points = []
    timestamp = str(datetime.now())
    file_name = f"report_{timestamp}.csv"
    session = boto3.session.Session(
    region_name="us-east-1",
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
)
    b = session.client('backup')

    res = b.list_recovery_points_by_backup_vault(
        BackupVaultName=vault_name,
        ByCreatedBefore=datetime(2023, 3, 1),
        MaxResults=500
    )

    while pagination:
        with open(file_name, 'a', newline='') as file:
            writer = csv.writer(file)
            field = [
                "Resource Arn",
                "Status",
                "Resource Type",
                "Backup Type",
                "Creation Date",
                "Completion Date"
            ]
            writer.writerow(field)
            for point in res['RecoveryPoints']:
                if point['ResourceType'] == 'EC2':
                    point['BackupType'] = "Image"
                elif point['ResourceType'] == 'EFS':
                    point['BackupType'] = "Backup"    
                else:
                    point['BackupType'] = "Snapshot"
                writer.writerow([point['RecoveryPointArn'], point['Status'], point['ResourceType'], point['BackupType'], point['CreationDate'], point['CompletionDate']])
                restore_points.append(point['RecoveryPointArn'])
            if 'NextToken' in res:
                res = b.list_recovery_points_by_backup_vault(
                    BackupVaultName=vault_name,
                    ByCreatedBefore=datetime(2023, 3, 1),
                    MaxResults=500,
                    NextToken=res['NextToken'],
                )
            else:
                pagination = False
    print('CSV file %s created.' % file_name)
    return restore_points


def delete_recovery_points(vault_name: str, point_arn_list: list) -> bool:
    session = boto3.session.Session(
    region_name="us-east-1",
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    )
    b = session.client('backup')

    for index, point in enumerate(point_arn_list):
        print(f'[.] Deleting recovery point "{point}" [{index} / {len(point_arn_list)}]')
        res = b.delete_recovery_point(
            BackupVaultName=vault_name,
            RecoveryPointArn=point
        )
        sleep(1)

    return True

if __name__ == '__main__':
    vault_name = "Default"
    recovery_points = get_recovery_points(vault_name)
    print(f'[+] Found {len(recovery_points)} recovery points! Deleting them!')
    delete_recovery_points(vault_name, recovery_points)