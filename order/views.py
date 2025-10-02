from rest_framework import status, generics, permissions
from rest_framework.response import Response
from rest_framework.exceptions import NotFound

from .serializers import CartItemSerializer, CartSerializer, OrderSerializer, OrderItemSerializer
from .models import Cart, CartItem, Order, OrderItem


# Cart Views
class CartDetailView(generics.RetrieveAPIView):
    serializer_class = CartSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        cart, _ = Cart.objects.get_or_create(user=self.request.user)
        return cart


class CartAddItemView(generics.CreateAPIView):
    serializer_class = CartItemSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        cart, _ = Cart.objects.get_or_create(user=self.request.user)
        serializer.save(cart=cart)


class CartUpdateItemView(generics.UpdateAPIView):
    serializer_class = CartItemSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'slug'

    def get_queryset(self):
        return CartItem.objects.filter(cart__user=self.request.user)


class CartDeleteItemView(generics.DestroyAPIView):
    serializer_class = CartItemSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'slug'

    def get_queryset(self):
        return CartItem.objects.filter(cart__user=self.request.user)


class CheckoutView(generics.CreateAPIView):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        cart, _ = Cart.objects.get_or_create(user=request.user)
        cart_items = cart.order_items.select_related('property')

        if not cart_items.exists():
            return Response({'detail': 'Your cart is empty.'}, status=status.HTTP_400_BAD_REQUEST)

        order, created = Order.objects.get_or_create(user=request.user)
        if not created:
            order.order_items.all().delete()

        order_items = []
        for cart_item in cart_items:
            order_items.append(
                OrderItem(
                    order=order,
                    property=cart_item.property,
                    quantity=cart_item.quantity,
                )
            )
        OrderItem.objects.bulk_create(order_items)

        cart_items.delete()

        serializer = self.get_serializer(order)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


# Order Views
class OrderView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = OrderSerializer

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)


class OrderDetailView(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = OrderSerializer
    lookup_field = 'slug'

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)


class CancelOrderView(generics.DestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = OrderSerializer
    lookup_field = 'slug'

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)


class OrderItemListView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = OrderItemSerializer

    def get_queryset(self):
        slug = self.kwargs['slug']
        try:
            order = Order.objects.get(slug=slug, user=self.request.user)
        except Order.DoesNotExist:
            raise NotFound('Order not found.')
        return order.order_items.select_related('property')


class OrderItemDetailView(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = OrderItemSerializer
    lookup_field = 'slug'

    def get_queryset(self):
        return OrderItem.objects.filter(order__user=self.request.user).select_related('property')
