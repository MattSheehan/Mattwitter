# COPYRIGHT Matt Sheehan 2020
from django.db import models
'''
    *~*~* models *~*~*
    Excel spreadsheet idea: we're creating the column names in our db.
    
    Edit or create model:
    $ ./manage.py makemigrations
    Commit changes to database
    $ ./manage.py migrate
'''
class Tweet(models.Model):
#   id = models.AutoField(primary_key=True)
    content = models.TextField(blank=True, null=True)
    # path to image NOT actual image
    image = models.FileField(upload_to='images/', blank=True, null=True)