from .models import Cart


def get_cart_from_request(request, prefetch_items=False):
    cart = None
    session_key = request.session.session_key

    if session_key:
        cart = Cart.objects.filter(
            session_key=session_key, status=Cart.Status.ACTIVE
        ).first()

    if cart and prefetch_items:
        cart = (
            Cart.objects.filter(id=cart.id)
            .prefetch_related(
                "items",
                "items__product_variant",
                "items__product_variant__product",
                "items__product_variant__image",
                "items__product_variant__product__thumbnail",
            )
            .first()
        )

    return cart
