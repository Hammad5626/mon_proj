from django.urls import path
from .views import upload_excel,graph_view,index,admin_logout, graph2_view
from .views import AdminLoginView

urlpatterns = [
    path('',index,name='index'),
    path('home/', upload_excel, name='upload_excel'),
    path('graph/', graph_view, name='graph'),
    path('graph2/', graph2_view, name='graph2'),
    path('admin/login/', AdminLoginView.as_view(), name='admin_login'),
    path('admin/logout/', admin_logout, name='admin_logout'),
]