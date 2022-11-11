from django.urls import path
from press import views

urlpatterns = [
    # ex: /polls/5/
    path('home/', views.home)

]