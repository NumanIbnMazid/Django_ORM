from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
import debug_toolbar
from django.conf import settings
from . import views
from base.views import user_teacher_and_student_list


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.HomeView.as_view(), name='home'),
    path('data/', user_teacher_and_student_list, name='data'),
]


if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        # Django Debug Toolbar
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
    urlpatterns = urlpatterns + \
        static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns = urlpatterns + \
        static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
