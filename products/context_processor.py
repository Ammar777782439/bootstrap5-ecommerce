from typing import Counter
from urllib import request
from .models import CartItem,ShoppingCart


def global_context(requset):
     if requset.user.is_authenticated:
      user_id=requset.user
      shoppingCart=ShoppingCart.objects.filter(user=user_id).first()
      cartItem=CartItem.objects.filter(cart=shoppingCart)
      
      counter_pro=[item.product for item in cartItem ]
      counter=Counter(counter_pro)
      s=sum(counter.values())

      
      return {'global_data': s}
     else:
        return {'global_data':None}
      