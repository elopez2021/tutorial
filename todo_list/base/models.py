from django.db import models
from django.contrib.auth.models import User 
'''import the built-in django user to use it as a foreign key in the user field'''


# Create your models here.

class Task(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=200)
    description = models.TextField(null=True,blank=True)
    complete = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True) 

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['complete'] 
        '''this means that is going to be order by the complete field. Any complete items should be sent to the bottom of the list because they're done we don't need to focus on those anymore'''