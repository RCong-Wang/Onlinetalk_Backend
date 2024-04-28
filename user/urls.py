from django.urls import path
from . import views

app_name = 'user'

# urlpatterns = [
#     # path('signin/', views.usersignin, name="signin-page"),
#     # path('login/', views.userlogin, name="login"),
#     # path('logout/',views.userlogout, name="logout"),
#     # path('addfriend/<int:friend>/',views.add_friend,name="add-friend"),
#     # path('searchfriend/',views.search_friend,name="search-friend"),
#     # path('friendlist/',views.friend_list,name="friend-list"),
#     path('checklogin/',views.check_user_login,name="check-login"),
# ]

urlpatterns = [
    path('checklogin/',views.check_user_login,name="check-login"),
    path('login/',views.userlogin,name='login'),
    path('logout/',views.userlogout,name='logout'),
    path('getcsrf/',views.get_csrf_token,name='csrf'),
    path('friendlist/',views.friend_list,name='friend-list'),
    path('searchfriend/',views.search_friend,name='search-box'),
    path('addfriend/',views.add_friend,name='add-friend'),
]