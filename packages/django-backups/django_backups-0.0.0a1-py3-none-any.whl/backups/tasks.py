from celery import shared_task
from dotenv import load_dotenv
from datetime import datetime
import os
from .utils import get_server_databases, upload_file_to_do_space
from .models import BackupEntry, ContentType
from django.conf import settings

load_dotenv()

@shared_task
def backup_whole_pg_cluster(db_host, db_port, db_name, db_user, db_password, backup_folder, server_id, server_name, content_type_id, locally=False):
    content_type = ContentType.objects.get(id=content_type_id)
    timestamp = datetime.now().strftime("%m_%d_%H-%M-%S")
    cluster_backup_dir = os.path.join(settings.BACKUP_DIR, f"databases/pg_{timestamp}")
    if not os.path.exists(settings.BACKUP_DIR):
        os.mkdir(settings.BACKUP_DIR)
    if not os.path.exists(os.path.join(settings.BACKUP_DIR, 'databases')):
        os.mkdir(os.path.join(settings.BACKUP_DIR, 'databases'))
    if not os.path.exists(cluster_backup_dir):
        os.mkdir(cluster_backup_dir)
    os.environ['PGPASSWORD'] = db_password
    databases = get_server_databases(db_host, db_user, db_password, db_port, db_name)

    backup_entries_to_save = []

    for database in databases:
        print(database, "in process...")
        os.system(f'pg_dump -h {db_host} -U {db_user} -p {db_port} {database} -F c > {os.path.join(backup_folder, f"srv_{server_name}_{database}___{timestamp}.sql")}')
        with open(os.path.join(backup_folder, f"srv_{server_name}_{database}___{timestamp}.sql"), 'rb') as f:
            file_url = upload_file_to_do_space(f, f"srv_{server_name}_{database}___{timestamp}.sql")

            backup_entry = BackupEntry.objects.create(
                content_type=content_type,
                object_id=server_id,
                file=file_url if not locally else f'get_backup/pg_{timestamp}___{database}_.sql'
            )



@shared_task
def backup_database(db_host, db_port, db_name, db_user, db_password, backup_folder, database_id, content_type_id, locally=False):
    content_type = ContentType.objects.get(id=content_type_id)
    timestamp = datetime.now().strftime("%m_%d_%H-%M-%S")
    if not os.path.exists(backup_folder):
        os.mkdir(backup_folder)
    if not os.path.exists(os.path.join(backup_folder, 'databases')):
        os.mkdir(os.path.join(backup_folder, 'databases'))
    os.environ['PGPASSWORD'] = db_password
    os.system(f'pg_dump -h {db_host} -U {db_user} -p {db_port} {db_name} -F c > {os.path.join(backup_folder, f"pg_{timestamp}___{db_name}_.sql")}')

    with open(os.path.join(backup_folder, f'pg_{timestamp}___{db_name}_.sql'), 'rb') as f:
        print("Uploading")
        file_url = upload_file_to_do_space(f, f'pg_{timestamp}___{db_name}_.sql')
        print("Uploaded")
        BackupEntry.objects.create(
            content_type=content_type,
            object_id=database_id,
            file=file_url if not locally else f'get_backup/pg_{timestamp}___{db_name}_.sql'
        )


