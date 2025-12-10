from django.db import models
from django.contrib.auth.models import User


# --- 1. KURS STRUKTURASI ---
class Course(models.Model):
    title = models.CharField(max_length=200, verbose_name="Kurs nomi")
    description = models.TextField(verbose_name="Tavsif")
    is_active = models.BooleanField(default=True, verbose_name="Aktiv")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Kurs"
        verbose_name_plural = "1. Kurslar"


class Lesson(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='lessons', verbose_name="Kurs")
    title = models.CharField(max_length=200, verbose_name="Dars nomi")
    video_url = models.URLField(blank=True, null=True, verbose_name="Video havola (YouTube/Vimeo)")
    order = models.PositiveIntegerField(verbose_name="Tartib raqami")

    def __str__(self):
        return f"{self.course.title} - {self.title}"

    class Meta:
        ordering = ['order']
        verbose_name = "Dars"
        verbose_name_plural = "2. Darsliklar"


# --- 2. KITOB VA RESURSLAR ---
class Resource(models.Model):
    title = models.CharField(max_length=200, verbose_name="Resurs nomi")
    file = models.FileField(upload_to='resources/files/', verbose_name="Fayl (PDF/EPUB)")
    type = models.CharField(max_length=50, choices=[('book', 'Kitob'), ('guide', 'Qo\'llanma')], default='book',
                            verbose_name="Turi")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "O'quv resursi"
        verbose_name_plural = "3. Kitoblar va Resurslar"


# --- 3. QISQA SAVOL-JAVOBLAR (FAQ) ---
class FAQ(models.Model):
    question = models.CharField(max_length=255, verbose_name="Savol")
    answer = models.TextField(verbose_name="Javob")
    is_published = models.BooleanField(default=True, verbose_name="Nashr etilgan")

    def __str__(self):
        return self.question[:50]

    class Meta:
        verbose_name = "Savol-Javob (FAQ)"
        verbose_name_plural = "4. Savol-Javoblar"


# --- 4. ADMIN BILAN BOG'LANISH ---
class ContactMessage(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Foydalanuvchi")
    email = models.EmailField(verbose_name="Email")
    subject = models.CharField(max_length=150, verbose_name="Mavzu")
    message = models.TextField(verbose_name="Xabar matni")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Yuborilgan vaqt")
    is_resolved = models.BooleanField(default=False, verbose_name="Hal etildi")

    def __str__(self):
        return f"Xabar: {self.subject} - {self.email}"

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Murojaat xabari"
        verbose_name_plural = "5. Admin bilan bog'lanish (Murojaatlar)"


# --- 5. KALKULYATOR STRATEGIYASI (Sozlamalar) ---
class CalculatorConfig(models.Model):
    name = models.CharField(max_length=100, default="Asosiy Strategiya Sozlamalari")
    max_risk_percent = models.DecimalField(max_digits=5, decimal_places=2, default=1.0,
                                           verbose_name="Maksimal Risk (%)")
    min_trade_size = models.IntegerField(default=10, verbose_name="Minimal Savdo Hajmi")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Strategiya Sozlamasi"
        verbose_name_plural = "6. Kalkulyator Strategiyasi"
        # Bitta yozuvdan ko'p bo'lmasligi uchun cheklov
        unique_together = ('name',)


# ... (Course, Lesson, Resource, FAQ, ContactMessage, CalculatorConfig turaversin) ...

# --- 7. SAVOL-JAVOB TESTLARI ---
# Javob variantlari (A, B, C)
CHOICES = (
    ('A', 'A'),
    ('B', 'B'),
    ('C', 'C'),
)


class QuizQuestion(models.Model):
    # Savol uchun rasm joylash
    image = models.ImageField(upload_to='quizzes/images/', verbose_name="Savol Rasmi (Diagramma)",
                              help_text="Savol uchun grafik yoki diagramma yuklang")

    # Savol matni (rasm qo'shilsa ham, qisqa matn kerak bo'lishi mumkin)
    question_text = models.CharField(max_length=500, verbose_name="Savol matni (ixtiyoriy)", blank=True, null=True)

    # Javob variantlari
    option_a = models.CharField(max_length=255, verbose_name="Variant A")
    option_b = models.CharField(max_length=255, verbose_name="Variant B")
    option_c = models.CharField(max_length=255,
                                verbose_name="Variant C (Agar A,B varianti bo'lsa, buni bo'sh qoldiring)", blank=True,
                                null=True)

    # To'g'ri javobni tanlash
    correct_answer = models.CharField(max_length=1, choices=CHOICES, verbose_name="To'g'ri javob")

    # Nechta variantni ko'rsatish (2 variant yoki 3 variant)
    num_options = models.IntegerField(choices=[(2, 'A va B'), (3, 'A, B va C')], default=3,
                                      verbose_name="Variantlar soni")

    is_published = models.BooleanField(default=True, verbose_name="Nashr etilgan")

    def __str__(self):
        return self.question_text if self.question_text else f"Rasmga asoslangan savol ({self.id})"

    class Meta:
        verbose_name = "Test Savoli"
        verbose_name_plural = "7. Test Savol-Javoblari"