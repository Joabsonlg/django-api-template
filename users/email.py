from djoser import email


class PasswordResetEmail(email.PasswordResetEmail):
    template_name = 'users/email/password_reset.html'
