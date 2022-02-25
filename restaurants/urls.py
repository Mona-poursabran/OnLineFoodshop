from django.urls import path
from django.urls.conf import include
from django.views.generic import TemplateView
from restaurants.views import *
from rest_framework import routers
router = routers.DefaultRouter()
router.register(r'adminpanel', foodViewSet)

urlpatterns = [
    path('', MenuItemList.as_view(), name='home'),
    path('search1/', search, name='search1'),
    path('search/', search_result, name='search'),
    path('<int:pk>/', get_info_search, name='product'),
    path('food/<int:pk>/', FoodDetails.as_view(), name= 'food_detail'),
    path('branchdetail/<int:pk>/', BranchDetails.as_view(), name="branch_detail"),

    path('Admin_panel/',AdminPanel.as_view(), name='admin_panel'),
    path('Admin_panel/restaurnats/', RestaurantsList.as_view(), name="restaurant_lists"),
    path('Admin_panel/restaurnats/menu/<int:pk>/', RestaurantMenu.as_view(), name="branch_detail_superuser"), 
    path('delete_branch/', DeleteBranch.as_view(), name="delete_rest"),
    path('create_food/', CreateFood.as_view(), name='create_food'),
    path('food/', FoodList.as_view(), name = 'food_list'),
    path('fooddetail/<int:pk>/', FoodDetailAdmin.as_view(), name='food_detail_admin'), 
    path('food/<int:pk>/update/', FoodUpdate.as_view(), name= 'food_update'),
    path('food/dalete/<int:pk>/', FoodDelete.as_view(), name="delete"),
    path('new_category/',NewCategory.as_view(), name='new_category'),
   
    
    path('menu_item/<int:pk>/', CartViewMenuItem.as_view(), name= 'product'),
    path('cart/', CartView.as_view(), name= 'cart'),
    path('checkout/', checkout, name='checkout'),
    path('update_order/', update_order, name="update_order"),
    # path('create_addr/', create_addr, name='create_addrr'),

    
    
    ####Rest framework
    path('apifood/',AllFood.as_view(), name = 'food_list_2'),
    path('foodview/', include(router.urls)),

    path('apifoods/', Foods.as_view(), name= 'foods'),
    path('foods/', show_foods, name='food'),


 ]


