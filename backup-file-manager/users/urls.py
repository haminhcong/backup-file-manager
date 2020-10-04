from django.urls import path

from . import views

app_name = 'user'
urlpatterns = [

    path(r'profile/', views.ProfileView.as_view(), name='profile'),
    path(r'password/', views.ChangePasswordView.as_view(), name='change_password'),
    path(r'api-tokens/', views.TokenListView.as_view(), name='token_list'),
    path(r'api-tokens/add/', views.TokenEditView.as_view(), name='token_add'),
    path(r'api-tokens/<int:pk>/edit/', views.TokenEditView.as_view(), name='token_edit'),
    path(r'api-tokens/<int:pk>/delete/', views.TokenDeleteView.as_view(), name='token_delete'),
]
