from rest_framework.exceptions import APIException
from rest_framework import status

class CoordinatesNotFound(APIException):
    status_code=status.HTTP_400_BAD_REQUEST
    default_detail = 'Latitude and Longitude are not provided when filtering with distance.'
    default_code = 'coordinates_not_provided'