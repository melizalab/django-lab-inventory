# Custom Authentication Backend with Additional Security
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.core.cache import cache
import logging

logger = logging.getLogger(__name__)
User = get_user_model()


class SecureAuthBackend(ModelBackend):
    """
    Enhanced authentication backend with additional security checks
    """
    
    def authenticate(self, request, username=None, password=None, **kwargs):
        """
        Authenticate with additional security validations
        """
        if username is None or password is None:
            return None
        
        # Check for empty credentials
        if not username.strip() or not password.strip():
            logger.warning("Authentication attempt with empty credentials")
            return None
        
        # Check username length to prevent enumeration attacks
        if len(username) > 150:
            logger.warning(f"Authentication attempt with overly long username")
            return None
        
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            # Run the default password hasher to prevent timing attacks
            User().set_password(password)
            logger.warning(f"Authentication attempt for non-existent user: {username}")
            return None
        
        # Check if user account is active
        if not user.is_active:
            logger.warning(f"Authentication attempt for inactive user: {username}")
            return None
        
        # Verify password
        if user.check_password(password):
            logger.info(f"Successful authentication for user: {username}")
            return user
        
        return None
    
    def get_user(self, user_id):
        """
        Get user with caching for performance
        """
        cache_key = f"user_obj:{user_id}"
        user = cache.get(cache_key)
        
        if user is None:
            try:
                user = User.objects.get(pk=user_id)
                # Cache user object for 5 minutes
                cache.set(cache_key, user, 300)
            except User.DoesNotExist:
                return None
        
        return user if user.is_active else None
