from datetime import timedelta

from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils import timezone
from six import text_type


class AccountActivationTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        expiry_duration = timedelta(days=1)  # Token expires after 1 day
        expiry_date = timestamp + expiry_duration.total_seconds()  # Add seconds instead of timedelta
        return (
                text_type(user.pk) + text_type(timestamp) +
                text_type(expiry_date) + text_type(user.is_active)
        )


account_activation_token = AccountActivationTokenGenerator()
