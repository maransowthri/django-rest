from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from profiles_app.serializers import UserSerializer


class UsersAPIView(APIView):
    """Test API View

    Args:
        APIView (View): Generic API View provided by rest_framework
    """
    serializer_class = UserSerializer

    def get(self, request, format=None):
        """Returns list of user names

        Args:
            request (HTTPRequest): Input request
        """
        usernames = ['Karan', 'Kalees', 'Maran', 'Mahesh']

        return Response({ 'message': 'Usernames returned properly', 'usernames': usernames })
    
    def post(self, request):
        """Creates a new user

        Args:
            request (HTTPRequest): Input Request
        """
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            name = serializer.validated_data.get('name')
            greetings = f'Hello {name}!'
            return Response({ 'greetings': greetings, 'message': 'User has been created successfully' })
        else:
            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
    
    def put(self, request, pk=None):
        """Updates an existing user data

        Args:
            request (HTTP Request): Input Request
        """
        return Response({ 'message': 'User has been updated successfully' })

    def patch(self, request, pk=None):
        """Updates part of the existing user

        Args:
            request (HTTP Request): Input Request
        """
        return Response({ 'message': 'User has been patched successfully' })
        
    def delete(self, request, pk=None):
        """Deletes an existing user

        Args:
            request (HTTP Request): Input Request
        """
        return Response({ 'message': 'User has been deleted successfully' })
        