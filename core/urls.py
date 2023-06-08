from django.urls import path
from . import views

urlpatterns = [
    path('',views.index,name='index'),
    path('upload-excel/', views.upload_excel, name='upload_excel'),
    path('drawdown/', views.drawdown_calculation_view, name='drawdown'),
    path('signup/', views.signup, name='signup'),
    path('signin/', views.signin, name='signin'),
    path('logout/', views.logout_view, name='logout'),
    path('users/', views.user_list, name='user_list'),
    path('toggle_favorite/', views.toggle_favorite, name='toggle_favorite'),
    path('favorite-users/', views.favorite_users, name='favorite_users'),
    path('user-data/<int:user_id>/', views.user_data, name='user_data'),
]