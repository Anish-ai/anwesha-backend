from django.http import JsonResponse
from .models import Sponsors, MyntraRegistration
from django.views import View
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import HTTP_401_UNAUTHORIZED, HTTP_404_NOT_FOUND, HTTP_200_OK
import jwt
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
            # Get JWT token from Authorization header (Bearer token) or cookies
            auth_header = request.META.get('HTTP_AUTHORIZATION', '')
            
            if auth_header.startswith('Bearer '):
                # Extract Bearer token
                token = auth_header.replace('Bearer ', '')
            else:
                # Fallback to cookie-based JWT
                token = request.COOKIES.get('jwt_token')
            
            if not token:
                return Response(
                    {"detail": "No token provided. Use Authorization: Bearer <token> header or jwt_token cookie"},
                    status=HTTP_401_UNAUTHORIZED
                )
            
            # Decode JWT token using COOKIE_ENCRYPTION_SECRET (HS256)
            try:
                payload = jwt.decode(token, settings.COOKIE_ENCRYPTION_SECRET, algorithms=['HS256'])
            except jwt.ExpiredSignatureError:
                return Response(
                    {"detail": "Token has expired"},
                    status=HTTP_401_UNAUTHORIZED
                )
            except jwt.InvalidTokenError as e:
                return Response(
                    {"detail": f"Invalid token: {str(e)}"},
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
