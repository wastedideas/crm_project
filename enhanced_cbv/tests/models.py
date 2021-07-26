from django.db import models


class Author(models.Model):
    name = models.CharField(max_length=255)

    def __unicode__(self):
        return self.name


class Article(models.Model):
    title = models.CharField(max_length=255)
    pub_date = models.DateField()
    author = models.ForeignKey(Author, blank=True, null=True)
