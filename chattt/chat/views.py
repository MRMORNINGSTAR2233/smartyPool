from django.shortcuts import render
from django.contrib.auth import get_user_model
from .models import(
    ChatSession,ChatSessionMember,ChatSessionMessage, deserialize_user
)
from rest_framework import APIView , status
from rest_framework.response import Response
from rest_framework import permissions
# Create your views here.

class ChatSessionView(APIView):
    """Manage chat sessions."""

    permissions_classes = (permissions.IsAuthenticated,)

    def post(self, request, *awrgs, **kwargs):
        """create a new chat session."""
        user = request.user

        chat_session = ChatSession.objects.create(owner=user)

        return Response(
            {
                'status':'SUCCESS',
                'uri':chat_session.uri,
                'message':'New chat session created'
            }
        )
    def patch(self, request, *args, **kwargs):
        """Add a user to a chat sessoins."""

        User = get_user_model()

        uri = kwargs["uri"]
        username = request.data['username']
        user = User.objects.get(username=username)

        chat_session = ChatSession.objects.get(uri=uri)
        owner = chat_session.owner

        if owner != user:
            chat_session.members.get_or_create(user=user , chat_session=chat_session)

        owner = deserialize_user(owner)
        members =[
            deserialize_user(chat_session.user)
            for chat_session in chat_session.members.all()  
        ]

        members.insert(0, owner)
        return Response({
            'status':'SUCCESS',
            'members':members,
            'message':'%s joined the chat'%user.username,
            'user':deserialize_user(user)
        })

class ChatSesMesView(APIView):
    """Create/get Chat sessions messages"""

    permissions_classes = (permissions.IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        """return all messages in a chat session"""

        uri = kwargs["uri"]

        chat_session = ChatSession.objects.get(uri=uri)

        messages = [chat_session_message.to_json()
                    for chat_session_message in chat_session.messages.all()]
        return Response({
            'id':chat_session.id,
            'uri':chat_session.uri,
            'messages':messages
        })
    def post(self, request, *args, **kwargs):
        """Create a new message in a chat session"""

        uri = kwargs['uri']
        message = request.data['message']

        user  = request.user 
        chat_session = ChatSession.objects.get(uri=uri)

        ChatSessionMessage.objects.create(
            user=user, chat_session=chat_session, message=message
        )
        return Response({
            'status':'SUCCESS',
            'uri':chat_session.uri,
            "message":message,
            'user':deserialize_user(user)
        })