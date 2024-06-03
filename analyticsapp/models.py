from django.db import models

# Create your models here.
class CSVfile(models.Model):
    file=models.FileField(upload_to='csvs/')
    uploaded_at=models.DateTimeField(auto_now_add=True)