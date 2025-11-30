from django.core.exceptions import ValidationError
from rest_framework import status, views
from rest_framework.response import Response

from carts.models import Cart

from .serializers import OrderCreateSerializer
from .services import create_order_from_cart


class CheckoutView(views.APIView):
    def get_cart(self, request):
        session_key = request.session.session_key
        if session_key:
            return Cart.objects.filter(
                session_key=session_key, status=Cart.Status.ACTIVE
            ).first()

        return None

    def post(self, request):
        cart = self.get_cart(request)
        if not cart or cart.items.count() == 0:
            return Response(
                {"error": "Cart is empty or not found."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = OrderCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        shipping_data = serializer.validated_data["shipping_address"]
        billing_data = serializer.validated_data.get("billing_address")
        customer_email = serializer.validated_data["email"]

        shipping_data["email"] = customer_email

        try:
            order = create_order_from_cart(
                user=request.user,
                cart=cart,
                shipping_data=shipping_data,
                billing_data=billing_data,
            )
        except ValidationError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(
                {"error": "Unable to create order. Please try again."},
                status=status.HTTP_400_BAD_REQUEST,
            )
