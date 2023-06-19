# Django Notes IV:  
## Server Schedule Events Primer  
Something important that is bound to be necessary, for whatever reason, when running a server for a web application is the need to do some scheduled event. Most likely scenarios are automatic back ups, but other things could be updates based on some real world, changing parameter, for example, requesting new data from an API at regular intervals.  
Here is how to start off, very simply.  
### APScheduler  
This is a Python module that handles scheduling. It is not specific Django (even though there is a Django version of it, but I do not see it used too much). To integrate Advanced Python Scheduler into a Python program, first install it with pip. Recommended to install into a Django prepared virtual environment.  
  
    pip3 install apscheduler  
  
The documentation is here, for further reading…  
  
    https://apscheduler.readthedocs.io/en/3.x/userguide.html  
  
The demo here will be extremely simple, as it is meant to be for look back familiarization. That said, however, it does delve a little deeper into the workings of Django. Here are some concepts:  
It is the first time the apps.py file is actually used, which means that the application in INSTALLED_APPS in settings must be referenced properly, by its route.  
The updater will be a separate file, in a separate folder.  
The execution of the updater will also be a separate file.  
Let’s take a look.  
## The Project  
This project will do something really simple. It will automatically add a new entry to a model database every minute, while the server is running.  
### Start a new project:  
  
    django-admin startproject eventproject  
  
Inside the project folder, start a new application:  
  
    python3 manage.py startapp eventapp  
  
Here is where the new stuff starts. Inside the eventapp directory, create another one:  
  
    mkdir updater  
  
Inside the new updater directory, create three new, empty Python files, named such:  
  
    __init__.py  
    executeupdate.py  
    updater.py

The project structure should look like this…  
  
    • eventproject  
        ◦ eventproject  
        ◦ eventapp  
            ▪ __pycache__  
            ▪ updater  
                • __init__.py  
                • executeupdate.py  
                • updater.py  
            ▪ migrations  
  
All standard created files have been omitted from that structure, incidentally.  
The application route would be the first thing to do, which is pretty much normal. This is the urls.py file in the eventproject directory:  
  
    from django.contrib import admin
    from django.urls import path, include
  
    urlpatterns = [  
    	path('admin/', admin.site.urls),  
    	path("", include("eventapp.urls"))  
    ]  
  
Now go to settings.py, in the same directory, and add the application to it under INSTALLED_APPS:	 
  
    INSTALLED_APPS = [  
	    "eventapp.apps.EventappConfig",  
	    … the rest of the standard apps here...  
    ]  
      
It is now very important to properly set the route of the application to the apps.py file that resides in the eventapp directory, where previously just putting “eventapp“ would have sufficed. Not anymore.  
Now that the apps.py file has been mentioned, it is in the interest of continuity that it be looked at immediately. This is what it should look like:  
  
    from django.apps import AppConfig  
    
    class EventappConfig(AppConfig):  
	    default_auto_field = 'django.db.models.BigAutoField'  
	    name = 'eventapp'  
  
	    def ready(self):  
		from .updater import executeupdate  
		executeupdate.execute()  
  
The ready function is what is added. Ready is one of the normal class functions of the AppConfig, but here a custom version of it is being made. All it is saying is:  
  
    • Import your executeupdate.py file from the updater directory  
    • Do the execute() function that is (will be) inside that file.  
  
That is it. So, again, in the interest of continuity, let’s take a look at the new executeupdate.py file:  
  
    from apscheduler.schedulers.background import BackgroundScheduler  
    from .updater import create_save  
  
    def execute():  
	    scheduler = BackgroundScheduler()  
	    scheduler.add_job(create_save, "interval", minutes = 1)  
	    scheduler.start()  
  
Now, what the AppConfig is actually doing becomes apparent. This is the function that the ready function is calling from executeupdate.py when the application starts (is ready). Now what this function is needs to be looked at. From the top down.  
The new module that was installed to the environment earlier, apscheduler, contains a function that needs to be imported, BackgroundScheduler.  
Also, in the new custom file, updater.py, there will be another function called create_save. That gets imported, too (it will be made in a moment).  
The execute function, here, then makes an instance of BackgroundScheduler. To this instance, a new job (a new background job, to be clear) is added with the class function add_job(). This tells the BackgroundScheduler what function should be executed, how (interval, in this case), and how frequently (each minute, in this case).  
Once those parameters are set, the BackgroundScheduler instance is launched with the  start() class function. It will now run, as from application startup.  
So, now the create_save() function must be made, in the still empty updater.py file. This is what it will look like:  
  
    from eventapp.models import *  
    from random import randrange  
  
    def create_save():  
	    SEvent = SaveEvent.objects.all()  
	    rand_num = randrange(100)  
  
	    try:  
		    SEvent.create(saved = rand_num)  
	    except:  
		    print("There was an error!")  
  
