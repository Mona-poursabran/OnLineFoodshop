from restaurants.serializer import FoodSerializer
from .models import *
from django.db.models import Q
from django.shortcuts import redirect, render, get_object_or_404
from accounts.models import Address, Customer, CustomerAddr
from django.urls import reverse_lazy
from django.http import JsonResponse,HttpResponseForbidden,HttpResponseNotFound
from django.db.models import Sum
from django.views.generic import *
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from accounts.mixin import SuperUserRequiredMixin
from django.contrib import messages
###Rest
from rest_framework import generics, viewsets,permissions
from rest_framework.views import APIView
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response

############################ Admin Panel #################################

class AdminPanel(SuperUserRequiredMixin, TemplateView):
    """
        Admin panel
    """
    template_name = 'restaurant/Admin_panel.html'



class RestaurantsList(SuperUserRequiredMixin,ListView):
    """
        Admin is able to check restaurants
    """
    model = Branch
    context_object_name = 'check_branch'
    template_name = 'restaurant/admin_check_branch.html'

class RestaurantMenu(SuperUserRequiredMixin,DetailView):
    """
        Admin is able to check restaurants' menu
    """
    model= Branch
    template_name = 'restaurant/branch_detail_superuser.html'
    context_object_name = 'branch'

class DeleteBranch(SuperUserRequiredMixin, View):
    def get(self,req):
        id = req.GET.get('id')
        branch_id =  Branch.objects.filter(id= id).values_list('id', flat=True)[0]
        print('branch', branch_id)
        ResturantManager.objects.get(branch__id = branch_id).delete()

        data={
            'deleted': True
        }
        return JsonResponse(data)
        

class CreateFood(SuperUserRequiredMixin,CreateView):
    """
    Admin is able to create a new food
    """
    model = Food
    template_name = 'restaurant/create_food.html'
    fields= '__all__'
    success_url = reverse_lazy('food_list')


class FoodList(SuperUserRequiredMixin,ListView):
    """
    Admin has the list of food
    """
    model = Food
    context_object_name = 'food_list'
    template_name = 'restaurant/food_list.html'


class FoodDetailAdmin(SuperUserRequiredMixin, DetailView):
    """
    Admin can check each detail of food
    """
    model = Food
    template_name = 'restaurant/food_detail_admin.html'


class FoodUpdate(SuperUserRequiredMixin, UpdateView):
    """
    Admin is able to update one food
    """
    model= Food
    template_name = 'restaurant/update_food.html'
    fields = '__all__'

    def get_success_url(self):
           pk = self.kwargs["pk"]
           return reverse("food_detail_admin", kwargs={"pk": pk})


class FoodDelete(SuperUserRequiredMixin,View):
    """
    Admin is able to delete a food 
    using ajax
    """
    def get(self,request, pk, *args, **kwargs):
        if request.is_ajax:
            food = Food.objects.get(pk = pk)
            food.delete()
            return JsonResponse({"message": "success"})
        return JsonResponse({"message":"wrong"})


class NewCategory(SuperUserRequiredMixin, CreateView):
    """
    Admin is able to add a new categoty
    """
    model = Category
    template_name = 'restaurant/new_category.html'
    fields =['type']
    success_url = reverse_lazy('create_food')


################################## Home Page ###################################

class FoodDetails(DetailView):
    """
    customer is able to check the food details
    """
    model = Food
    template_name = 'restaurant/food_detail.html'



class MenuItemList(ListView):  
    """
        Home page with list of food category , restaurants
    """
    # model = MenuItem
    model = Branch
    context_object_name = 'menu_list'
    template_name = 'home.html'
    
    def get_queryset(self):
        category = Category.objects.all()

        # foods = MenuItem.objects.filter(quantity__gt= 0, food__category__in = category).order_by('food__category','menu__branch__name')
        foods = Branch.objects.filter(category__in= category)
        return foods

    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        context['best_food'] = Food.objects.filter(
                                Q(menu_food__menu_order__order__status= 'Regist')|
                                Q(menu_food__menu_order__order__status= 'Send')  | 
                                Q(menu_food__menu_order__order__status= 'Delivery')).annotate(sum_food= Sum("menu_food__menu_order__quantity")).order_by("-sum_food")[:3]
        context['best_restaurant'] =Menu.objects.filter(
                                Q(menu__menu_order__order__status= 'Regist')|
                                Q(menu__menu_order__order__status= 'Send')| 
                                Q(menu__menu_order__order__status= 'Delivery')).annotate(total_price= Sum("menu__menu_order__order__total_price")).order_by("-total_price")[:3]
        return context



def search(req):
    """
        all users are able to search food and restaurant's name with render html
    """
    results=[]
    if req.method == 'GET':
        query = req.GET.get('search')
        if query == '':
            query = 'None'
        results = MenuItem.objects.filter(Q(food__food_name__icontains= query)| Q(menu__branch__name__icontains=query))
    context ={'query': query, 'results': results}
    print(results)
    return render(req, 'restaurant/search.html', context)


class BranchDetails(DetailView):
    """
        Customer and Admin is able to see Branch info
    """
    model= Branch
    template_name = 'restaurant/branch_detail.html'

