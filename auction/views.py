from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils import timezone
from PIL import Image
from .models import *
from .forms import *
import datetime


# Create your views here.
def index(request):
    pictures = {"product": [], "auction": []}
    products = Product.objects.filter(sold=False, is_auction=False).order_by('-published_date')
    for product in products:
        pictures["product"].append(ProductImage.objects.get(pk=product.pictures["pictures"][0])) # 중고 상품 모델로부터 사진을 가져옵니다.
    # 팔리지 않은, 유효기간이 지나지 않은 상품만 보여주도록 설정합니다.
    auction_products = Auction.objects.prefetch_related('product').filter(product__sold=False, expiration_date__gte=timezone.now()).order_by('-product__published_date')
    for product in auction_products:
        pictures["auction"].append(ProductImage.objects.get(pk=product.product.pictures["pictures"][0])) # 경매 상품 모델로부터 사진을 가져옵니다.
    return render(request, 'auction/index.html', {
        'title': '경매장터: 메인 페이지',
        'timezone_now': timezone.now(),
        'products': zip(products, pictures["product"]), # zip으로 product, pictures 바인딩
        'auction_products': zip(auction_products, pictures["auction"]),
    })


def product_detail(request, pk):
    product = Product.objects.get(pk=pk)
    pictures = ProductImage.objects.filter(product=product)
    product.viewer += 1 # 조회수 (세션 검증을 설정하여 조회수 악용 방지 예정)
    product.save()
    if product.is_auction:
        bid_form = BidPublishForm()
        auction = Auction.objects.get(pk=pk)
        bids = Bid.objects.filter(product=product).order_by('-published_date')
        return render(request, 'auction/product_detail.html', {
            'title': "경매장터: " + product.title,
            'timezone_now': timezone.now(),
            'product': product,
            'numbers': [x for x in range(0, len(pictures))], # Carousel indicator를 위한 변수
            'pictures': pictures,
            'auction': auction,
            'bids': bids,
            'minimum_bid': auction.current_price + (product.price * 0.1),
            'bid_form': bid_form,
        })
    else:
        return render(request, 'auction/product_detail.html', {
            'title': "경매장터: " + product.title,
            'timezone_now': timezone.now(),
            'product': product,
            'numbers': [x for x in range(0, len(pictures))],
            'pictures': pictures,
        })


def place_bid(request):
    if not request.user.is_authenticated:
        messages.warning(request, "<strong>경고!</strong> 로그인이 필요한 작업입니다. ", extra_tags="alert-danger")
        return redirect('login')

    if request.method == "POST":
        form = BidPublishForm(request.POST)
        if form.is_valid():
            product = Product.objects.get(pk=request.POST["product_id"])
            auction = Auction.objects.get(pk=request.POST["product_id"])
            minimum_rate = int(round(product.price * 0.1, -3))
            minimum = auction.current_price + minimum_rate
            if int(request.POST["price"]) < minimum: # 시스템이 설정한 최저 입찰가보다 낮은 값이 도출될 경우 (Minimum 무시 공격 대비)
                raise TypeError
            bid = form.save(commit=False)
            bid.published_user = request.user
            bid.product = product
            bid.save()
            auction.bids["bids"].append(bid.pk)
            auction.current_price = bid.price
            auction.save()
        return redirect('product_detail', pk=request.POST["product_id"])


def publish_type(request):
    if not request.user.is_authenticated:
        messages.warning(request, "<strong>경고!</strong> 로그인이 필요한 작업입니다. ", extra_tags="alert-danger")
        return redirect('login')

    return render(request, 'auction/publish_type.html', {'title': '경매장터: 업로드'})


def image_check(file): # 사진 파일 여부 확인 함수
    try:
        image = Image.open(file)
        image.verify()
        return True
    except:
        return False


def publish(request, article_type):
    if not request.user.is_authenticated:
        messages.warning(request, "<strong>경고!</strong> 로그인이 필요한 작업입니다. ", extra_tags="alert-danger")
        return redirect('login')

    if request.method == "POST":
        form = ProductPublishForm(request.POST)
        if form.is_valid():
            article = form.save(commit=False)
            article.published_user = request.user
            article.pictures = {}
            if article_type == "product":
                article.is_auction = False
                article.save()
            elif article_type == "auction":
                article.is_auction = True
                article.save()
                expiration_date = timezone.now() + datetime.timedelta(int(request.POST["expiration_date"]))
                Auction.objects.create(
                    product=article,
                    expiration_date=expiration_date,
                    current_price=article.price,
                    bids={"bids": []}
                )
            picture_list = []
            for f in request.FILES.getlist('picture'): # 유저가 업로드한 사진 리스트를 가져옵니다.
                if image_check(f):
                    image = ProductImage.objects.create(product=article, picture=f) # 사진 한 장당 ProductImage 쿼리 하나
                    picture_list.append(image.pk)
            article.pictures = {"pictures": picture_list} # 추후 최적화를 위해 게시물에 바인딩된 사진의 pk를 JSON으로 저장
            article.save()
            return redirect('product_detail', pk=article.pk)

    else:
        form = ProductPublishForm()
        conditions = Condition.objects.all()
        return render(request, 'auction/publish.html', {'title': '경매장터: 업로드', 'form': form, 'conditions': conditions})
