from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
# Create your models here.


def is_email_esprit(value):
   
   if str(value).endswith('@esprit.tn') == False:
      
      raise ValidationError(f"Your email {value} must end with @esprit.tn ")
   return value

def valideCin(value):
   if len(value)!=8:
      raise ValidationError("Cin must has 8 characters")
   
   return value

class Person(AbstractUser):
    cin = models.CharField(primary_key=True, max_length=8 ,validators=[valideCin])
    email = models.EmailField("Email",max_length=50 ,unique=True  , validators=[is_email_esprit])
    username = models.CharField(max_length=20 , unique=True)

    USERNAME_FIELD='username'


    def __str__(self):
      return  self.username


    class Meta:
        verbose_name="Person"