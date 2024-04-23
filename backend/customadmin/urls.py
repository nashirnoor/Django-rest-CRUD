from django.urls import path
from .views import AdminLogin,AdminUsersList,AdminUpdateUser,AdminSearchUser,AdminUserDelete


urlpatterns = [
    path('',AdminLogin.as_view()),
    path('users/',AdminUsersList.as_view()),
    path('user-update/<int:pk>/',AdminUpdateUser.as_view()),
    path('user-delete/<int:pk>/',AdminUserDelete.as_view()),
    path('user-search/',AdminSearchUser.as_view()),
    
]
