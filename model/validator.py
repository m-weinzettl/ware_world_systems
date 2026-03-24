from email_validator import validate_email, EmailNotValidError
from zxcvbn import zxcvbn


class Validator:
    @staticmethod
    def validate_mail(email_to_check):
        try:
            email_info = validate_email(email_to_check, check_deliverability=False)
            return True, email_info.normalized
        except (EmailNotValidError, ValueError) as e:
            return False, str(e)

    @staticmethod
    def validate_password(password_to_check):
        if not password_to_check or len(password_to_check) < 8:
            return False, "Das Passwort muss mindestens 8 Zeichen lang sein."

        results = zxcvbn(password_to_check)
        score = results["score"]  # 0 schwach bis 4 stark

        if score < 3:
            feedback_data = results.get("feedback", {})
            warning = feedback_data.get("warning", "")
            suggestions = feedback_data.get("suggestions", [])

            error_msg = f"Passwort zu schwach (Stufe {score}/4). "
            if warning:
                error_msg += f"{warning} "
            if suggestions:
                error_msg += f"Tipp: {suggestions[0]}"

            return False, error_msg.strip()

        return True, password_to_check