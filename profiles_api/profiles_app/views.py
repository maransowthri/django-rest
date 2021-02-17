from rest_framework.views import APIView
from rest_framework.response import Response


class HelloAPIView(APIView):
    """Test API View

    Args:
        APIView (View): Generic API View provided by rest_framework
    """

    def get(self, request, format=None):
        """Returns list of user names

        Args:
            request (HTTPRequest): Input request
            format (string, optional): Request format. Defaults to None.
        """
        usernames = ['Karan', 'Kalees', 'Maran', 'Mahesh']

        return Response({ 'message': 'Request has been processed successfully', 'usernames': usernames })