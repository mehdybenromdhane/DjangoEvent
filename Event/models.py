from django.db import models
from Person.models import Person
# Create your models here.
from datetime import datetime

class Event (models.Model):
    category_list=(
        ("Musique","Musique"),
        ("Cinema","Cinema"),
        ("Sport","Sport"),

    )

    category =models.CharField(max_length=10,choices=category_list )
    title = models.CharField(max_length=20)
    description= models.TextField()
    image=models.ImageField(null=True , upload_to="images/",blank=True)
    state=models.BooleanField(default=False)
    nbr_paticipants= models.IntegerField(default=0)
    evt_date=models.DateTimeField(null=True)
    created_at = models.DateField(auto_now_add=True)
    updated_at =models.DateField(auto_now=True)
    organisateur = models.ForeignKey(Person , on_delete=models.SET_NULL , null=True)
    participant = models.ManyToManyField(Person, through="Participants" , related_name="participant")


    class Meta:
        constraints =[

            models.CheckConstraint(check=models.Q(
            evt_date__gt= datetime.now()

            ), name = "Please check date event")
       
       
        ]

    def __str__(self):
        return self.title

class Participants(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)

    participation_date = models.DateTimeField(datetime.now() , null=True , auto_now_add=True)
     
    class Meta:
        unique_together=['person','event']
       
