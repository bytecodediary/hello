from django.urls import path
from . import views
app_name = 'frontend'

urlpatterns = [
    path('chatbot-response/', views.get_chatbot_response, name='chatbot_get_response'),
    path("home/", views.home, name='home'),
]