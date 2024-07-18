from django.contrib import admin,messages
from .models import Event,Participants

from datetime import datetime
class nbr_Participation(admin.SimpleListFilter):
    title = 'Number of participations'
    parameter_name = 'nbr_paticipants'

    def lookups(self, request, model_admin):
        return (
            ('No', ("No participants")),
            ('Yes', ("There are participants ")),
            
        )

    def queryset(self, request, queryset):
        if self.value() == 'No':
            return queryset.filter(nbr_paticipants__exact=0)
        if self.value() == 'Yes':
            return queryset.filter(nbr_paticipants__gt=0)
        




def accept_state(ModelAdmin,request, queryset):

    row_updated = queryset.update(state=True)

    if (row_updated ==1):

        msg = "1 event was"
    
    else:
        msg = f"{row_updated} events were"

    messages.success(request,f"{msg} successfully updated")
    


def refuse_state(ModelAdmin,request, queryset):

    row_updated = queryset.update(state=False)

    if (row_updated ==1):

        msg = "1 event was"
    
    else:
        msg = f"{row_updated} events were"

    messages.success(request,f"{msg} successfully updated")
       

accept_state.short_description = "State True"

refuse_state.short_description = "State False"



class ParticipationInline (admin.TabularInline):
    model = Participants
    extra = 1
    readonly_fields=('participation_date',)
    classes =['collapse']



@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    
     list_display=('title','category','evt_date','state','nbr_paticipants' ,'created_at')

     readonly_fields=('created_at','updated_at',)

     def numberOfParticipants(self,obj):
          nb = obj.participant.count()
          return nb
     list_per_page = 2

     list_filter=('title',nbr_Participation,)


     autocomplete_fields= ['organisateur']
     actions=[accept_state , refuse_state]


     fieldsets = (
            ('A propos', {"fields": ('title','description','image'),}),
            ('Date',{"fields":('evt_date','created_at','updated_at')
            }),
            ('Others',{"fields":('category','state','nbr_paticipants') }),
            ('Personal',{"fields":('organisateur',) }))
     
     inlines =[ParticipationInline]

@admin.register(Participants)
class participationAdmin(admin.ModelAdmin):
    pass