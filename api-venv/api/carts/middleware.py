import uuid

class CartIdMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        new_cart_id = None
        if 'cart_id' not in request.COOKIES:
            new_cart_id = str(uuid.uuid4())
            request.cart_id = new_cart_id
        else:
            request.cart_id = request.COOKIES['cart_id']

        response = self.get_response(request)

        if new_cart_id:
            response.set_cookie('cart_id', new_cart_id, max_age=60*60*24*30,  secure=True, samesite='Lax')  # 30 days
        return response
