from django.contrib import admin
from .models import Person
# Register your models here.




@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    
    list_display=("username", "email" , "cin" , "last_login")
    search_fields=('email',)