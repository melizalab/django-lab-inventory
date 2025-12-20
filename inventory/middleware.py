# Authentication Middleware for Enhanced Security
from django.contrib.auth.signals import user_login_failed
from django.core.cache import cache
from django.http import HttpResponse
from django.utils import timezone
import logging

logger = logging.getLogger(__name__)


class LoginAttemptMiddleware:
    """
    Middleware to track and limit failed login attempts.
    Implements account lockout after multiple failed attempts.
    """
    
    MAX_ATTEMPTS = 5
    LOCKOUT_DURATION = 900  # 15 minutes in seconds
    
    def __init__(self, get_response):
        self.get_response = get_response
        # Connect to login failed signal
        user_login_failed.connect(self.login_failed_callback)
    
    def __call__(self, request):
        # Check if user is locked out before processing
        if request.path == '/accounts/login/' and request.method == 'POST':
            ip_address = self.get_client_ip(request)
            username = request.POST.get('username', '')
            
            # Check lockout status
            if self.is_locked_out(ip_address, username):
                logger.warning(f"Blocked login attempt from locked account: {username} ({ip_address})")
                return HttpResponse(
                    "Too many failed login attempts. Account temporarily locked. Please try again in 15 minutes.",
                    status=429
                )
        
        response = self.get_response(request)
        return response
    
    def login_failed_callback(self, sender, credentials, request, **kwargs):
        """Track failed login attempts"""
        ip_address = self.get_client_ip(request)
        username = credentials.get('username', '')
        
        # Increment attempt counter
        self.increment_attempts(ip_address, username)
        
        logger.warning(f"Failed login attempt for user: {username} from IP: {ip_address}")
    
    def get_client_ip(self, request):
        """Get the client's IP address"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
    
    def get_cache_key(self, ip_address, username):
        """Generate cache key for tracking attempts"""
        return f"login_attempts:{ip_address}:{username}"
    
    def increment_attempts(self, ip_address, username):
        """Increment failed login attempts"""
        cache_key = self.get_cache_key(ip_address, username)
        attempts = cache.get(cache_key, 0)
        cache.set(cache_key, attempts + 1, self.LOCKOUT_DURATION)
    
    def is_locked_out(self, ip_address, username):
        """Check if account is locked out"""
        cache_key = self.get_cache_key(ip_address, username)
        attempts = cache.get(cache_key, 0)
        return attempts >= self.MAX_ATTEMPTS
    
    @staticmethod
    def clear_attempts(ip_address, username):
        """Clear failed attempts (called on successful login)"""
        cache_key = f"login_attempts:{ip_address}:{username}"
        cache.delete(cache_key)


class SecurityHeadersMiddleware:
    """
    Add additional security headers to all responses
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        response = self.get_response(request)
        
        # Add security headers
        response['X-Content-Type-Options'] = 'nosniff'
        response['X-Frame-Options'] = 'DENY'
        response['X-XSS-Protection'] = '1; mode=block'
        response['Referrer-Policy'] = 'strict-origin-when-cross-origin'
        response['Permissions-Policy'] = 'geolocation=(), microphone=(), camera=()'
        
        return response
