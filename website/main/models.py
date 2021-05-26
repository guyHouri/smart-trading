"""
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")

import django
django.setup()

from django.core.management import call_command
"""

from django.db import models
#from django_pandas.managers import DataFrameManager

"""
class MyModel(models.Model):
    figure = MatplotlibFigureField(figure='my_figure')


class Product(models.Model):
    product_name=models.TextField()
    objects = models.Manager()
    #pdobjects = DataFrameManager()  # Pandas-Enabled Manager 
"""