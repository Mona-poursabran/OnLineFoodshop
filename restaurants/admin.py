from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(Meal_Food)
admin.site.register(Category)


class Menu_Item(admin.TabularInline):
    model = MenuItem

@admin.register(Menu)
class Menucustom(admin.ModelAdmin):
    inlines=[Menu_Item]
  

@admin.register(Branch)
class BranchAdmin(admin.ModelAdmin):
    list_display = ['name', 'branch_name', 'city' ,'main_branch']
    list_display_links =  ['branch_name', 'name']
    list_filter= ['name']


@admin.register(Food)
class FoodAdmin(admin.ModelAdmin):
    list_display =['food_name', 'created_date']
    search_fields = ['food_name']
    list_filter= ['created_date']


@admin.register(Order) 
class OrderAdmin(admin.ModelAdmin): 
    search_fields = ['status','created_date']  
    list_filter = ['status'] 
     

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['order','quantity'] 
    search_fields=['order']
