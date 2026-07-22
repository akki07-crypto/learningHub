import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth.models import User

admin_username = "admin"
admin_email = "akki28869@gmail.com"
admin_password = "AdminPassword123"

print("="*60)
print(" CREATING SUPERUSER ADMIN ACCOUNT FOR ELEARN_DB")
print("="*60)

admin_user, created = User.objects.get_or_create(username=admin_username)
admin_user.email = admin_email
admin_user.is_staff = True
admin_user.is_superuser = True
admin_user.set_password(admin_password)
admin_user.save()

if created:
    print(f"[SUCCESS] Superuser '{admin_username}' created successfully in MySQL database!")
else:
    print(f"[SUCCESS] Superuser '{admin_username}' password updated successfully in MySQL database!")

print(f" -> Username : {admin_username}")
print(f" -> Password : {admin_password}")
print(f" -> Admin URL: http://127.0.0.1:8000/admin/")
print("="*60)
