from django.contrib import admin, messages
from .models import Server, Database, Table, BackupEntry
from .actions import *
from django.utils.html import format_html

class ServerInline(admin.TabularInline):
    model = Database

class DatabaseInline(admin.TabularInline):
    model = Table

class ServerAdmin(admin.ModelAdmin):
    list_display = ['host', 'is_accessible']
    ordering = []
    inlines = [ServerInline]
    actions = [update_connection_status, update_server_databases, backup_server_databases]

class DatabaseAdmin(admin.ModelAdmin):
    list_display = ['db_name', 'server_id']
    ordering = []
    inlines = [DatabaseInline]
    actions = [update_database_tables, backup_databases]

class BackupEntryAdmin(admin.ModelAdmin):
    list_display = ['get_content_type_model', 'get_url']

    def get_url(self, obj):
        return format_html(f"""<a href="{obj.file}">{obj.file}</a>""")
    
    def get_content_type_model(self, obj):
        return f"{obj.content_type.model} | {obj.object_id}" if obj.content_type else 'None'
    get_content_type_model.short_description = 'Content Type Model'


class TableAdmin(admin.ModelAdmin):
    list_display = ['name', 'database']
    ordering = []
    actions = [update_database_tables]

admin.site.register(ContentType)
admin.site.register(Table, TableAdmin)
admin.site.register(Server, ServerAdmin)
admin.site.register(Database, DatabaseAdmin)
admin.site.register(BackupEntry, BackupEntryAdmin)