################################# Search food and restaurants ################################
def search_result(req):
    """
        all users are able to search food and restaurant's name with ajax
    """
    if req.is_ajax():
        res = None
        result = req.POST.get('data')
        q = MenuItem.objects.filter(Q(food__food_name__icontains= result)| Q(menu__branch__name__icontains=result)| Q(menu__branch__branch_name__icontains=result))
        if len(q) > 0 and len(result) > 0:
            data =[]
            for i in q:
                item ={
                    'pk' : i.pk,
                    'food':{'food_name':i.food.food_name, 'img':i.food.image.url},
                    'menu': {'name':i.menu.branch.name, 'branch':i.menu.branch.branch_name},
                    'price': i.price,
                    'quantity': i.quantity
                }
                data.append(item)
            res = data
        else:
            res = "No Food Or Restaurant Found..."

        return JsonResponse({'dataa':res})
    return JsonResponse({})



def get_info_search(req, pk):
    obj = get_object_or_404(MenuItem, pk=pk)
    return render(req, 'restaurant/search.html', {'obj':obj})



############################### Cart ###############################

class CartViewMenuItem(DetailView):
    model = MenuItem
    template_name = "restaurant/product.html"

    def post(self, request, *args, **kwargs):
        menu_item = self.get_object()
        print('menu_item',menu_item)
        if request.user.is_authenticated:
            customer = Customer.objects.get(username= request.user.username)
        else:
            device = request.COOKIES['device']
            customer, bool_created = Customer.objects.get_or_create(device=device, username=device)

        if int(request.POST.get('quantity')) > menu_item.quantity:
            messages.error(request, "The quantity which you have choosen is more than our quantity!")
            return redirect(reverse('product', kwargs={'pk': menu_item.pk}))

        if Order.objects.filter(customer=customer, status='Order').exists():
            order = Order.objects.get(customer=customer, status='Order')
            if not order.order.first().is_same_restaurant(menu_item.menu.branch):
                order.order.all().delete()
                messages.info(request, "Previuos Order is deleted !")

        else:
            order = Order.objects.create(customer=customer, status='Order')
        order_item, bool_created = OrderItem.objects.get_or_create(order=order, menu_item=menu_item)
        order_item.quantity = request.POST['quantity']
        order_item.save()
        return redirect('cart')




def get_cart(customer):
    if Order.objects.filter(customer=customer, status='Order').exists():
        return Order.objects.filter(customer=customer, status='Order').first()
    return None
        
def set_cart_for_real_customer(request, order):
    real_customer = request.user
    real_customer_order, created = Order.objects.get_or_create(customer=real_customer, status='Order')
    real_customer_order.order.all().delete()
    real_customer_order.order.set(list(order.order.all()))
    order.delete()
    return real_customer_order



class CartView(View):
    def get(self, request, *args, **kwargs):
        device = self.request.COOKIES.get('device')
        if Customer.objects.filter(device=device).exists() and self.request.user.is_authenticated:
            device_customer = Customer.objects.filter(device=device).last()
            device_cart = get_cart(device_customer)
            if device_cart:
                order = set_cart_for_real_customer(self.request, device_cart)
                device_customer.delete()
            else:
                order = get_cart(self.request.user)
                print('order', order)
        else:
            if request.user.is_authenticated:
                customer = request.user
            else:
                customer, created = Customer.objects.get_or_create(username=device, device=device)
            order = get_cart(customer)
            queryset = Address.objects.filter(addr_customer__customer__username= request.user.username)
        queryset = Address.objects.filter(addr_customer__customer__username= request.user.username)
        return render(request, 'restaurant/cart.html', {'order': order, 'addresses':list(queryset.values('city', 'street', 'plaque'))})

    # def post(self, request):
    #     queryset = Address.objects.filter(addr_customer__customer__username= request.user.username)
    #     print('queryset,', queryset)
    #     return JsonResponse({"addresses": list(queryset.values('city', 'street', 'plaque'))})


def checkout(req):
    if not req.user.is_superuser and not req.user.is_staff:
        if req.method == 'POST' and req.is_ajax:
            index = int(req.POST.get("selected_address_index"))
            selected_address = Address.objects.all()[index]
            print('selected_address',selected_address)
            customer = req.user
            order = Order.objects.get(customer= customer, status= 'Order')
            b = Branch.objects.all()
            for i in b:
                pk = i.pk
            order.status = 'Regist'
            order.customer_addr = selected_address
            order.total_price = order.get_cart_total
            order.save()
            for orderitem in order.order.all():
                orderitem.menu_item.quantity -= orderitem.quantity
                orderitem.menu_item.save()
            return JsonResponse({'message':"Your order is registered!"})
        else:
            return  HttpResponseForbidden("<h1>403 Forbidden</h1>")
    return HttpResponseNotFound('<h1>4o4 Page not found</h1>')




def update_order(request):
    if request.method == "POST" and request.is_ajax:
        if request.user.is_authenticated:
            customer = request.user
        else:
            device = request.COOKIES['device']
            customer, bool_created = Customer.objects.get_or_create(device=device)

        order_item = request.POST.get('order_item')

        order = Order.objects.get(customer=customer, status='Order')
        order.order.all()[int(order_item)].delete()
        if not order.order.all():
            order.delete()
        return JsonResponse({})
    return JsonResponse({})





"""
    Using rest framework for admin panel

"""

class AllFood(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'food_list.html'
    
    def get(self, request):
        queryset = MenuItem.objects.all()
        return Response({'foods': queryset})


class foodViewSet(viewsets.ModelViewSet):
    queryset = Food.objects.all()
    serializer_class = FoodSerializer
    permission_classes = [permissions.IsAdminUser, permissions.IsAuthenticated ]

    
class Foods (generics.ListAPIView):
    queryset = Food.objects.all()
    serializer_class = FoodSerializer
    permission_classes = [permissions.IsAdminUser]


def show_foods(req):
    return render(req, 'show_food.html')
