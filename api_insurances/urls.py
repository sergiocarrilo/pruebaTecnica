from . import views
from django.urls import path

urlpatterns = [
    path('login/', views.LoginViewSet.as_view({
        'post': 'login'
    }), name='login'),
    path('register/', views.RegisterViewSet.as_view({
        'post': 'register'
    }), name='register'),
    path('account/', views.AccountViewSet.as_view({
        'delete': 'unsubscribe'
    }), name='account'),
    path('password/change/', views.AccountViewSet.as_view({
        'patch': 'change_password'
    }), name='password_change'),
    path('insurance/', views.InsuranceViewSet.as_view({
        'get': 'list',
        'post': 'create'
    }), name='insurance'),
    path('insurance/<int:pk>/', views.InsuranceViewSet.as_view({
        'get': 'get',
        'delete': 'delete'
    }), name='insurance_id'),

]
