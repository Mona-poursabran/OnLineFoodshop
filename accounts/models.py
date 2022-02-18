from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)


class Address(models.Model):
    city = models.CharField(max_length=30)
    street = models.CharField(max_length=30)
    plaque = models.PositiveIntegerField()
    def __str__(self):
        return self.city+" "+self.street+" "+str(self.plaque)

class Customer (CustomUser):
    device = models.CharField(max_length=200, null= True, blank=True )
    class Meta:
        verbose_name = "Customer"

    def save(self,*args, **kwargs ) :
        if not self.id:
            self.is_staff= False
        return super(Customer, self).save(*args, **kwargs )


class CustomerAddr(models.Model):
    customer= models.ForeignKey(Customer, related_name='customer_addr', on_delete=models.SET_NULL, null= True)
    address = models.ForeignKey(Address, related_name='addr_customer', on_delete=models.SET_NULL, null= True)
    is_main = models.BooleanField(default=True, verbose_name='Main_Address')
    def __str__(self) -> str:
        return f'{str(self.customer)} {str(self.address)}'


class ResturantManager(CustomUser):
    class Meta:
        # proxy = True
        verbose_name = "Manager"
        verbose_name_plural = "Managers"

    def save(self,*args, **kwargs ) :
        if not self.id:
            self.is_staff= True
            self.is_superuser = False
        return super(ResturantManager, self).save(*args, **kwargs )


class Admin(CustomUser):
    class Meta:
        proxy = True
        verbose_name = "Admin"
        verbose_name_plural = "Admins"

    def save(self,*args, **kwargs ) :
        if not self.id:
            self.is_superuser =True
        return super(Admin, self).save(*args, **kwargs )

