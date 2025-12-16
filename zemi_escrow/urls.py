from django.urls import path
from zemi_escrow import views

urlpatterns = [
    path("create_order/", views.create_order),
    path("payment_webhook/", views.payment_webhook),
    path("confirm_delivery/", views.confirm_delivery),
    path("stk_push/", views.stk_push),
    path("confirm_stk/", views.confirm_stk),
    path("release_funds/", views.release_funds),
]
