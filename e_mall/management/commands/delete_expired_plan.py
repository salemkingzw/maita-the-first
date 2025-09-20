from django.core.management.base import BaseCommand
from e_mall.models.userprofile import Subscription

class Command(BaseCommand):
    def handle(self, *args, **options):
        expired_plan=Subscription.objects.filter(is_active=False)
        for items in expired_plan:            
            items.delete()
            print(f"deleted expired plan: {items}")
        if not expired_plan:
            print("no expired plan found")