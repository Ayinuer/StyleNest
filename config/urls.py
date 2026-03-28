from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', include('store.urls')),
    path('accounts/', include('accounts.urls')),
    path('cart/', include('carts.urls')),

    path('subscribers/', include('subscribers.urls')),
    path('campaigns/', include('campaigns.urls')),
    path('billing/', include('billing.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)