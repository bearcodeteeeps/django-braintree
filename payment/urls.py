from django.conf.urls import url
import views

urlpatterns = [
    url(r'^subscribe/', views.paymentview, name = "subscribe")
]