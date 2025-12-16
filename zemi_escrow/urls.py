from django.urls import path
from .views import (
    create_order,
    payment_webhook,
    confirm_delivery,
    stk_push,
    confirm_stk,
    release_funds,
)

urlpatterns = [
    path("create_order/", create_order, name="create_order"),
    path("payment_webhook/", payment_webhook, name="payment_webhook"),
    path("confirm_delivery/", confirm_delivery, name="confirm_delivery"),
    path("stk_push/", stk_push, name="stk_push"),
    path("confirm_stk/", confirm_stk, name="confirm_stk"),
    path("release_funds/", release_funds, name="release_funds"),
]
