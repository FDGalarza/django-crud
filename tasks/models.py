from django.db import models
from django.contrib.auth.models import User # para relacionar las tareas con el usuario que las crea modelo User

# Create your models here.
    
class Task(models.Model):
    title           = models.CharField(max_length=200) # campo de texto con maximo 200 caracteres
    description     = models.TextField(blank=True) #campo de texto puede estar vacio
    created         = models.DateTimeField(auto_now_add=True) # campo fecha con la fecha actual por defecto
    datecompleted   = models.DateTimeField(null=True) # campo fecha null
    important       = models.BooleanField(default=False) # campo booleano con valor por defecto
    user            = models.ForeignKey(User, on_delete=models.CASCADE) # llave foranea del modelo usuario,
                                                                        # con eliminación por cascada
                                                                        
    def __str__(self):
        return self.title + '- by ' + self.user.username
        