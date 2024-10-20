from django.db import models
from django.contrib.auth import get_user_model
from uuid import uuid4
# Create your models here.

User = get_user_model()

def deserialize_user(user):
    """Deserialize user instamce in json"""
    return{
        'id':user.id,'username':user.username, 'email':user.email,
        'first_name':user.first_name, 'last_name':user.last_name
    }

class TracableDateModel(models.Model):
    """Abstarct model for track of create/update date for a model."""

    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)   

class Meta:
    abstarct = True

def generate_unique_uri():
    """Generate unique uri for the chat sessions."""
    return str(uuid4()).replace('-','')[:15]

class ChatSession(TracableDateModel):
    """A chat session. The uri are generated by taking the first 15 charecters from the UUID"""

    owner = models.ForeignKey(User, on_delete=models.PROTECT)
    uri = models.URLField(default=generate_unique_uri)

class ChatSessionMessage(TracableDateModel):
    """Store  messages for a session."""

    user = models.ForeignKey(User, on_delete=models.PROTECT)
    chat_session = models.ForeignKey(ChatSession, related_name='messages', on_delete=models.PROTECT)
    message = models.TextField(max_length=500)

    def to_json(self):
        """Deserialize message to json"""
        return {
            'user':deserialize_user(self.user),
            'message':self.message
        }
class ChatSessionMember(TracableDateModel):
    """Store all the users in a chat sessions"""

    chat_session = models.ForeignKey(
        ChatSession, related_name='memebers', on_delete = models.PROTECT
    )

    user = models.ForeignKey(User, on_delete=models.PROTECT)