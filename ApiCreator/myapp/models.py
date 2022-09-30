from django.db import models

class Modelnames(models.Model):
    modelname = models.CharField(max_length=100)

    def __str__(self):
        return modelname