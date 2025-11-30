from rest_framework import serializers
from django.utils.translation import gettext_lazy as _
from .models import Cart, CartItem
from products.models import ProductVariant


class CartVariantSerializer(serializers.ModelSerializer):
    product_title = serializers.CharField(source="product.title", read_only=True)
    product_slug = serializers.CharField(source="product.slug", read_only=True)
    image = serializers.SerializerMethodField()

    class Meta:
        model = ProductVariant
        fields = [
            "id",
            "sku",
            "product_title",
            "product_slug",
            "price",
            "image",
            "attributes",
        ]

    def get_image(self, obj):
        if obj.image:
            request = self.context.get("request")
            return (
                request.build_absolute_uri(obj.image.url) if request else obj.image.url
            )

        if obj.product.thumbnail:
            request = self.context.get("request")
            return (
                request.build_absolute_uri(obj.product.thumbnail.url)
                if request
                else obj.product.thumbnail.url
            )

        return None


class CartItemSerializer(serializers.ModelSerializer):
    variant = CartVariantSerializer(source="product_variant", read_only=True)
    total_price = serializers.DecimalField(
        max_digits=10, decimal_places=2, read_only=True
    )

    class Meta:
        model = CartItem
        fields = ["id", "variant", "quantity", "total_price"]


class CartItemAddSerializer(serializers.ModelSerializer):
    product_variant_id = serializers.IntegerField()
    quantity = serializers.IntegerField(min_value=1)

    class Meta:
        model = CartItem
        fields = ["product_variant_id", "quantity"]

    def validate(self, data):
        variant_id = data.get("product_variant_id")
        quantity = data.get("quantity")

        try:
            variant = ProductVariant.objects.get(id=variant_id)
        except ProductVariant.DoesNotExist:
            raise serializers.ValidationError(
                {"product_variant_id": _("Product not found.")}
            )

        if quantity > variant.stock_quantity:
            raise serializers.ValidationError(
                {
                    "quantity": _(
                        f"Only {variant.stock_quantity} items available in stock."
                    )
                }
            )

        return data


class CartItemUpdateSerializer(serializers.Serializer):
    quantity = serializers.IntegerField(min_value=1)


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    total_price = serializers.DecimalField(
        max_digits=10, decimal_places=2, read_only=True
    )
    total_items = serializers.IntegerField(read_only=True)

    class Meta:
        model = Cart
        fields = ["id", "session_key", "status", "items", "total_price", "total_items"]
        read_only_fields = ["status", "session_key"]
