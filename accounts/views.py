import re
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from datetime import datetime
from django.shortcuts import redirect, render
from restaurants.models import *
from .forms import *
from .models import *
from django.urls import reverse_lazy
from django.views.generic import *
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin 
from .mixin import StaffRequiredMixin
from django.db.models import Q

def customer_signup(req):
    """
        Customer is able to register by entering address
    """
    if req.method == 'POST':
        form = CustomUserForm(req.POST)
        if form.is_valid():
            form.save()
            address = Address.objects.create(city=req.POST['city'], street=req.POST['street'], plaque=req.POST['plaque'])
            customer= Customer.objects.get(email=req.POST['email'])
            customer_addr = CustomerAddr.objects.create(customer =customer, address = address, is_main= True )
            return redirect('home')
    form = CustomUserForm()
    return render(req, 'registration/signup_customer.html', {'form': form})





def manager_signup(req):
    """
        Manager is able to register by adding address and branch info
    """
    form = MangerUserForm()
    if req.method == 'POST':
        form = MangerUserForm(req.POST)
        if form.is_valid() and req.POST['password'] and req.POST['password2'] and req.POST['password'] == req.POST['password2']:
            form = form.save()
            return redirect('home')
        return render (req, "registration/signup_manager.html", {"form": form, 'msg': "Wrong"})
    
    return render(req, 'registration/signup_manager.html', {'form': form})



def login_success(req):
    if req.user.is_staff and not req.user.is_superuser:
        return redirect('manager_panel')  
    elif req.user.is_superuser and req.user.is_staff:
        return redirect('admin_panel')
    else:
        return redirect('customer_info')

################################################# Manager Info #####################################################
class AbstractRestaurantManager(LoginRequiredMixin, UserPassesTestMixin):

    def test_func(self):
        if not self.request.user.is_superuser:
            return self.request.user.is_staff

class ManagerPanel(AbstractRestaurantManager,StaffRequiredMixin,LoginRequiredMixin,TemplateView):
    """
        Restaurant Manager Panel
    """
    model= Branch
    template_name='restaurant/Manager_panel.html'




class UpdateBranch(AbstractRestaurantManager,StaffRequiredMixin,LoginRequiredMixin, UpdateView):
    """
    Restaurant's manager is able to update branch info
    """
    model = Branch
    template_name = 'restaurant/branch_update.html'
    fields = ["image","name", "branch_name","city","address","category","main_branch"]
    success_url = reverse_lazy('branch_manager')
  

class BranchManager(AbstractRestaurantManager,StaffRequiredMixin,LoginRequiredMixin,ListView):
    """
        Restaurant's manager is able to see branch info
    """
    model = Branch
    context_object_name = 'branch_list'
    template_name ='restaurant/branch.html'

  

  
class BranchDetail(AbstractRestaurantManager,StaffRequiredMixin,LoginRequiredMixin,DetailView):
    """
        restaurant's manager is able to see details and menu
    """
    model = Branch
    template_name= 'restaurant/branch_detail_manager.html'




class UpdateMenu(AbstractRestaurantManager,StaffRequiredMixin,LoginRequiredMixin, UpdateView):
    """
        restaurant's manager is able to update the menu
    """
    model = MenuItem
    template_name = 'restaurant/update_menu.html'
    fields= ['price', 'quantity']

    def get_success_url(self):
        branch = Branch.objects.filter(manager__username = self.request.user.username)
        for i in branch:
            pk= i.id
        return reverse("branch_detail_manager", kwargs={"pk": pk})
 

class DeleteMenu(AbstractRestaurantManager,StaffRequiredMixin,LoginRequiredMixin, DeleteView):
    model = MenuItem
    template_name = "restaurant/delete_menu.html"
    fields = ['food', 'price', 'quantity']

    def get_success_url(self):
        branch = Branch.objects.filter(manager__username = self.request.user.username)
        for i in branch:
            pk= i.id
        return reverse("branch_detail_manager", kwargs={"pk": pk})




  
@login_required
def create_menu(req):
    if req.user.is_staff and not req.user.is_superuser:
        branch1 = Branch.objects.filter(manager__username = req.user.username)
        for i in branch1:
            pk= i.id
            category = i.category

        food = Food.objects.filter(category= category)
        branch = Branch.objects.get(manager__username =req.user.username)
        print(branch)
        menu, created = Menu.objects.get_or_create(branch = branch)

        print("Menu: ",menu)
        if  req.method == 'POST':
            food = req.POST.get('food')
            price = req.POST.get('price')
            quantity = req.POST.get('number')

            foods = Food.objects.get(food_name= food)
            obj = MenuItem.objects.create(menu = menu, food= foods, price= price, quantity= quantity)
            obj.save()
            return redirect(reverse("branch_detail_manager", kwargs={"pk": pk}))
    else:
        html = "<html><body><h1>This Page Is Forbidden!!!!</h1></body></html>"
        return HttpResponse(html)
    context = {'food': food, 'menu': menu, 'branch_manager': branch}
    return render(req, 'restaurant/create_menu.html', context)
    

