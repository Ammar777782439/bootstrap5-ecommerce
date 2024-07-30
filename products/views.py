from django.shortcuts import get_object_or_404, render
from .models import Product
# Create your views here.
def index(request):
    return render(request,'products\index.html',{'name':Product.objects.all()})

def detail(request, id):
    product = get_object_or_404(Product, id=id)
    ratings = product.ratings.all()  # الحصول على جميع التقييمات المرتبطة بالمنتج
    average_rating = product.get_average_rating()
    return render(request, 'products/product-item-detail.html', {
        'product': product,
        'ratings': ratings,
        'average_rating': average_rating,
    })