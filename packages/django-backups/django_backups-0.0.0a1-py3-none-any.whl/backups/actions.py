from django.contrib import admin, messages
from .models import Server, Database, Table, BackupEntry
from .utils import check_connection, get_server_databases, get_database_tables
from .tasks import backup_whole_pg_cluster, backup_database
from django.conf import settings
from django.utils.html import format_html
from django.contrib.contenttypes.models import ContentType

@admin.action(description='check server connection')
def update_connection_status(modeladmin, request, queryset):
    values = queryset.values()[0]
    if check_connection(
        values['host'],
        values['db_user'],
        values['db_password'],
        values['db_port'],
        values['default_db_name'],
    ):
        queryset.update(is_accessible=True)
    else:
        queryset.update(is_accessible=False)

@admin.action(description='get server databases')
def update_server_databases(modeladmin, request, queryset):
    databases_to_create = []
    for server in queryset:
        databases = get_server_databases(
            server.host,
            server.db_user,
            server.db_password,
            server.db_port,
            server.default_db_name
        )
        for database in databases:
            databases_to_create.append(Database(server=server,
                                                db_name=database,
                                                db_host=server.host,
                                                db_user=server.db_user,
                                                db_password=server.db_password,
                                                db_port=server.db_port))
    Database.objects.bulk_create(databases_to_create, ignore_conflicts=True)
    messages.info(request, "Updated databases for selected servers ")

@admin.action(description='Backup all databases')
def backup_server_databases(modeladmin, request, queryset):
    content_type = ContentType.objects.get_for_model(Server)
    for server in queryset:
        args = (
            server.host,
            server.db_port,
            server.default_db_name,
            server.db_user,
            server.db_password,
            str(settings.BACKUP_DIR),
            server.id,
            server.server_name,
            content_type.id
        )
        
        if hasattr(settings, 'CELERY_BROKER_URL'):
            backup_whole_pg_cluster.delay(*args)
        else:
            backup_whole_pg_cluster(*args)

    messages.info(request, "Backup for selected servers has started...")

@admin.action(description='Update all tables')
def update_database_tables(modeladmin, request, queryset):
    tables_to_create = []
    for database in queryset:
        tables = get_database_tables(
            database.db_host,
            database.db_user,
            database.db_password,
            db_port=database.db_port,
            db_name=database.db_name)
        for table in tables:
            tables_to_create.append(Table(database=database, name=table))
    Table.objects.bulk_create(tables_to_create, ignore_conflicts=True)
    messages.info(request, "Updated tables for selected the databases")


@admin.action(description='Backup database')
def backup_databases(modeladmin, request, queryset):
    content_type = ContentType.objects.get_for_model(Database)
    for database in queryset:
        args = (
            database.db_host,
            database.db_port,
            database.db_name,
            database.db_user,
            database.db_password,
            str(settings.BACKUP_DIR),
            database.id,
            content_type.id
        )
        if hasattr(settings, 'CELERY_BROKER_URL'):
            backup_database.delay(
                *args
            )
        else:
            backup_database(*args)
    messages.info(request, "Backup for selected databases has started...")

