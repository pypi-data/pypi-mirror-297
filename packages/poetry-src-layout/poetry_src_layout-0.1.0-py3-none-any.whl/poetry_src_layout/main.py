from poetry_src_layout.validator import PhoneNumberValidator

validator = PhoneNumberValidator(api_key="your-api-key-here")
is_valid1 = validator.validate("+15551234")
is_valid2= validator.validate("+12069220880")
is_valid3= validator.validate("2069220880", country_code="US")
print(is_valid1)
print(is_valid2)
print(is_valid3)