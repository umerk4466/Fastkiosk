from django import template
register = template.Library()

from ..models import Service

# all_services_categories.html
@register.filter
def services_numb_by_cat(custom_tags,id):
    service_num = Service.objects.filter(category__id=id).count()
    return service_num

# register filter
register.filter('services_numb_by_cat', services_numb_by_cat)

@register.filter
def get_services_by_cat_id(custom_tags,id):
    services =  Service.objects.filter(category__id=id)
    return services

register.filter('get_services_by_cat_id', get_services_by_cat_id)


# specific_service.html
@register.filter
def get_user_services(custom_tags,username):
    services =  Service.objects.filter(user__username=username)
    return services

register.filter('get_user_services', get_user_services)