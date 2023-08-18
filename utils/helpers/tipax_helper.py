import requests
import json
from decouple import config
from zeep.exceptions import ValidationError
from django.utils.translation import gettext as _

from apps.account.models import PostServiceToken, City, State
from utils.exceptions import FailedDependency


class TipaxHelper:
    def login(self):
        post_service_url = config("TIPAX_URL")
        post_service_username = config("TIPAX_USERNAME")
        post_service_password = config("TIPAX_PASSWORD")
        post_service_api_key = config("TIPAX_API_KEY")

        req_data = {
            "username": post_service_username,
            "password": post_service_password,
            "apiKey": post_service_api_key,
        }
        req_header = {
            "accept": "application/json",
            "content-type": "application/json"
        }

        response = requests.post(url=post_service_url + "Account/token/", data=json.dumps(
            req_data), headers=req_header)

        if response.status_code == 200:
            token = response.json()["accessToken"]
            try:
                post_service_token = PostServiceToken.objects.first()
                post_service_token.token = token
                post_service_token.save()

            except:
                PostServiceToken.objects.create(token=token)

        else:
            print(f"login failed code: {response.status_code}")
            raise FailedDependency()

    def get_cities(self):
        post_service_url = config("TIPAX_URL")

        try:
            token = PostServiceToken.objects.first().token

            req_header = {
                "accept": "application/json",
                "content-type": "application/json",
                "Authorization": f"Bearer {token}"
            }

            states_response = requests.get(url=post_service_url + "States/", headers=req_header)
            print(f"state received code: {states_response.status_code}")
            if states_response.status_code == 200:
                existing_states = State.objects.all().values_list("post_service_id", flat=True)
                states = []
                for item in states_response.json():
                    if item["id"] not in existing_states:
                        city = State(
                            name=item["title"],
                            post_service_id=item["id"],
                        )
                        states.append(city)

                State.objects.bulk_create(states)

            elif states_response.status_code == 401:
                raise ValidationError(_('incorrect token'))

            else:
                print(f"get cities failed code :{states_response.status_code}")
                raise FailedDependency()

            cities_response = requests.get(url=post_service_url + "Cities/Plusstate/", headers=req_header)
            print(f"cities received code: {cities_response.status_code}")
            if cities_response.status_code == 200:
                existing_cities = City.objects.all().values_list("post_service_id", flat=True)
                cities = []
                for item in cities_response.json():
                    if item["id"] not in existing_cities:
                        state = State.objects.get(post_service_id=item["stateId"])
                        city = City(
                            name=item["title"],
                            post_service_id=item["id"],
                            state=state
                        )
                        cities.append(city)

                City.objects.bulk_create(cities, batch_size=500)

            elif cities_response.status_code == 401:
                raise ValidationError(_('incorrect token'))

            else:
                print(f"get cities failed code :{cities_response.status_code}")
                raise FailedDependency()

        except Exception as e:
            print(e)
            if isinstance(e, ValidationError) or isinstance(e, AttributeError):
                self.login()
                self.get_cities()

    def get_estimated_price(self, origin_city, destination_city, price):
        post_service_url = config("TIPAX_URL")

        try:
            token = PostServiceToken.objects.first().token

            req_header = {
                "accept": "application/json",
                "content-type": "application/json",
                "Authorization": f"Bearer {token}"
            }

            req_data = {
                "packageInputs": [
                    {
                        "origin": {
                            "cityId": origin_city.post_service_id
                        },
                        "destination": {
                            "cityId": destination_city.post_service_id
                        },
                        "weight": 15,
                        "packageValue": price if price > 2000000 else 2000000,
                        "PackageContentId": 9,
                        "length": 80,
                        "width": 40,
                        "height": 70,
                        "packType": 20
                    }
                ]
            }
            print(req_data)

            pricing_response = requests.post(
                url=post_service_url + "Pricing/",
                headers=req_header,
                data=json.dumps(req_data)
            )
            print(f"pricing received code: {pricing_response.status_code}")
            if pricing_response.status_code == 200:
                print(pricing_response.status_code, pricing_response.json())
                if "regularPlusRate" in pricing_response.json()[0].keys() and pricing_response.json()[0]["regularPlusRate"]:
                    return {
                        "title": pricing_response.json()[0]["regularPlusRate"]["serviceTitle"],
                        "price": pricing_response.json()[0]["regularPlusRate"]["finalPrice"]
                    }
                elif "regularRate" in pricing_response.json()[0].keys() and pricing_response.json()[0]["regularRate"]:
                    return {
                        "title": pricing_response.json()[0]["regularRate"]["serviceTitle"],
                        "price": pricing_response.json()[0]["regularRate"]["finalPrice"]
                    }
                elif "expressRate" in pricing_response.json()[0].keys() and pricing_response.json()[0]["expressRate"]:
                    return {
                        "title": pricing_response.json()[0]["expressRate"]["serviceTitle"],
                        "price": pricing_response.json()[0]["expressRate"]["finalPrice"]
                    }
                else:
                    print("in else")
                    return {"error": "post service failed"}

            elif pricing_response.status_code == 401:
                print(pricing_response.status_code, pricing_response.json())
                raise ValidationError(_('incorrect token'))

            elif pricing_response.status_code == 400:
                print(pricing_response.status_code, pricing_response.json())
                return {"error": "request failed"}

            else:
                print(f"get pricing failed code :{pricing_response.status_code}")
                raise FailedDependency()

        except Exception as e:
            print(e)
            if isinstance(e, ValidationError) or isinstance(e, AttributeError):
                self.login()
                self.get_estimated_price(origin_city=origin_city, destination_city=destination_city, price=price)

    def submit_order(self, origin_address, destination_address, price):
        post_service_url = config("TIPAX_URL")

        try:
            token = PostServiceToken.objects.first().token

            req_header = {
                "accept": "application/json",
                "content-type": "application/json",
                "Authorization": f"Bearer {token}"
            }

            req_data = {
                "packages": [
                    {
                        "origin": {
                            "cityId": origin_address.city.post_service_id,
                            "fullAddress": origin_address.address,
                            "latitude": str(origin_address.latitude),
                            "longitude": str(origin_address.longitude),
                            "beneficiary": {
                                "fullName": origin_address.receiver,
                                "mobile": str(origin_address.phone)
                            }
                        },
                        "destination": {
                            "cityId": destination_address.city.post_service_id,
                            "fullAddress": destination_address.address,
                            "latitude": str(destination_address.latitude),
                            "longitude": str(destination_address.longitude),
                            "beneficiary": {
                                "fullName": destination_address.receiver,
                                "mobile": str(destination_address.phone)
                            }
                        },
                        "weight": 15,
                        "packageValue": price if price > 2000000 else 2000000,
                        "PackageContentId": 9,
                        "length": 80,
                        "width": 40,
                        "height": 70,
                        "packType": 20,
                        "serviceId": 2
                    }
                ]
            }
            print(req_data)

            pricing_response = requests.post(
                url=post_service_url + "Orders/",
                headers=req_header,
                data=json.dumps(req_data)
            )
            print(f"order received code: {pricing_response.status_code}")
            if pricing_response.status_code == 201:
                print(pricing_response.status_code, pricing_response.json())
                return {
                    "tracking_code": pricing_response.json()["trackingCodes"][0],
                    "order_id": pricing_response.json()["orderId"]
                }

            elif pricing_response.status_code == 401:
                print(pricing_response.status_code, pricing_response.json())
                raise ValidationError(_('incorrect token'))

            elif pricing_response.status_code == 400:
                print(pricing_response.status_code, pricing_response.json())
                return {"error": "request failed"}

            else:
                print(f"get pricing failed code :{pricing_response.status_code}")
                raise FailedDependency()


        except Exception as e:
            print(e)
            if isinstance(e, ValidationError) or isinstance(e, AttributeError):
                self.login()
                self.submit_order(origin_address=origin_address, destination_address=destination_address, price=price)
