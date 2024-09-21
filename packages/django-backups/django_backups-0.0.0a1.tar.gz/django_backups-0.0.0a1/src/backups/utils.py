import psycopg2
import subprocess
import os
from datetime import datetime
import boto3


def check_connection(db_host, db_user, db_password, db_port, db_name):
    try:
        connection = psycopg2.connect(database=db_name, user=db_user, password=db_password, host=db_host, port=db_port, connect_timeout=3)
        cursor = connection.cursor()
        return True
    except Exception as e:
        return False

def get_server_databases(db_host, db_user, db_password, db_port, db_name):
    os.environ['PGPASSWORD'] = db_password
    full_command = f"""psql -t -c "SELECT datname FROM pg_database WHERE datdba = (SELECT oid FROM pg_roles WHERE rolname = \'{db_user}\'); " -h {db_host} -p {db_port} -U {db_user} -d {db_name}"""  # | grep '\\S'"""
    databases = subprocess.check_output(full_command, shell=True, executable='bash').decode().split('\n')
    databases = [i.strip() for i in databases if i != '']
    return databases

def get_database_tables(db_host, db_user, db_password, db_port, db_name):
    os.environ['PGPASSWORD'] = db_password
    full_command = f"""psql -t -c "\\dt" -h {db_host} -p {db_port} -U {db_user} -d {db_name} -P pager=off"""
    entries = subprocess.check_output(full_command, shell=True, executable='bash').decode().split('\n')
    tables = [i.split('|')[1].strip() for i in entries if i != '' and '|' in i]
    return tables

def generate_presigned_url(file_name, expiration=86400):
    s3_client = boto3.client(
        's3',
        aws_access_key_id=os.getenv('DO_SPACE_ACCESS_KEY_ID'),
        aws_secret_access_key=os.getenv('DO_SPACE_SECRET_ACCESS_KEY'),
        region_name=os.getenv('DO_SPACE_REGION'),
        endpoint_url=os.getenv('DO_SPACE_ENDPOINT_URL'),
    )
    try:
        response = s3_client.generate_presigned_url('get_object',
                                                    Params={
                                                        'Bucket': os.getenv('DO_SPACE_BUCKET_NAME'),
                                                        'Key': file_name
                                                    },
                                                    )
    except Exception as e:
        print(f"Error generating pre-signed URL: {e}")
        return None
    return response


def upload_file_to_do_space(file_obj, file_name):

    s3 = boto3.client(
        's3',
        region_name=os.getenv('DO_SPACE_REGION'),
        endpoint_url=os.getenv('DO_SPACE_ENDPOINT_URL'),
        aws_access_key_id=os.getenv('DO_SPACE_ACCESS_KEY_ID'),
        aws_secret_access_key=os.getenv('DO_SPACE_SECRET_ACCESS_KEY')
    )
    s3.upload_fileobj(
        file_obj,
        os.getenv('DO_SPACE_BUCKET_NAME'),
        file_name,
        ExtraArgs={'ACL': 'private'},
        
    )

    file_url = generate_presigned_url(file_name, expiration=3600)

    return file_url
