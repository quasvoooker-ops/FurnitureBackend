from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType


class Command(BaseCommand):
    help = 'Creates the Store Staff group with appropriate permissions'

    def handle(self, *args, **kwargs):
        from products.models import Product
        from orders.models import Order

        group, created = Group.objects.get_or_create(name='Store Staff')

        product_ct = ContentType.objects.get_for_model(Product)
        order_ct = ContentType.objects.get_for_model(Order)

        permissions = []

        for codename in ['add_product', 'view_product', 'change_product']:
            perm = Permission.objects.get(content_type=product_ct, codename=codename)
            permissions.append(perm)

        for codename in ['view_order', 'change_order']:
            perm = Permission.objects.get(content_type=order_ct, codename=codename)
            permissions.append(perm)

        group.permissions.set(permissions)

        if created:
            self.stdout.write(self.style.SUCCESS('Store Staff group created with permissions.'))
        else:
            self.stdout.write(self.style.SUCCESS('Store Staff group updated with permissions.'))
