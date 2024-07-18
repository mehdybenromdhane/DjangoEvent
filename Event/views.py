from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render,redirect
from django.http import JsonResponse
import json

from .models import Event,Participants
from django.http import HttpResponse
from .forms import EventForm
from django.views.generic import *
# Create your views here.
from django.urls import reverse_lazy

from dotenv import load_dotenv

from Person.models import Person
import os
from django.core.files import File

import google.generativeai as genai
import requests
# You can access the image with PIL.Image for example
import io
from PIL import Image
# Access your API key as an environment variable.



GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
IMAGEGEN_KEY = os.getenv('IMAGEGEN_KEY')


genai.configure(api_key=GOOGLE_API_KEY)

def ai_generate_description(title):

    model = genai.GenerativeModel('gemini-1.5-flash')

    prompt=f"Generate a detailed description for an event with the title in 4 lines: {title}",

    response = model.generate_content(prompt)

    
    return response.text
def generate_description(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        title = data.get('title', '')
        description = ai_generate_description(title)  # Call your AI content generation function here
        return JsonResponse({'description': description})
    return JsonResponse({'error': 'Invalid request'}, status=400)





API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-xl-base-1.0"
headers = {"Authorization": f"Bearer {IMAGEGEN_KEY} "}

def imageGen(payload):
	response = requests.post(API_URL, headers=headers, json=payload)
	return response.content


def generate_image(request):
    if request.method == 'POST':
        # Generate the image


        data = json.loads(request.body)
        title = data.get('title', '')
        image_bytes = imageGen({
            "inputs": f"event for {title}",
        })

        # Save the image to a temporary in-memory file
        image = Image.open(io.BytesIO(image_bytes))
        with io.BytesIO() as output:
            image.save(output, format="JPEG")
            image_data = output.getvalue()


        # Save the image temporarily to the filesystem (e.g., in the media directory)
        image_name = 'generated_image.jpg'
        image_path = 'media/images/' + image_name
        with open(image_path, 'wb') as f:
            f.write(image_data)

        return JsonResponse({'image_url': '/' + image_path})
    return JsonResponse({'error': 'Invalid request method'}, status=400)
def hello (request , name):

    text = f"hello {name}"
    
    return render(request , 'event/list.html' , { 't':text})




def listEvent(request):

    list = Event.objects.filter(state=True).order_by('-evt_date')


    nbr_event = Event.objects.filter(state=True).count()


    return render(request , 'event/list.html', { 'list':list , 'nbr':nbr_event} )



class ListEvents(ListView):

    model=Event
    template_name="event/list.html"
    context_object_name = "list"


    def get_queryset(self):
        list = Event.objects.filter(state=True)
        return list

        











class Details(DetailView):
    model=Event
    template_name="event/details.html"
    context_object_name="event"



def detailEvent(req,ide): 

     event=  Event.objects.get(id=ide)
     user = req.user


     button =False
     participant = Participants.objects.filter(person = user, event=event)




     if participant:
         button=True
     else:
         button=False

    



     return render(req, "event/detailsEventFc.html" , {'evenement':event , 'btn':button })


def addEvent(req):

    form = EventForm()

    if req.method == 'POST':

        form = EventForm(req.POST,req.FILES)

        if form.is_valid():
            event = form.save(commit=False)
            file_name = os.path.basename('generated_image.jpg')

            print(file_name)
            file_path = os.path.join('media/images', file_name)
            with open(file_path, 'rb') as f:
                event.image.save(file_name, File(f), save=True)
            event.save()
            print (event)
            
        form.save()
        return redirect('listEvent')

    return render (req , "event/add.html" , {'form':form} )





class Add(CreateView):
    model= Event
    template_name = "event/add.html"
    form_class = EventForm



class Update(UpdateView):

    model= Event
    template_name = "event/update.html"
    form_class = EventForm
    success_url =  reverse_lazy('listEvent')


class deleteEvent(DeleteView):

    model=Event
    template_name= "event/delete.html"

    success_url =  reverse_lazy('listEvent')



def delete(req,ide):

    event=  Event.objects.get(id=ide)

    if event:
        event.delete()

    
    return redirect("listEvent")




def participer(req,id):

    event = Event.objects.get(id=id)
    user = Person.objects.get(cin=1144)

    if user: 
        participant = Participants.objects.create(person = user , event= event)
        participant.save()

        event.nbr_paticipants += 1

        event.save()

    return redirect("listEvent")




def cancel(req,id):

    event = Event.objects.get(id=id)
    user = Person.objects.get(cin=1144)

    if user: 
        participant = Participants.objects.filter(person = user , event= event)
        participant.delete()

        event.nbr_paticipants -= 1

        event.save()

    return redirect("listEvent")