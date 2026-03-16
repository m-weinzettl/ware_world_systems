from email_validator import validate_email, EmailNotValidError

class Validator:
    def validate_mail(self, email_to_check):
        try:
            email_info = validate_email(email_to_check, check_deliverability=False)
            return True, email_info.normalized
        except EmailNotValidError as e:
            return False, str(e)
