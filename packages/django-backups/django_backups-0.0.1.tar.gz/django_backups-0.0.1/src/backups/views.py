from django.shortcuts import render
from django.http.response import FileResponse
import os
from django.conf import settings


def get_backup(request, file_name):
    full_file_path = os.path.join(settings.BACKUP_DIR, file_name)
    return FileResponse(open(full_file_path, 'rb'), as_attachment=True, filename=(os.path.basename(file_name)))


# def get_file_dynamic_url(request, file_name):
