from django.contrib import admin
from handler.models import Submission, Recommendations, UserRankings, FinalResult, Recipe, Image
# Register your models here.
admin.site.register(Submission)
admin.site.register(Recipe)

# https://docs.djangoproject.com/en/4.0/ref/contrib/admin/#django.contrib.admin.ModelAdmin.filter_vertical
# The Genre page is wonky due to the nature of many to many, so if applicable this can be implemented
# as a filter_vertical. 
admin.site.register(Recommendations)
admin.site.register(FinalResult)
admin.site.register(UserRankings)
admin.site.register(Image)