from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

class CatalogueView(APIView):
    permission_classes = [IsAuthenticated]  # Ensure that only authenticated users can access this API

    def get(self, request):
        try:
            # Dummy catalogue data (you can replace this with actual DB data)
            catalogue_data = [
                {"id": 1, "name": "Item 1", "price": 100},
                {"id": 2, "name": "Item 2", "price": 200},
                {"id": 3, "name": "Item 3", "price": 300},
            ]

            return Response({
                "message": "Catalogue retrieved successfully",
                "catalogue": catalogue_data
            }, status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response({"error": f"Failed to retrieve catalogue: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)