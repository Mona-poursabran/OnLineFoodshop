from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import *
from restaurants.models import *
from django.contrib.auth.hashers import make_password
from allauth.account.forms import SignupForm, LoginForm
from allauth.account.adapter import DefaultAccountAdapter

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('email', 'username',)

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('email', 'username',)
        




class CustomUserForm(UserCreationForm):
    email = forms.EmailField(required=True)
    city = forms.CharField(max_length=30)
    street = forms.CharField(max_length=30)
    plaque = forms.IntegerField(min_value=1)
    is_main = forms.BooleanField()
    class Meta(UserCreationForm):
        model = Customer
        fields = ['username','email', 'city', 'street', 'plaque', 'is_main']
    
    def save(self, commit= True) :
        user = super().save(commit=False)
        if commit:
            user.save()
        return user



class MangerUserForm(forms.ModelForm):
    email = forms.EmailField(required=True)
    username = forms.CharField(required=True)
    password = forms.CharField(required=True, widget=forms.PasswordInput())
    password2 = forms.CharField(required=True, widget=forms.PasswordInput())


    class Meta:
        model = Branch
        fields = ("email","username","name","branch_name","image", "address", "city", "description","category","main_branch","password","password2")
        widgets = { 
             'password': forms.PasswordInput(), 
             'password2': forms.PasswordInput(),
            'description': forms.Textarea(attrs={'cols': 15, 'rows':5})
                } 

    def save(self, commit=True):
            email = self.cleaned_data['email']
            username = self.cleaned_data['username']
            password = make_password(self.cleaned_data['password'])
            manager = ResturantManager.objects.create(username = username, password = password,email  = email)
            manager.save()
            name = self.cleaned_data["name"]
            branch_name = self.cleaned_data['branch_name']
            image = self.cleaned_data['image']
            category = self.cleaned_data['category']
            address = self.cleaned_data['address']
            city = self.cleaned_data['city']
            description = self.cleaned_data['description']
            main_branch = self.cleaned_data['main_branch']
            branch = Branch.objects.create(name = name, branch_name = branch_name, image=image,  manager = manager , category=category ,address = address,city = city ,description = description, main_branch= main_branch )
            branch.save()




