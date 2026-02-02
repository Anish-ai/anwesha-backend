from django.http import JsonResponse
from .models import Sponsors, MyntraRegistration
from django.views import View
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import HTTP_401_UNAUTHORIZED, HTTP_404_NOT_FOUND, HTTP_200_OK
from cryptography.fernet import Fernet
import json
from django.conf import settings
from user.models import User


def allsponsors(request):
    if request.method == "GET":
        # Retrieve all sponsors from the database
        sponsors = Sponsors.objects.all()
        # Convert the sponsor queryset to a list of dictionaries
        listed_sponsors = list(sponsors.values())
        # Return a JSON response with the list of sponsors
        return JsonResponse(listed_sponsors, safe=False, status=200)
    else:
        # Handle any HTTP method other than GET
        response = JsonResponse(
            {"message": "Invalid method", "status": "405"},
            status=405
        )
        return response


class MyntraStatus(APIView):
    def get(self, request):
        """Check if user is registered in Myntra sheet"""
        try:
            # Get JWT token from cookies
            token = request.COOKIES.get('jwt_token')
            if not token:
                return Response(
                    {"detail": "No token provided"},
                    status=HTTP_401_UNAUTHORIZED
                )
            
            # Decrypt token using COOKIE_ENCRYPTION_SECRET
            cipher = Fernet(settings.COOKIE_ENCRYPTION_SECRET.encode() if isinstance(settings.COOKIE_ENCRYPTION_SECRET, str) else settings.COOKIE_ENCRYPTION_SECRET)
            try:
                decrypted = cipher.decrypt(token.encode() if isinstance(token, str) else token)
                payload = json.loads(decrypted.decode())
            except Exception as e:
                return Response(
                    {"detail": "Invalid token"},
                    status=HTTP_401_UNAUTHORIZED
                )
            
            # Get anwesha_id from payload
            anwesha_id = payload.get('id')
            if not anwesha_id:
                return Response(
                    {"detail": "Invalid token payload"},
                    status=HTTP_401_UNAUTHORIZED
                )
            
            # Check Myntra registration
            myntra_reg = MyntraRegistration.objects.filter(anwesha_user_id=anwesha_id).first()
            
            if myntra_reg:
                return Response({
                    "is_myntra_registered": True,
                    "email": myntra_reg.email,
                    "registered_at": myntra_reg.registered_at,
                    "anwesha_user_id": myntra_reg.anwesha_user_id
                }, status=HTTP_200_OK)
            else:
                return Response({
                    "is_myntra_registered": False,
                    "message": "User not found in Myntra registrations"
                }, status=HTTP_200_OK)
                
        except Exception as e:
            return Response(
                {"detail": f"Error: {str(e)}"},
                status=500
            )
