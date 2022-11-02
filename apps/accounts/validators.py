from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _


class CustomPasswordValidator():

    def validate(self, password, user=None):
        special_characters = "[~\!@#\$%\^&\*\(\)_\+{}\":;'\[\]]"
        if not any(char.isdigit() for char in password) or not any(char.isalpha() for char in password) or not any(char in special_characters for char in password):
            raise ValidationError(_('Passwords must contain letters, numbers and special characters.'))
        if len(password) < 8:
            raise ValidationError(_('Password must contain at least 8 characters'), code="password_too_short")
    def get_help_text(self):
        return ""

phone_regex_pattern = RegexValidator(regex=r'^\+[0-9]*$', message='Phone number must be in this format: +1234567890')

# class CustomPasswordValidator():

#     def __init__(self, min_length=1):
#         self.min_length = min_length

#     def validate(self, password, user=None):
#         special_characters = "[~\!@#\$%\^&\*\(\)_\+{}\":;'\[\]]"
#         if not any(char.isdigit() for char in password):
#             raise ValidationError(_('Password must contain at least %(min_length)d digit.') % {'min_length': self.min_length})
#         if not any(char.isalpha() for char in password):
#             raise ValidationError(_('Password must contain at least %(min_length)d letter.') % {'min_length': self.min_length})
#         if not any(char in special_characters for char in password):
#             raise ValidationError(_('Password must contain at least %(min_length)d special character.') % {'min_length': self.min_length})
#         if len(password) < 8:
#             raise ValidationError(_('Password must contain at least characters'), code="password_too_short")

#     def get_help_text(self):
#         return ""
