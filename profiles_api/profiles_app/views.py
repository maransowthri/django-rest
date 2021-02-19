from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, viewsets
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
        

class UsersViewset(viewsets.ViewSet):
    """Test View Sets

    Args:
        viewsets (ViewSet): generic viewset provided by rest_framework
    """
    serializer_class = UserSerializer

    def list(self, request):
        """Get all user objects

        Args:
            request (HTTPRequest): Input request

        Returns:
            HTTPResponse: Expected API Response
        """
        usernames = ['Karan', 'Kalees', 'Maran', 'Mahesh']
        return Response({ 'message': 'Usernames has been sent properly', 'usernames': usernames })
    
    def retrieve(self, request, pk=None):
        """Retrieve a particualr user object

        Args:
            request (HTTPRequest): Input Request
            pk (int): User ID
        """
        return Response({ 'messgae': 'Returning paricular user object' })
    
    def create(self, request):
        """Creates a new user object

        Args:
            request (HTTPRequest): Input Request
        """
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            name = serializer.validated_data.get('name')
            greetings = f'Hello {name}'
            return Response({ 'message': 'User object has been created successfully', 'greetings': greetings })
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        """Updates existing user object

        Args:
            request (HTTPRequest): Input Request
            pk(int): User ID
        """
        return Response({ 'message': 'Updated user object successfully'})   

    def partial_update(self, request, pk=None):
        """Updates existing user object partially

        Args:
            request (HTTPRequest): Input Request
            pk(int): User ID
        """
        return Response({ 'message': 'Partially updated user object successfully'})   
    
    def destroy(self, request, pk=None):
        """Deleted existing user object

        Args:
            request (HTTPRequest): Input Request
            pk(int): User ID
        """
        return Response({ 'message': 'Deleted user object successfully'})   
    
