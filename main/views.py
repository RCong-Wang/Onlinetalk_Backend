###############################################
from .models import Message, Chatroom
from user.models import UserProfile
from .serializers import ChatroomSerializer, MessageSeralizer

from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework import serializers
from rest_framework.decorators import action
from rest_framework.decorators import action, authentication_classes, permission_classes
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
#################################################
def home(request):

    return render(request, 'home/index.html')


@authentication_classes([SessionAuthentication])  # SessionAuthentication 身分驗證
@permission_classes([IsAuthenticated])  # 登入才可以創建或尋找聊天室
class ChatroomViewSets(viewsets.ModelViewSet):
    queryset = Chatroom.objects.all()
    serializer_class = ChatroomSerializer

    def perform_create(self, serializer):
        chatroom = serializer.save()
        chatroom.members.add(self.request.user.userprofile)

    #回傳聊天室的id，無則創建
    @action(detail=False, methods=['GET'])
    def chatroom_is_exist(self, request):
        self_user_profile = request.user.userprofile
        friend_profile = self_user_profile.friend.get(id=request.GET.get('id'))
        room = Chatroom.objects.filter(members=self_user_profile).filter(members=friend_profile).first()
        if room:
            return Response({'success':room.id})
        else:
            return Response({'room_id':"N/A"})

@authentication_classes([SessionAuthentication])  # SessionAuthentication 身分驗證
@permission_classes([IsAuthenticated])  # 登入才可以傳訊息
class MessageViewSets(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSeralizer

    def perform_create(self, serializer):
        serializer.save(senter=self.request.user.userprofile)

    def create(self, request, *args, **kwargs):
        try:
            response = super().create(request, *args, **kwargs)
            return response
        except serializers.ValidationError as e:
            print("Validation Error:", e.detail)
            raise e
    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        print(instance.context)
        instance.delete()
        
        return Response({'success':'successful delete'})

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset()).filter(room=request.GET.get('id'))
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

# ###############################################
# @login_required
# def is_exist_chatroom(request):
#     user_a = request.user.userprofile
#     friend_id = request.GET.get('id')
#     user_b = get_object_or_404(UserProfile,id=friend_id)
#     room = Chatroom.objects.filter(members=user_a).filter(members=user_b).first()
#     if room:
#         return JsonResponse({"success":room.id})
#     else:
#         return JsonResponse({"fail":"room is not exist!"})

# @login_required
# def create_chatroom(request):
#     user_a_profile = request.user.userprofile
#     friend_id = int(request.body)
#     user_b_profile = get_object_or_404(UserProfile,id=friend_id)

#     room = Chatroom(
#         name = user_a_profile.user.username+" and "+ user_b_profile.user.username
#     )
#     room.save()
#     room.members.add(user_a_profile,user_b_profile)
#     room.save()

#     return JsonResponse({"success":room.id})

# @login_required 
# def get_message(request):
#     room_id = request.GET.get('id')
#     room = get_object_or_404(request.user.userprofile.member, id=room_id)
#     message = room.room.all()
#     if not message:
#         return JsonResponse({"fail":"message is null"})
#     else:
#         serializer = MessageSeralizer(message,many=True)
#         messages = serializer.data
#         return JsonResponse(messages, safe=False)

# @login_required
# def send_message(request):
#     if request.method =="POST":
#         data = json.loads(request.body)
#         room = get_object_or_404(request.user.userprofile.member,id=data.get('id'))
#         new_message = Message(
#             context = data.get('messages'),
#             senter = request.user.userprofile,
#         )
#         new_message.save()
#         new_message.room.set([room])
#         new_message.save()

#         context = {
#             "id":new_message.id,
#             "context":new_message.context,
#             "time": new_message.time,
#             "senter": new_message.senter.id,
#         }
#         return JsonResponse(context)
#     else:
#         return JsonResponse({"success":"fail send"})
        
        





