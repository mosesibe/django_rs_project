from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.shortcuts import render, get_object_or_404
from .models import Listing
from .choices import state_choices, bedroom_choices, price_choices



def index(request):
    listings = Listing.objects.order_by('-list_date').filter(is_published=True)
    paginator = Paginator(listings, 6)  # Show 25 contacts per page

    page = request.GET.get('page')
    lists = paginator.get_page(page)

    context = {
        'listings': lists
    }
    return render(request, 'listings/listings.html', context)
    # return render(request, 'listings/listings.html', context)

def listing(request, listing_id):
    listing = get_object_or_404(Listing, pk=listing_id)

    context = {
        'listing': listing
    }
    return render(request, 'listings/listing.html', context)

def search(request):

    # query fro search filtering
    queryset_list = Listing.objects.order_by('-list_date')

    # Search by Keywords
    if 'keywords' in request.GET:
            keywords = request.GET['keywords']
            if keywords:
                queryset_list = queryset_list.filter(description__icontains=keywords)

    # Search by City
    if 'city' in request.GET:
        city = request.GET['city']
        if city:
            queryset_list = queryset_list.filter(city__iexact=city)

    # Search by State
    if 'state' in request.GET:
        state = request.GET['state']
        if state:
            queryset_list = queryset_list.filter(state__iexact=state)

    # Search by Bedrooms
    if 'bedrooms' in request.GET:
        bedrooms = request.GET['bedrooms']
        if bedrooms:
            #lte = less than or equal to
            queryset_list = queryset_list.filter(bedrooms__lte=bedrooms)

    # Search by Price
    if 'price' in request.GET:
        price = request.GET['price']
        if price:
            queryset_list = queryset_list.filter(price__lte=price)


    context ={
        'state_choices': state_choices,
        'bedroom_choices': bedroom_choices,
        'price_choices': price_choices,
        'listings': queryset_list,
        #This values will pull in values to keep on the search field in search results
        'values': request.GET
    }
    return render(request, 'listings/search.html', context)
