from django.conf import settings
from shop.models import Gadget

class Basket:
    def __init__(self, request):
        self.session = request.session
        basket = self.session.get(settings.BASKET_SESSION_ID)
        if not basket:
            basket = self.session[settings.BASKET_SESSION_ID] = {}
        self.basket = basket

    def save(self):
        self.session[settings.BASKET_SESSION_ID] = self.basket
        self.session.modified = True

    def add(self, product_id):
        product = Gadget.objects.get(pk=product_id)
        product_id = str(product_id)
        if product_id not in self.basket:
            self.basket[product_id] = {
                'id': product.pk,
                'name' : product.name,
                'count_prod': 1,
                'price_prod': product.price,
                'sum': 0
            }
        else:
            print('Зашли в Элсы!!!')
            self.basket[product_id]['count_prod'] = int(self.basket[product_id]['count_prod']) + 1
        
        self.basket[product_id]['sum'] = self.basket[product_id]['count_prod'] * self.basket[product_id]['price_prod']
        self.save()

    def remove(self, product):
        prod_pk = str(product.pk)

        if prod_pk in self.basket:
            del self.basket[prod_pk]
            self.save()

    def get_total_price(self):
        return sum(float(item['price_prod']) * int(item['count_prod']) for item in self.basket.values())

    def clear(self):
        del self.session[settings.BASKET_SESSION_ID]
        self.session.modified = True

    def __len__(self):
        return sum(int(item['count_prod']) for item in self.basket.values())

    def __iter__(self):
        list_prod_pk = self.basket.keys()

        list_prod_obj = Gadget.objects.filter(pk__in=list_prod_pk)

        basket = self.basket.copy()

        for prod_obj in list_prod_obj:
            basket[str(prod_obj.pk)]['phone'] = prod_obj

        for item in basket.values():
            item['total_price'] = float(item['price_prod']) * int(item['count_prod'])
            yield item
