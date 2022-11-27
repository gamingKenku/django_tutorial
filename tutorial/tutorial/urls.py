from django.urls import path, include
from hello import views as db_views
from users import views as users_views
from django.contrib import admin

urlpatterns = [
    path("", include("django.contrib.auth.urls")),
    path('admin/', admin.site.urls),
    path("", db_views.home),
    path("redact/<int:book_id>", db_views.redact),
    path("delete/<int:book_id>", db_views.delete),
    path("add/", db_views.add),
    path('users/register/', users_views.register, name="register"),
    path("users/login/", users_views.login_view, name="login"),
    path("users/logout/", users_views.logout_view, name="logout"),
    path("users/profile/", users_views.profile, name="profile"),
    path("users/profile/redact/", users_views.redact, name="redact"),
    path("users/profile/change_password/", users_views.change_password, name="redact"),
    path("users/cart/", users_views.cart, name='cart'),
    path("users/cart/add_to_cart/<int:book_id>", users_views.add_to_cart, name='add_to_cart'),
    path("users/cart/order", users_views.order, name='order'),
    path("users/profile/order_history", users_views.order_history, name='order_history')
]
