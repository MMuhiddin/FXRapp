from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout  # Barcha kerakli funksiyalar import qilindi
from .models import Course, Resource, QuizQuestion


# --- Bosh sahifa ---
def index(request):
    return render(request, 'index.html')


# --- Login/Register Sahifasi ---
def login_register_view(request):
    return render(request, 'login_register.html')

from django.shortcuts import render, redirect
# ... boshqa importlar ...
from django.contrib.auth.decorators import login_required # <--- YUQORIDAN QO'SHING

# ... boshqa view funksiyalar ...

# --- Dashboard Sahifasi ---
@login_required(login_url='login_register') # Tizimga kirmagan bo'lsa, login sahifasiga qaytaradi
def dashboard_view(request):
    # Bu yerda request.user orqali foydalanuvchi ma'lumotlari mavjud bo'ladi
    return render(request, 'dashboard.html')

# ... pastda login_user va register_user funksiyalari qolsin.


# --- Dashboard Sahifasi ---

@login_required(login_url='login_register')
def dashboard_view(request):
    # Bazadan ma'lumotlarni sanaymiz (agar modellar mavjud bo'lsa)
    # Agar hali ma'lumot kiritilmagan bo'lsa, 0 chiqadi
    context = {
        'video_count': Course.objects.filter(is_active=True).count(),
        'book_count': Resource.objects.filter(type='book').count(),
        'quiz_count': QuizQuestion.objects.filter(is_published=True).count(),
    }
    return render(request, 'dashboard.html', context)


# --- Registration Logikasi ---
def register_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Bu foydalanuvchi nomi band.")
            return redirect('login_register')

        try:
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password
            )
            user.save()

            # Ro'yxatdan o'tgandan keyin avtomatik tizimga kiritish
            new_user = authenticate(request, username=username, password=password)

            if new_user is not None:
                login(request, new_user)
                messages.success(request, f"Xush kelibsiz, {username}! Ro'yxatdan o'tish muvaffaqiyatli yakunlandi.")
                return redirect('dashboard')
            else:
                messages.warning(request, "Avtomatik kirishda xatolik. Iltimos, qo'lda kiring.")
                return redirect('login_register')

        except Exception as e:
            messages.error(request, "Ro'yxatdan o'tishda xatolik yuz berdi.")
            return redirect('login_register')

    return redirect('login_register')


# --- LOGIN LOGIKASI (Yangi qo'shilgan) ---
def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Authenticate: Ma'lumotlarni tekshirish
        user = authenticate(request, username=username, password=password)

        if user is not None:
            # Muvaffaqiyatli: Session ochish va Dashboardga yo'naltirish
            login(request, user)
            messages.success(request, f"Xush kelibsiz, {username}!")
            return redirect('dashboard')
        else:
            # Xatolik: Xato xabarini ko'rsatish
            messages.error(request, "Login yoki parol noto'g'ri kiritildi.")
            return redirect('login_register')

    return redirect('login_register')


# --- LOGOUT LOGIKASI (Yangi qo'shilgan) ---
def logout_user(request):
    logout(request)
    messages.info(request, "Tizimdan muvaffaqiyatli chiqdingiz.")
    return redirect('login_register')


# frxapp/views.py ichiga qo'shing

@login_required(login_url='login_register')
def video_lessons_view(request):
    # Barcha aktiv kurslarni olib kelamiz
    courses = Course.objects.filter(is_active=True)

    context = {
        'courses': courses
    }
    return render(request, 'video_lessons.html', context)


# frxapp/views.py ichiga (pastga) qo'shing

@login_required(login_url='login_register')
def books_view(request):
    # 'book' turidagi barcha resurslarni olib kelamiz
    books = Resource.objects.filter(type='book')

    context = {
        'books': books
    }
    return render(request, 'books.html', context)