from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

# 繼承viewsets.ModelViewSet，使用套件自動生成urls
router = DefaultRouter()
router.register(r'chatrooms', views.ChatroomViewSets , basename='chatroom')
router.register(r'messages', views.MessageViewSets , basename='message')




urlpatterns = [
    path('', views.home, name="home"),
    # path('isexistchatroom/',views.is_exist_chatroom,name="is-exist-chatroom"),
    # path('createchatroom/',views.create_chatroom,name="create-chatroom"),
    # path('getmessage/',views.get_message,name="get-message"),
    # path('sendmessage/',views.send_message,name="send-message"),
    path('api/', include(router.urls)),
]