Getting familiar again, now. A Django Model called SaveEvent is being imported here, at the top (which is yet to be made). Also, to just dump random numbers into the model, randrange is imported from standard Python random. As should be pretty clear to base Django coders, the function attempts to create a new SaveEvent model entry. That is all. The BackgroundScheduler job created in the executeupdate.py file is what will ensure that this function gets called every minute.  
So, now finish off the main stuff by creating that model. Go to the eventapp/models.py file. Create this model:  
  
    from django.db import models  
  
    class SaveEvent(models.Model):  
	    saved = models.IntegerField()  
  
	    def __str__(self):  
		return f"This is Save number {self.saved}"  
  
That would be it, except for some minor details now, which can be guessed. Namely, the eventapp/urls.py and eventapp/views.py files. In this application, they will not do much, but in more involved projects, somewhere to print out the results of the event will be needed, so this sets the canvas for it.  
The views.py file:  
  
    from django.shortcuts import render
    from django.http import HttpResponse
  
    def index(request):
	    return HttpResponse("<h1>The app is running</h1>")
  
The urls.py file:  
  
    from django.urls import path  
    from . import views  
  
    urlpatterns = [  
	    path("", views.index, name = "index")  
    ]  
  
Finally, to be able to see the effects of the running scheduled event, give admin access to the model in eventapp/admin.py, which will look like this:  
  
    from django.contrib import admin  
    from .models import *  
  
    admin.site.register(SaveEvent)  
  
Almost done. From the command line in the terminal, with the PWD in the project directory, make the migrations, and create a superuser:  
  
    python3 manage.py makemigrations eventapp  
  
    python3 manage.py migrate  
  
    python3 manage.py createsuperuser  
  
If all went well, the server should run, and after a few minutes, logging into the admin site and checking the model will reveal that a few entries were automatically created.  
Done!  
### Decorators  
There is a way to use decorators, which seems to cut down on the number of files needed to execute the function to create the save. I am not positive I have got this right, but it does seem to work. Here, I will describe it.  
Create the same project, but in the updater directory, only create these two files:  
    • updater  
        ◦ __init__.py  
        ◦ updater.py  
  
Now, that updater.py file will look like this:  
  
    from apscheduler.schedulers.background import BackgroundScheduler  
    from eventapp.models import *  
    from random import randrange  
  
    scheduler = BackgroundScheduler()  
  
    @scheduler.scheduled_job(trigger = "interval", minutes = 1)  
    def create_save():  
	    SEvent = SaveEvent.objects.all()  
	    try:  
		    SEvent.create(saved = randrange(100))  
	    except:  
		    print("There was an error")  
  
    scheduler.start()
  
Notice that the BackgroundScheduler is now integrated into this file (that is, no longer is the executeupdate.py file needed). The scheduler is both defined and started here, as well as the function to do the saving of the number to the model database. The decorator contains the periodicity that was previously in the executeupdate.py file.  
There is one other difference, of course. Go to the apps.py file in the eventapp directory. It will now look like this:  
  
    from django.apps import AppConfig  
  
    class EventappiiConfig(AppConfig):  
	    default_auto_field = 'django.db.models.BigAutoField'  
	    name = 'eventapp'  
  
	    def ready(self):  
		    from .updater import updater  
		    updater.create_save()  
  
See, now the create_save() function is imported directly, and not referenced through the executeupdate.py file anymore.  
This appears to work, for all intents and purposes.  
## Some other details  
The background scheduler add_job needs a slightly deeper look. First, there are warnings all over the place in the documentation about NOT letting two jobs run together. There are some ways described in the documentation as to how to avoid this if more than one job exists, or how to cause a job to wait for another to finish. As more familiarity is gained with apscheduler, this will be added to these notes.  
The other thing is the ways that jobs can be scheduled. Here, some practice is required.  
In the example, the job uses an “interval” method (properly called a trigger), set to minutes = 1. Playing around with that would allow the minutes to be increased, with no major problems.  In fact, for more clarity, the add_job could be written like this, specifying trigger:  
  
    scheduler.add_job(create_save, trigger = "interval", minutes = 1)  
  
So, there are three types of triggers:  
    • interval  
        ◦ https://apscheduler.readthedocs.io/en/3.x/modules/triggers/interval.html#module-apscheduler.triggers.interval  
    • date  
        ◦ https://apscheduler.readthedocs.io/en/3.x/modules/triggers/date.html#module-apscheduler.triggers.date  
    • cron  
        ◦ https://apscheduler.readthedocs.io/en/3.x/modules/triggers/cron.html#module-apscheduler.triggers.cron  
  
The date could be useful, but it is only for a one off event. The “cron” trigger, however, is actually useful if you want a repetitive scheduled event that fires at a particular time. Where the interval trigger works from intervals that utilize the start of the server as the datum, cron will actually wait for a specific, recurring time. There is some good reference of how to use it here:  
  
https://betterprogramming.pub/introduction-to-apscheduler-86337f3bb4a6  
For example, let’s say we want an event to fire every day at 05:20 hours UTC. Here is what could be done:  
  
    @scheduler.scheduled_job(trigger = "cron", hour = 5, minute = 20)  
  
It also accepts strings, which gives some more flexibility. For example, if you want the update to occur at both 05:20 and 05:25, you can do this:  
  
    @scheduler.scheduled_job(trigger = "cron", hour = 5, minute = “20,25”)  
  
Note that the minute parameter is now a string of both minute values separated by a comma.  
  
