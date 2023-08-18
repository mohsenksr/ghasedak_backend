import datetime

from apps.order.models import OrderItem, OrderItemUserData
from utils.helpers.tipax_helper import TipaxHelper


class PostAdaptor:
    def get_cities(self):
        TipaxHelper().get_cities()

    def get_estimated_price(self, shopping_cart):
        prices = {"items": {}, "additional_price": False}
        for order_item in shopping_cart.order_items.all():
            if not order_item.product.post_service_support:
                prices["additional_price"] = True
                prices["items"].update({
                    order_item.id: "POST_SERVICE_NOT_SUPPORTED",
                })
                continue
            try:
                origin_city = order_item.product_price.vendor.main_address.city
            except Exception as e:
                return {"error": "vendor_main_address_error"}

            try:
                destination_city = shopping_cart.user_data.address.city
            except Exception as e:
                return {"error": "customer_address_error"}

            price = order_item.product_price.price / 10
            shipping_price = TipaxHelper().get_estimated_price(
                origin_city=origin_city,
                destination_city=destination_city,
                price=price,
            )
            if not shipping_price or "error" in shipping_price.keys():
                return {"error": "request_error"}
            prices["items"].update({
                order_item.id: shipping_price,
            })

        sum_price = 0
        print(prices)
        for item in prices["items"].values():
            if item != "POST_SERVICE_NOT_SUPPORTED" and "price" in item.keys():
                sum_price += int(item["price"])
        prices.update({"sum": sum_price})

        for order_item_id in prices["items"].keys():
            if prices["items"][order_item_id] == "POST_SERVICE_NOT_SUPPORTED":
                continue
            order_item = OrderItem.objects.get(id=order_item_id)
            if order_item.user_data:
                order_item.user_data.shipping_cost = int(prices["items"][order_item_id]["price"])
                order_item.user_data.save()
            user_data = OrderItemUserData.objects.create(
                shipping_cost=int(prices["items"][order_item_id]["price"]),
                shipping_date=datetime.datetime.now().date(),
                received_date=datetime.datetime.now().date(),
            )
            order_item.user_data = user_data
            order_item.save()

        return prices

    def submit_order(self, order):
        tracking_info = {"items": {}}
        for order_item in order.order_items.all():
            if not order_item.product.post_service_support:
                continue
            try:
                origin_address = order_item.product_price.vendor.main_address
            except Exception as e:
                return {"error": "vendor_main_address_error"}

            try:
                destination_address = order.user_data.address
            except Exception as e:
                return {"error": "customer_address_error"}

            price = order_item.product_price.price / 10
            tracking = TipaxHelper().submit_order(
                origin_address=origin_address,
                destination_address=destination_address,
                price=price,
            )
            if not tracking or "error" in tracking.keys():
                return {"error": "request_error"}
            tracking_info["items"].update({
                order_item.id: tracking,
            })

        for order_item_id in tracking_info["items"].keys():
            order_item = OrderItem.objects.get(id=order_item_id)
            order_item.user_data.details = str(tracking_info["items"][order_item_id])
            order_item.user_data.save()

        return tracking_info
