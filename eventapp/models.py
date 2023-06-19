from django.db import models

class SaveEvent(models.Model):
    saved = models.IntegerField()

    def __str__(self):
        return f"This is Save number {self.saved}"
    
    
