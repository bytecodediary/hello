from django.urls import path
from . import views
app_name = 'frontend'

urlpatterns = [
    path('chatbot-response/', views.get_chatbot_response, name='chatbot-response'),
    path("", views.home, name='home'),
]