from django.contrib import admin
from django.contrib.admin.options import TabularInline
from django.contrib.auth.admin import UserAdmin
from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import *
# Register your models here.


admin.site.register(Address)
admin.site.register(CustomerAddr)

class CustomerAddress(TabularInline):
    model= CustomerAddr


# class CustomUserAdmin():
#     model = CustomUser
#     list_display = ['username', 'email', 'is_superuser', 'is_staff', 'password']
# admin.site.register(CustomUser, CustomUserAdmin)

class CustomUserAdmin(admin.ModelAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ['email', 'username','password', 'is_staff', 'is_superuser']
admin.site.register(CustomUser, CustomUserAdmin)


@admin.register(Admin)
class CustomAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'is_superuser']
    list_display_links = ['email']
    search_fields = ['username', 'email']
    fieldsets = ( 
        (None, {'fields': ('username','password','email')}), 
        ) 
  
    list_filter = ['is_active']

    def get_queryset(self, request):
        return Admin.objects.filter(is_superuser=True)
    
    def save_model(self, request, obj, form, change):
        obj.set_password(form.cleaned_data["password"])
        obj.save()


@admin.register(Customer)
class Customers(admin.ModelAdmin):
    list_display = ['id','email', 'username' ]
    fieldsets = ( 
        (None, {'fields': ('username','password','email')}), 
        ) 

    inlines=[CustomerAddress]
    def save_model(self, request, obj, form, change):
        obj.set_password(form.cleaned_data["password"])
        obj.save()

    def get_queryset(self, request) :
        return Customer.objects.filter(is_staff=False)


@admin.register(ResturantManager)
class ManagerAdmin(admin.ModelAdmin):
    list_display = ['email', 'username', 'is_staff' ]
    fieldsets = ( 
        (None, {'fields': ('username','password','email')}), 
        ) 
 
    def save_model(self, request, obj, form, change):
        obj.set_password(form.cleaned_data["password"])
        obj.save()

    def get_queryset(self, request) :
        return ResturantManager.objects.filter(is_staff=True, is_superuser= False)
