from .models import Colum

nav_display_columns = Colum.objects.filter(nav_display=True)


def nav_column(request):
    return {'nav_display_columns': nav_display_columns}