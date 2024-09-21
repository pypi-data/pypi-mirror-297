from django.db import models
import psycopg2
from .utils import check_connection
from django.core.exceptions import ValidationError
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

class Server(models.Model):
    host = models.CharField(max_length=256, null=False, blank=False)
    default_db_name = models.CharField(max_length=128, default="defaultdb", null=False, blank=False)
    db_user = models.CharField(max_length=256, null=False, blank=False)
    db_password = models.CharField(max_length=256, null=False, blank=False)
    db_port = models.CharField(max_length=256, null=False, blank=False)
    is_accessible = models.BooleanField(default=True, null=False, blank=False)
    last_accessed = models.DateTimeField(auto_now_add=True, null=False, blank=False)
    name = models.CharField(max_length=64, default="default_server", null=False, blank=False)

    def save(self, *args, **kwargs):
        if not check_connection(
            db_host=self.host,
            db_user=self.db_user,
            db_password=self.db_password,
            db_port=self.db_port,
            db_name=self.default_db_name
        ):
            raise ValidationError("can't establish connection")

        super(Server, self).save(*args, **kwargs)


class Database(models.Model):
    server = models.ForeignKey(Server, on_delete=models.CASCADE, related_name='databases')
    db_host = models.CharField(max_length=256, null=False, blank=False)
    db_name = models.CharField(max_length=256)
    db_user = models.CharField(max_length=256, null=False, blank=False)
    db_password = models.CharField(max_length=256, null=False, blank=False)
    db_port = models.CharField(max_length=256, null=False, blank=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['server', 'db_name'], name='unique_server_db_name_combination'
            )
        ]

    def __str__(self):
        return f"{self.db_name} | {self.server.name}"

class Table(models.Model):
    database = models.ForeignKey(Database, on_delete=models.CASCADE, related_name='tables')
    name = models.CharField(max_length=256)


class BackupEntry(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")

    file = models.FileField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Backup of {self.content_object} created at {self.created_at}"


