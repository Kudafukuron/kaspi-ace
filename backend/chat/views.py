from rest_framework.views import APIView
from rest_framework.response import Response
from .models import ChatMessage
from rest_framework.permissions import IsAuthenticated
from users.models import User
from .serializers import ChatMessageSerializer

class ChatHistoryView(APIView):
    def get(self, request, user_id):
        other_user_id = user_id
        messages = ChatMessage.objects.filter(
            sender__in=[request.user.id, other_user_id],
            receiver__in=[request.user.id, other_user_id]
        ).order_by("timestamp")

        return Response(ChatMessageSerializer(messages, many=True).data)

class SendMessageView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        receiver_id = request.data.get("receiver")
        content = request.data.get("content")

        if not receiver_id or not content:
            return Response({"error": "receiver and content required"}, status=400)

        try:
            receiver = User.objects.get(id=receiver_id)
        except User.DoesNotExist:
            return Response({"error": "receiver not found"}, status=404)

        msg = ChatMessage.objects.create(
            sender=request.user,
            receiver=receiver,
            content=content
        )

        return Response(ChatMessageSerializer(msg).data, status=201)