from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

def custom_404(request, exception=None):
    return JsonResponse(
        {"error": "The requested endpoint was not found."}, status=404
    )

class HealthCheckView(APIView):
    def get(self, request):
        try:
            return Response({"status": "healthy"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

