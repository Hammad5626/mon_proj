from django.urls import path
from .views import (index, 
                    upload_excel, 
                    drawdown_calculation_view, 
                    signup, 
                    signin, 
                    logout_view, 
                    user_list, 
                    toggle_favorite, 
                    favorite_users, 
                    user_data
                )

urlpatterns = [
    path('', index ,name='index'),
    path('upload-excel/', upload_excel, name='upload_excel'),
    path('drawdown/', drawdown_calculation_view, name='drawdown'),
    path('signup/', signup, name='signup'),
    path('signin/', signin, name='signin'),
    path('logout/', logout_view, name='logout'),
    path('users/', user_list, name='user_list'),
    path('toggle_favorite/', toggle_favorite, name='toggle_favorite'),
    path('favorite-users/', favorite_users, name='favorite_users'),
    path('user-data/<int:user_id>/', user_data, name='user_data'),
]