from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from users.serializers import UserSerializer


class UserDetailsView(RetrieveAPIView):
    """ 
    Class provides the functionality necessary to authenticate if a user exists.
    """
    serializer_class = UserSerializer
    lookup_url_kwarg = "uid"
    permission_classes = [IsAuthenticated]


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_detail_from_jwt(req):
    """ 
    Checks if a user is authenticated, using their JWT, and returns 401 if they're not, otherwise return the serialized user data.
    """
    if req.user is None:
        return Response("User not found", status=401)

    user = req.user
    serialized = UserSerializer(user).data

    return Response(data=serialized)
