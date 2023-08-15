from django.urls import path

from app.views import PortfolioView

app_name = "app"

urlpatterns = [
    path("", PortfolioView.as_view()),
]
