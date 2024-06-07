# store/password_reset.py

from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import redirect, get_object_or_404, render
from django.contrib import messages
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.views import View
from django.contrib.auth.forms import SetPasswordForm

class PasswordResetRequestView(View):
    def get(self, request):
        # Render the password reset request form
        return render(request, 'password_reset_form.html')

    def post(self, request):
        # Handle form submission
        username = request.POST.get("username")
        if not username:
            messages.error(request, 'Please enter a username.')
            return render(request, 'password_reset_form.html')
        
        if not User.objects.filter(username=username).exists():
            messages.error(request, 'Username does not exist.')
            return render(request, 'password_reset_form.html')
        
        user = get_object_or_404(User, username=username)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)
        return redirect('password_reset_confirm', uidb64=uid, token=token)

class PasswordResetConfirmView(View):
    def get(self, request, uidb64=None, token=None):
        # Ensure both uidb64 and token are provided
        if uidb64 is None or token is None:
            messages.error(request, 'Invalid reset link.')
            return redirect('user-password_reset')

        uid = force_str(urlsafe_base64_decode(uidb64))
        user = get_object_or_404(User, pk=uid)
        
        # Check token validity
        if default_token_generator.check_token(user, token):
            form = SetPasswordForm(user)
            return render(request, 'password_reset_confirm.html', {'form': form})
        else:
            messages.error(request, 'The reset link is no longer valid.')
            return redirect('user-password_reset')

    def post(self, request, uidb64=None, token=None):
        # Ensure both uidb64 and token are provided
        if uidb64 is None or token is None:
            messages.error(request, 'Invalid reset link.')
            return redirect('user-password_reset')

        uid = force_str(urlsafe_base64_decode(uidb64))
        user = get_object_or_404(User, pk=uid)
        
        # Check token validity
        if default_token_generator.check_token(user, token):
            form = SetPasswordForm(user, request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, 'Your password has been reset successfully!')
                return redirect('sign-in')
            else:
                return render(request, 'password_reset_confirm.html', {'form': form})
        else:
            messages.error(request, 'The reset link is no longer valid.')
            return redirect('user-password_reset')
