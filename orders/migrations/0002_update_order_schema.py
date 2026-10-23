# Migration to bring orders_order and orders_orderitem tables in line
# with the updated models.py.
#
# Changes from 0001:
#   Order:     customer (FK) -> user (FK), added full_name/email/phone/
#              address/city/postal_code/subtotal/shipping_fee/notes,
#              widened total, updated status choices.
#   OrderItem: product (FK) -> product_id (int), added name/image,
#              price field kept (same column, max_digits unchanged).

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        # ── Order: rename customer FK -> user ────────────────────────

        # 1. Add user FK as nullable (temp related_name to avoid clash)
        migrations.AddField(
            model_name='order',
            name='user',
            field=models.ForeignKey(
                null=True,
                blank=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name='orders_v2',
                to=settings.AUTH_USER_MODEL,
            ),
        ),

        # 2. Populate user_id from customer_id
        migrations.RunSQL(
            sql='UPDATE "orders_order" SET "user_id" = "customer_id";',
            reverse_sql=migrations.RunSQL.noop,
        ),

        # 3. Remove old customer FK (this also removes related_name='orders')
        migrations.RemoveField(
            model_name='order',
            name='customer',
        ),

        # 4. Make user non-nullable and set the final related_name
        migrations.AlterField(
            model_name='order',
            name='user',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name='orders',
                to=settings.AUTH_USER_MODEL,
            ),
        ),

        # ── Order: add missing columns ───────────────────────────────

        migrations.AddField(
            model_name='order',
            name='full_name',
            field=models.CharField(max_length=200, default=''),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='order',
            name='email',
            field=models.EmailField(default=''),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='order',
            name='phone',
            field=models.CharField(max_length=30, default=''),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='order',
            name='address',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='order',
            name='city',
            field=models.CharField(max_length=100, default=''),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='order',
            name='postal_code',
            field=models.CharField(max_length=20, default=''),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='order',
            name='subtotal',
            field=models.DecimalField(decimal_places=2, max_digits=12, default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='order',
            name='shipping_fee',
            field=models.DecimalField(decimal_places=2, max_digits=8, default=0),
        ),
        migrations.AddField(
            model_name='order',
            name='notes',
            field=models.TextField(blank=True, default=''),
        ),

        # Widen total and update status choices
        migrations.AlterField(
            model_name='order',
            name='total',
            field=models.DecimalField(decimal_places=2, max_digits=12),
        ),
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(
                choices=[
                    ('pending', 'Pending'),
                    ('confirmed', 'Confirmed'),
                    ('processing', 'Processing'),
                    ('shipped', 'Shipped'),
                    ('delivered', 'Delivered'),
                    ('cancelled', 'Cancelled'),
                ],
                default='pending',
                max_length=20,
            ),
        ),

        # ── OrderItem: replace product FK with product_id int ────────

        # Add new fields first
        migrations.AddField(
            model_name='orderitem',
            name='product_id_new',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='orderitem',
            name='name',
            field=models.CharField(max_length=200, default=''),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='orderitem',
            name='image',
            field=models.URLField(blank=True, max_length=500, default=''),
            preserve_default=False,
        ),

        # Copy the FK integer value into product_id_new
        # Django stores ForeignKey 'product' as column 'product_id'
        migrations.RunSQL(
            sql='UPDATE "orders_orderitem" SET "product_id_new" = "product_id";',
            reverse_sql=migrations.RunSQL.noop,
        ),

        # Remove the product FK (drops the product_id column)
        migrations.RemoveField(
            model_name='orderitem',
            name='product',
        ),

        # Rename product_id_new -> product_id
        migrations.RenameField(
            model_name='orderitem',
            old_name='product_id_new',
            new_name='product_id',
        ),
    ]
