import logging

from carts.models import Cart

logger = logging.getLogger(__name__)


class AssignCartMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not request.session.session_key:
            request.session.save()

        cart, created = Cart.objects.get_or_create(
            session_key=request.session.session_key,
            status=Cart.Status.ACTIVE,
        )

        request.cart = cart

        logger.debug(
            f"Assigned Cart ID: {cart.id} to Session Key: {request.session.session_key}. Cart created: {created}"
        )

        response = self.get_response(request)
        return response
