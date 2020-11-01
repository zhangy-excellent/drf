from django.urls import path

from api import views

urlpatterns = [
    path('books/',views.BookAPIView.as_view()),
    path('books/<str:id>',views.BookAPIView.as_view()),
    path('v2/books/',views.BookAPIViewV2.as_view()),
    path('v2/books/<str:id>',views.BookAPIViewV2.as_view()),
    # 名字必须是lookup_field里规定好的,不然会报错
    path('gen/<str:pk>',views.BookGenericView.as_view()),
    path('gen/',views.BookGenericView.as_view()),

    path('v2/gen/<str:pk>',views.BookGenericViewV2.as_view()),
    path('v2/gen/',views.BookGenericViewV2.as_view()),

    # path('set/',views.BookGenericViewV2.as_view()),
    # path('set/<str:pk>',views.BookGenericViewV2.as_view()),

    path('set/login/',views.BookViewSetView.as_view({"post":"user_login"})),
    path('set/register/',views.BookViewSetView.as_view({'post':"user_register"})),
    path('set/get_total/',views.BookViewSetView.as_view({'get':"get_user_count"})),
]