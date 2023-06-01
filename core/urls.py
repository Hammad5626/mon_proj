from django.urls import path
from .views import upload_excel,graph_view,index,admin_logout, graph2_view, monthly_stats_view, drawdown_calculation_view
from .views import AdminLoginView

urlpatterns = [
    path('',index,name='index'),
    path('home/', upload_excel, name='upload_excel'),
    path('monthly-stats/', monthly_stats_view, name='monthly_stats'),
    path('drawdown/', drawdown_calculation_view, name='drawdown'),
    path('graph/', graph_view, name='graph'),
    path('graph2/', graph2_view, name='graph2'),
    path('admin/login/', AdminLoginView.as_view(), name='admin_login'),
    path('admin/logout/', admin_logout, name='admin_logout'),
]