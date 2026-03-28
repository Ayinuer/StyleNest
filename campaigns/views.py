from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from accounts.models import ShopOwnerProfile
from .models import Campaign


@login_required
def campaign_list(request):
    shop_profile = ShopOwnerProfile.objects.filter(user=request.user).first()
    campaigns = Campaign.objects.filter(shop=shop_profile).order_by('-created_at')

    return render(request, 'campaigns/campaign_list.html', {
        'campaigns': campaigns,
        'shop_profile': shop_profile,
    })