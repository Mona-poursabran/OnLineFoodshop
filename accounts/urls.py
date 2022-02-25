from django.urls import path
from .views import *
from django.views.generic import TemplateView
urlpatterns = [
    path('signupcustomer/', customer_signup, name = 'signup_customer'),
    path('signupmanager/', manager_signup, name='signup_manager'),
    path('login_success/', login_success, name='login_success'),


    # PANEL MANAGER:)
    path('manager_panel/', ManagerPanel.as_view(), name='manager_panel'),
    path('branch/', BranchManager.as_view(), name='branch_manager'),
    path('branch/<int:pk>/', BranchDetail.as_view(), name='branch_detail_manager'),
    path('branch/<int:pk>/edit_branch/', UpdateBranch.as_view(), name= 'branch_edit'),
    path('branch/create_menu/', create_menu, name="create_menu" ),
    path('branch/<int:pk>/menu_update/',UpdateMenu.as_view(), name='update_menu'),
    path('branch/<int:pk>/menu_delete/', DeleteMenu.as_view(), name='delete_menu'),
    path('checkorders/', MangerCheckStatus.as_view(), name='checkstatus'),
    
    
    #PANEL CUSTOMER :)
    path('customer_info/', CustomerInfo.as_view(), name="customer_info"),
    path('customer_info/<int:pk>', CustomerUpdate.as_view(), name = "customer_update"),
    path('customer_info/main_addr/<int:pk>/', CustomerMainAddressUpdate.as_view(), name="update_addr"),
    path('customer_info/history-order/', CustomerOrderHistory.as_view(), name='customer_order'),
    # path('customer_info/new_addr/', create_addr , name= 'create_addr'),


    # Test

    # path('crud/', AddressView.as_view(), name='crud_ajax'),
    path('ajax/crud/create/',  CreateAddress.as_view(), name='crud_ajax_create'),
    path('ajax/crud/update/',  UpdateAddressr.as_view(), name='crud_ajax_update'),
    path('ajax/crud/delete/',  DeleteAddress.as_view(), name='crud_ajax_delete'),

    
    
]