class MangerCheckStatus(AbstractRestaurantManager, ListView):
    model = Order
    template_name = "restaurant/managerordercheck.html"

    def get_queryset(self):
        return Order.objects.filter(status='Regist').filter(order__menu_item__menu__branch__manager__username=self.request.user.username).distinct()

    def post(self, request):
        status ={'Send': 'Send', 'Delivery': 'Delivery'}
        if request.is_ajax():
            order_index = int(request.POST.get('order_index'))
            print('order_index', order_index)
            order = self.get_queryset()[order_index]
            order.status = status.get(request.POST.get('status'))
            print('status', order.status)
            order.save()
            return JsonResponse({})


########################################## Customer Info ############################################################
class AbstractCustomerUser(LoginRequiredMixin, UserPassesTestMixin):

    def test_func(self):
        if not self.request.user.is_superuser and not self.request.user.is_staff:
            return True

class CustomerInfo(AbstractCustomerUser,LoginRequiredMixin, ListView):
    model = Customer
    template_name ="restaurant/customer_info.html"
    context_object_name = 'customer_list'
   
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["addr"] = Address.objects.filter(addr_customer__customer__username= self.request.user.username)
        context['customer_addr'] = CustomerAddr.objects.filter(customer__username = self.request.user.username)
        context['Address'] = CustomerAddr.objects.all()
        return context
    


class CustomerOrderHistory(AbstractCustomerUser,LoginRequiredMixin, ListView):
    model= Order
    template_name = 'restaurant/customerorderlist.html'
    context_object_name = 'order_list'

    def get_queryset(self):
        self.queryset = Order.objects.filter(customer= self.request.user, status="Regist")
        return self.queryset



class CustomerUpdate(AbstractCustomerUser,LoginRequiredMixin,UpdateView):
    """
        customer is able to update its info
    """
    model = Customer
    template_name ="restaurant/customer_update.html"
    success_url = reverse_lazy('customer_info')
    fields =['first_name', 'last_name', 'username']


class CustomerMainAddressUpdate(AbstractCustomerUser,LoginRequiredMixin, UpdateView):
    """
        customer is able to update its main and extra addr
    """
    model = Address
    template_name = 'restaurant/customer_main_addr_update.html'
    success_url = reverse_lazy('customer_info')
    fields = ['city', 'street', 'plaque']


# @login_required
# def create_addr(req):
#     """
#         customer is able to add a new address
#     """
#     if not req.user.is_superuser and not req.user.is_staff:
#         if req.method == 'POST':
#             city = req.POST.get('city')
#             street = req.POST.get('street')
#             plaque = req.POST.get('plaque')

#             address = Address.objects.create(city= city, street= street, plaque= plaque)
#             customer = Customer.objects.get(username= req.user.username)
#             customeraddr = CustomerAddr.objects.create(address = address, customer= customer, is_main= False)
#             customeraddr.save()
#             return redirect('customer_info')
#     else:
#         html = "<html><body><h1>This Page Is Forbidden!!!!</h1></body></html>"
#         return HttpResponse(html)

#     return render(req, 'restaurant/new_addr.html')



################################################# Address  #######################################################

# class AddressView(ListView):
#     model = CustomerAddr
#     template_name = 'restaurant/customer_info.html'
#     context_object_name = 'Address'

class CreateAddress(View):
    def  get(self, request):
        city1 = request.GET.get('city', None)
        street1 = request.GET.get('street', None)
        plaque1 = request.GET.get('plaque', None)

        customer = Customer.objects.get(username = request.user.username)
        address = Address.objects.create(city= city1, street= street1, plaque = plaque1)
        print(customer, type(customer))
        print(address)
        obj =CustomerAddr.objects.create(
            customer = customer,
            address = address,
            is_main = False
        )

        user = {'id':obj.address.id,'city':obj.address.city,'street':obj.address.street,'plaque':obj.address.plaque,'is_main':obj.is_main}
        print(user)
        data = {
            'user': user,
        }
        return JsonResponse(data)



class UpdateAddressr(View):
    def  get(self, request):
        id1 = request.GET.get('id', None)
        city1 = request.GET.get('city', None)
        street1 = request.GET.get('street', None)
        plaque1 = request.GET.get('plaque', None)

        obj = Address.objects.get(id = id1)
        obj.city = city1
        obj.street = street1
        obj.plaque = plaque1
        obj.save()
        print("Address",obj)

        user = {'id':obj.id,'city':obj.city,'street':obj.street,'plaque':obj.plaque}
        print("user: ",user)
        data = {
            'user': user
        }
        return JsonResponse(data)


class DeleteAddress(View):
    def get(self, request ):
        id1 = request.GET.get('id', None)
        CustomerAddr.objects.get(address__id = id1).delete() 
        Address.objects.get(id = id1).delete()
        print('customeraddr.delete', CustomerAddr.objects.get(address__id = id1).delete() )     

        data ={
            'deleted':True
        }

        return JsonResponse(data)








