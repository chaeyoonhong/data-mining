from django.db import models

class KeywordTable(models.Model):
    idkeyword_table = models.AutoField(primary_key=True)
    type = models.CharField(max_length=45)
    site = models.CharField(max_length=45)
    keyword = models.CharField(max_length=45)
    date = models.DateField()
    count = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'keyword_table'

