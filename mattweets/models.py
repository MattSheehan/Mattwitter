# COPYRIGHT Matt Sheehan 2020
import random
from django.conf import settings
from django.db import models
'''
    *~*~* models *~*~*
    Excel spreadsheet idea: we're creating the column names in our db.

    Edit or create model:
    $ ./manage.py makemigrations
    Commit changes to database
    $ ./manage.py migrate
'''

# User model referencing built-in django feature
User = settings.AUTH_USER_MODEL


class Tweet(models.Model):
    #   id = models.AutoField(primary_key=True)
    # many users can have many tweets relationship
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # Tweet content
    content = models.TextField(blank=True, null=True)
    # path to image NOT actual image
    image = models.FileField(upload_to='images/', blank=True, null=True)

    # ordering meta class
    class Meta:
        ordering = ['-id']

    # return Tweet object content
    def __str__(self):
        return self.content

    # serialize data keeps data consistent
    def serialize(self):
        return {
            "id": self.id,
            "content": self.content,
            "likes": random.randint(0, 1000)
        }
