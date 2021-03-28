from django.db import models
from django.contrib.auth.models import User


class Document(models.Model):
    document_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    file = models.FileField(null=True)
    owner_username = models.CharField(max_length=150)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    deleted = models.BooleanField(default=False)
    users = models.ManyToManyField(User)


class UserDocumentMapping(models.Model):
    user_document_mapping_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    document = models.ForeignKey(Document, on_delete=models.CASCADE)


