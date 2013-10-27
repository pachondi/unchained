from south.modelsinspector import timezone
<<<<<<< HEAD:app/users/utils.py
from app.users.models import SiteUser
from app.relationships.models import ConnectionRequest

=======
from app.users.models import ConnectionRequest, SiteUser
>>>>>>> master:app/users/utils.py

def date_in_words(date):        
        now = timezone.now()
        diff = now - date
        second_diff = diff.seconds
        day_diff = diff.days
    
        if day_diff < 0:
            return ''
    
        if day_diff == 0:
            if second_diff < 10:
                return "just now"
            if second_diff < 60:
                return str(second_diff) + " seconds ago"
            if second_diff < 120:
                return  "a minute ago"
            if second_diff < 3600:
                return str( second_diff / 60 ) + " minutes ago"
            if second_diff < 7200:
                return "an hour ago"
            if second_diff < 86400:
                return str( second_diff / 3600 ) + " hours ago"
        if day_diff == 1:
            return "Yesterday"
        if day_diff < 7:
            return str(day_diff) + " days ago"
        if day_diff < 31:
            return str(day_diff/7) + " weeks ago"
        if day_diff < 365:
            return str(day_diff/30) + " months ago"
        return str(day_diff/365) + " years ago"

def get_connection_suggestion(user):        
        connections = user.connections.all()
        known_users = list()
        
        for u in SiteUser.objects.all():
            if not connections.filter(pk=u).exists() and not ConnectionRequest.objects.filter(status='R',to_user=user, from_user=u).exists() and not ConnectionRequest.objects.filter(status='R',from_user=user, to_user=u).exists() and not u == user:               
                known_users.append(u) 
        
        return known_users