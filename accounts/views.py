from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.contrib.auth.models import User

# Renders the homepage
def home(request):
    return render(request, 'home.html')

# Renders the privacy policy page
def privacy_policy(request):
    return render(request, 'privacy-policy.html')

# Renders the terms & conditions page
def terms_conditions(request):
    return render(request, 'terms-conditions.html')

# Renders the returns & cancellations page
def returns_cancellations(request):
    return render(request, 'returns-cancellations.html')

# Handles user login — looks up user by email, authenticates,
# logs in the user and returns them to previous page.
def login_view(request):
    if request.user.is_authenticated:
        next_url = request.GET.get('next') or '/'
        return redirect(next_url)
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        try:
            user_obj = User.objects.get(email=email)
            user = authenticate(request, username=user_obj.username, password=password)
        except User.DoesNotExist:
            user = None
        if user:
            # Block login if email not verified
            from allauth.account.models import EmailAddress
            try:
                email_address = EmailAddress.objects.get(user=user, primary=True)
                if not email_address.verified:
                    messages.error(request, 'Please verify your email address before logging in. Check your inbox for the confirmation link.')
                    return render(request, 'accounts/login.html', {'next': request.GET.get('next', '/')})
            except EmailAddress.DoesNotExist:
                # Google OAuth users won't have an EmailAddress record — let them through
                pass
            login(request, user)
            next_url = request.POST.get('next') or '/'
            return redirect(next_url)
        else:
            messages.error(request, 'Invalid email or password.')
    return render(request, 'accounts/login.html', {'next': request.GET.get('next', '/')})

# Handles new user registration — validates email and password,
# creates the user, logs them in and redirects to home.
def register_view(request):
    if request.user.is_authenticated:
        next_url = request.GET.get('next') or '/'
        return redirect(next_url)
    if request.method == 'POST':
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if password1 != password2:
            messages.error(request, 'Passwords do not match.')
            return render(request, 'accounts/register.html', {'next': request.POST.get('next', '/')})

        if User.objects.filter(email=email).exists():
            messages.error(request, 'An account with this email already exists.')
            return render(request, 'accounts/register.html', {'next': request.POST.get('next', '/')})

        if len(password1) < 8:
            messages.error(request, 'Password must be at least 8 characters.')
            return render(request, 'accounts/register.html', {'next': request.POST.get('next', '/')})

        user = User.objects.create_user(username=email, email=email, password=password1)

        # Create allauth EmailAddress record and send confirmation
        from allauth.account.models import EmailAddress
        email_address = EmailAddress.objects.create(
            user=user,
            email=email,
            primary=True,
            verified=False
        )
        email_address.send_confirmation(request)

        messages.info(request, 'Please check your email and click the confirmation link to activate your account.')
        return redirect('account_email_verification_sent')

    return render(request, 'accounts/register.html', {'next': request.GET.get('next', '/')})

# Logs the user out and redirects to home
def logout_view(request):
    logout(request)
    messages.success(request, 'You have been successfully logged out.')
    return redirect('home')