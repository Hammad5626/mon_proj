from django.urls import path
from . import views

urlpatterns = [
    path('',views.index,name='index'),
    path('home/', views.upload_excel, name='upload_excel'),
    path('monthly-stats/', views.monthly_stats_view, name='monthly_stats'),
    path('drawdown/', views.drawdown_calculation_view, name='drawdown'),
    path('graph/', views.graph_view, name='graph'),
    path('graph2/', views.graph2_view, name='graph2'),
    path('admin/login/', views.admin_login, name='admin_login'),
    path('admin/logout/', views.admin_logout, name='admin_logout'),
]