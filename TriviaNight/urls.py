"""TriviaNight URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.contrib import admin
from django.urls import path
from TriviaNight.views import *

urlpatterns = [path("admin/", admin.site.urls), path("", index, name="index"),
               path("run-answers/", run_answers, name="run-answers"),
               path("plot-heatmap/", plot_heatmap, name="plot-heatmap"),
               path("heatmap/", heatmap_view, name="heatmap"),
               path("plot-team-scores/", plot_team_scores, name="plot-team-scores")]
