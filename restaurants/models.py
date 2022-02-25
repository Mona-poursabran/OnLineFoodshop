from django.db import models
from accounts.models import ResturantManager
import jdatetime
from django.core.validators import MinValueValidator
from django.urls import reverse
# Create your models here.

class Meal_Food(models.Model):
    MEAL =[ 
        ('Breakfast', 'Breakfast'),
        ('Lunch', 'Lunch'),
        ('Dinner', 'Dinner')
    ]
    name = models.CharField(choices=MEAL, max_length=10, verbose_name='Meal')
    def __str__(self):
        return self.name


class Category(models.Model):
    type = models.CharField(max_length=100)
    
    def get_absolute_url(self):
        return reverse("category_detail", args=[str(self.id)])
    

    class Meta:
        verbose_name_plural= 'Categories'

    def __str__(self):
        return self.type

class Food(models.Model):
    food_name = models.CharField(max_length=50)
    image = models.ImageField(upload_to='food/%Y__%m__%d/', null=True, blank=True, default=None)
    description = models.TextField(null=True, blank=True)
    category = models.ForeignKey(Category, related_name='category_food', on_delete=models.CASCADE)
    meal = models.ManyToManyField(Meal_Food, related_name='meal_food')
    created_date = models.DateField(auto_now_add=True)
 
 
    @property
    def create_date_jalali(self):
        return jdatetime.datetime.fromgregorian(datetime=self.created_date)


    def get_absolute_url(self):
        return reverse("food_detail", args=[str(self.id)])
    
    def __str__(self):
        return self.food_name

    
class Restaurant (models.Model):
    name = models.CharField(max_length=30, verbose_name="Restaurant's name")
    class Meta:
        abstract = True


class Branch(Restaurant):
    image = models.ImageField(upload_to='branch/%Y__%m__%d/', null=True, blank=True)
    main_branch = models.BooleanField(default=False)
    category = models.ForeignKey(Category, related_name='branch_category' , on_delete=models.PROTECT)
    branch_name =models.CharField(max_length=30)
    city = models.CharField(max_length=30, default='Tehran')
    address = models.CharField(max_length=50, default='Poonak')
    description = models.TextField(null=True , blank=True)
    created_date = models.DateField(auto_now_add=True)
    manager = models.OneToOneField(ResturantManager,on_delete=models.CASCADE)
    
    @property
    def create_date_jalali(self):
        return jdatetime.datetime.fromgregorian(datetime=self.created_date)
    
    
    def __str__(self) -> str:
         return f"{self.name}>>{self.branch_name}"


class Menu(models.Model):
    branch= models.OneToOneField(Branch, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f'{str(self.branch)}'
    

class MenuItem(models.Model):
    menu = models.ForeignKey(Menu, related_name='menu', on_delete=models.CASCADE)
    food = models.ForeignKey(Food, related_name='menu_food', on_delete=models.SET_NULL, null= True)
    price = models.PositiveIntegerField()
    quantity = models.PositiveIntegerField()

    # @property
    # def sub_quantity(self):
    #     q = self.menu_order.all()
    #     sub = [self.quantity -item.quantity for item in q]
    #     return sub

    def __str__(self) -> str:
        return f"{self.price}>>{str(self.food)}>>{str(self.menu)}"



class OrderItem(models.Model):
    order = models.ForeignKey('Order',related_name='order' , on_delete=models.SET_NULL, null= True)
    menu_item= models.ForeignKey(MenuItem, related_name='menu_order', on_delete=models.SET_NULL, null= True)
    quantity = models.IntegerField(null= True, validators=[MinValueValidator(1)])


    @property
    def get_total(self):
        foodname = str(Food.objects.filter(menu_food__menu_order__id=self.id).values_list('food_name')[0][0])
        total = int(MenuItem.objects.filter(menu_order__order=self.order).filter(food__food_name=foodname).values_list("price")[0][0]) * self.quantity
        return total
        
    def is_same_restaurant(self, branch):
        return self.menu_item.menu.branch == branch


class Order(models.Model):
    FINAL_STATUS = [ 
        ('Order','Order'),
        ('Regist', 'Rgist'),
        ('Send', 'Send'),
        ('Delivery', 'Delivery')]

    # branch = models.ForeignKey(Branch, related_name='branch_order' ,on_delete=models.SET_NULL, null=True)
    customer = models.ForeignKey('accounts.Customer', related_name='customer_order', on_delete=models.SET_NULL, null= True)
    customer_addr = models.ForeignKey('accounts.Address', on_delete=models.CASCADE, null=True)
    menu_item = models.ManyToManyField(MenuItem, through=OrderItem,  related_name="order_food")
    status = models.CharField(choices=FINAL_STATUS, max_length=10, default='Order')
    total_price = models.PositiveIntegerField(null=True)
    order_date = models.DateTimeField(auto_now_add=True)

  

    @property
    def get_cart_total(self):
        orderitems = OrderItem.objects.all().filter(order=self.id)
        total = sum([item.get_total for item in orderitems])
        return total 

    @property
    def get_cart_items(self):
        orderitems = OrderItem.objects.all().filter(order=self.id)
        total = sum([item.quantity for item in orderitems])
        return total


    @property 
    def created_at_jalali(self):
        return jdatetime.datetime.fromgregorian(datetime= self.order_date)

 

    def __str__(self) -> str:
        return f'{str(self.status)}'