#!/usr/bin/env bash
set -o errexit

pip install -r requirements.txt
python manage.py collectstatic --no-input
python manage.py migrate
python manage.py setup_groups
python manage.py seed_products
python manage.py shell -c "
from django.contrib.auth.models import User
user, created = User.objects.get_or_create(username='admin')
user.email = 'admin@example.com'
user.is_staff = True
user.is_superuser = True
user.set_password('admin1234')
user.save()
print('Superuser password set to admin1234')
"
