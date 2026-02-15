import structlog
from django.contrib.auth import get_user_model
from django.db.models import Count, Q
from django.db.models.functions import TruncMonth
from django.utils import timezone
from wingman.constants import CACHE_TTL_DASHBOARD_STATS
from chat.models import Message

User = get_user_model()
logger = structlog.get_logger(__name__)

class DashboardService:
    @staticmethod
    def get_analytics():
        user_stats = User.objects.aggregate(
            total=Count('id'),
            premium=Count('id', filter=Q(is_premium=True)),
            active=Count('id', filter=Q(is_active=True))
        )
        total_users = user_stats['total']
        premium_users = user_stats['premium']
        free_users = total_users - premium_users
        active_today = User.objects.filter(last_login__date=timezone.now().date()).count()
        conversion_rate = round((premium_users / total_users * 100), 2) if total_users > 0 else 0
        
        twelve_months_ago = timezone.now() - timezone.timedelta(days=365)
        monthly_data = (
            User.objects.filter(date_joined__gte=twelve_months_ago)
            .annotate(month=TruncMonth('date_joined'))
            .values('month')
            .annotate(count=Count('id'))
            .order_by('month')
        )
        graph_data = [{"month": e['month'].strftime('%b %Y'), "count": e['count']} for e in monthly_data if e['month']]

        recent_users_qs = (
            User.objects
            .annotate(usage_count=Count('message', filter=Q(message__is_ai=False)))
            .order_by('-date_joined')[:5]
        )
        
        recent_users = []
        for user in recent_users_qs:
            user_data = {
                "id": user.id,
                "name": user.name or "",
                "email": user.email,
                "profile_image": user.profile_image.url if user.profile_image else None,
                "subscription": "Premium" if user.is_premium else "Free",
                "usage_count": user.usage_count,
                "status": "Active" if user.is_active else "Inactive",
            }
            recent_users.append(user_data)

        return {
            "total_users": total_users, "active_today": active_today,
            "premium_users": premium_users, "free_users": free_users,
            "conversion_rate": conversion_rate, "graph_data": graph_data,
            "recent_users": recent_users
        }