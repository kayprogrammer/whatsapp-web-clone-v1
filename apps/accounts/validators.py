from django.core.validators import RegexValidator

phone_regex_pattern = RegexValidator(regex=r'^\+[0-9]*$', message='Phone number must be in this format: +1234567890')