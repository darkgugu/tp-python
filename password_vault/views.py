from django.shortcuts import render
from .encryption import encrypt_password, decrypt_password

# Create your views here.
from django.shortcuts import render, get_object_or_404, redirect
from .models import PasswordEntry
from .forms import PasswordEntryForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .models import PasswordShareLink
from django.utils import timezone
from datetime import timedelta
from .forms import SignUpForm
from django.contrib.auth import login
from django.http import JsonResponse
from .utils import generate_strong_password
from django.contrib import messages
from django.contrib.auth import authenticate


@login_required
def password_list(request):
    passwords = PasswordEntry.objects.filter(user=request.user)
    return render(request, 'password_vault/password_list.html', {'passwords': passwords})

@login_required
def password_detail(request, pk):
    password = get_object_or_404(PasswordEntry, pk=pk, user=request.user)
    decrypted_password = decrypt_password(password.encrypted_password)
    return render(request, 'password_vault/password_detail.html', {
        'password': password,
        'decrypted_password': decrypted_password,
    })

@login_required
def password_add(request):
    if request.method == "POST":
        form = PasswordEntryForm(request.POST)
        if form.is_valid():
            password_entry = form.save(commit=False)
            password_entry.user = request.user
            password_entry.encrypted_password = encrypt_password(form.cleaned_data['password'])
            password_entry.save()
            return redirect('password_vault:password_list')
    else:
        form = PasswordEntryForm()
    return render(request, 'password_vault/password_form.html', {'form': form})

@login_required
def password_delete(request, pk):
    password = get_object_or_404(PasswordEntry, pk=pk, user=request.user)
    if request.method == "POST":
        password.delete()
        return redirect('password_vault:password_list')
    return render(request, 'password_vault/password_confirm_delete.html', {'password': password})

@login_required
def generate_share_link(request, pk):
    password = get_object_or_404(PasswordEntry, pk=pk, user=request.user)
    share_link = PasswordShareLink.objects.create(
        password_entry=password,
        expires_at=timezone.now() + timedelta(hours=1)
    )
    share_url = request.build_absolute_uri(
        f"/share/{share_link.token}/"
    )
    return render(request, 'password_vault/share_link_created.html', {
        'share_url': share_url,
        'expires_at': share_link.expires_at,
    })

def view_shared_password(request, token):
    share_link = get_object_or_404(PasswordShareLink, token=token)
    if not share_link.is_valid():
        return HttpResponse("Lien invalide ou expiré.")
    decrypted_password = decrypt_password(share_link.password_entry.encrypted_password)
    share_link.used = True
    share_link.save()
    return render(request, 'password_vault/view_shared_password.html', {
        'site_name': share_link.password_entry.site_name,
        'login': share_link.password_entry.login,
        'decrypted_password': decrypted_password,
    })

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, "Votre compte a été créé avec succès. Vous pouvez maintenant vous connecter.")
            return redirect('login')  # redirection vers la page de login
    else:
        form = SignUpForm()
    return render(request, 'password_vault/signup.html', {'form': form})

@login_required
def generate_password(request):
    password = generate_strong_password()
    return JsonResponse({'password': password})
