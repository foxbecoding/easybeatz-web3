import uuid

class CartIdMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if 'cart_id' not in request.COOKIES:
            request.cart_id = str(uuid.uuid4())
        else:
            request.cart_id = request.COOKIES['cart_id']
        return self.get_response(request)
