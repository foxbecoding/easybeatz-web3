from rest_framework.response import Response

class ResponseMixin:
    def view_response(self, message, data, status_code) -> Response:
        """Mixin method to generate view response"""
        return Response(
            {
                "message": message,
                "data": data
            },
            status=status_code
        )
