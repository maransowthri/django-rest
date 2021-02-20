from rest_framework import status, viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.filters import SearchFilter
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.settings import api_settings
from rest_framework.permissions import IsAuthenticated

from profiles_app.models import UserProfile, ProfileFeedItem
from profiles_app.serializers import TestSerializer, UserProfileSerializer, ProfileFeedItemSerializer
from profiles_app.permissions import UserProfilePermission, ProfileFeedPermission


class TestAPIView(APIView):
    """Test API View

    Args:
        APIView (View): Generic API View provided by rest_framework
    """
    serializer_class = TestSerializer

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
        

class TestViewSet(viewsets.ViewSet):
    """Test View Sets

    Args:
        viewsets (ViewSet): generic viewset provided by rest_framework
    """
    serializer_class = TestSerializer

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
    

class UserProfileViewSet(viewsets.ModelViewSet):
    """Handles user profile read, update & delete

    Args:
        viewsets (ViewSet): Generic viewset provided by rest_framework
    """
    serializer_class = UserProfileSerializer
    queryset = UserProfile.objects.all()
    permission_classes = (UserProfilePermission,)
    authentication_classes = (TokenAuthentication,)
    filter_backends = (SearchFilter,)
    search_fields = ('name', 'email')


class UserAuthView(ObtainAuthToken):
    """Handles user authentication

    Args:
        ObtainAuthToken (authToken): auth token provided by rest framework
    """
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES

class UserProfileFeedViewSet(viewsets.ModelViewSet):
    """Handles profile feeds

    Args:
        viewsets (ViewSet): Generic ViewSet provided by rest framework
    """
    serializer_class = ProfileFeedItemSerializer
    queryset = ProfileFeedItem.objects.all() 
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, ProfileFeedPermission)

    def perform_create(self, serializer):
        """Sets user profile to the logged in user

        Args:
            serializer (Serializer): Serializer used for this ViewSet
        """
        serializer.save(user_profile=self.request.user)

