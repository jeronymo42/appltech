from django.urls import path, include
from .views import Iphones, index, GadgetAdd, MoreInfo, GadgetUpdateView, GadgetDeleteView, user_registration, user_login, user_logout, contact_email, gadget_api_list, gadget_api_detail
from basket.views import basket_info
urlpatterns = [
    path('main/', Iphones.as_view(), name='shop'),
    path('', index, name='index'),
    path('addgadget/', GadgetAdd.as_view(), name='addgadget'),
    path('main/<int:key>/', MoreInfo.as_view(), name='details'),
    path('main/editgadget/<int:key>/',
         GadgetUpdateView.as_view(), name='editgadget'),
    path('main/deletegadget/<int:key>/',
         GadgetDeleteView.as_view(), name='deletegadget'),
    path('registration/', user_registration, name='regis'),
    path('login/', user_login, name='log in'),
    path('logout/', user_logout, name='log out'),
    path('email/', contact_email, name='contact_email'),
    path('basket/', basket_info, name='basket'),
    path('api/list/', gadget_api_list, name='gadget_api_list'),
    path('api/detail/<int:pk>', gadget_api_detail, name='gadget_api_detail'),

]
