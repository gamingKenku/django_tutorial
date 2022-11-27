from django.db import models


class BaseModel(models.Model):
    objects = models.Manager()

    class Meta:
        abstract = True


class Book(BaseModel):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=50)
    author = models.CharField(max_length=50)
    release_date = models.DateField()
    price = models.FloatField()

    class Meta:
        db_table = 'book'
