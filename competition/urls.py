"""
math_competition URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('logout/', views.log_out, name='logout'),
    path('login/', views.log_in, name='login'),
    path('competition/<int:comp_id>/', views.comp_detail, name='comp_detail'),
    path('problem/<int:prob_id>/', views.prob_detail, name='prob_detail'),
    path('competition/register/<int:comp_id>/', views.register_comp, name='register_comp'),
    path('competition/<int:comp_id>/standings/', views.standings, name='standings')
]