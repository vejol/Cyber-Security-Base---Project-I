from django.urls import path

from .views import homePageView, transferView, checkView, transactionsView

urlpatterns = [
    path('', homePageView, name='home'),
    path('transfer/', transferView, name='transfer'),
    path('check/', checkView, name='check'),
    path('transactions/<str:name>', transactionsView, name='transactionsView')
]
