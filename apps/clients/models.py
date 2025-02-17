from django.db import models

class ClientModel(models.Model):

    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    phone = models.CharField(max_length=20)

    def __str__(self):
        return self.name
    

    
class AddressModel(models.Model):
    client = models.ForeignKey(ClientModel, on_delete=models.CASCADE, related_name='addresses', null=True, blank=True)
    address = models.CharField(max_length=200)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    

    def __str__(self):
        return self.address