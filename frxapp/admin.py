from django.contrib import admin
from .models import Course, Lesson, Resource, FAQ, ContactMessage, CalculatorConfig, QuizQuestion


# Darsliklarni Kurs ichiga joylashtirish (Inline)
class LessonInline(admin.TabularInline):
    model = Lesson
    extra = 1

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('title',)
    inlines = [LessonInline] # Darslarni shu yerda qo'shamiz

@admin.register(Resource)
class ResourceAdmin(admin.ModelAdmin):
    list_display = ('title', 'type', 'file')
    list_filter = ('type',)

@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ('question', 'is_published')
    list_filter = ('is_published',)
    search_fields = ('question', 'answer')

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('subject', 'email', 'created_at', 'is_resolved')
    list_filter = ('is_resolved', 'created_at')
    readonly_fields = ('user', 'email', 'subject', 'message', 'created_at') # Ma'lumotlarni o'zgartirmaymiz
    actions = ['mark_resolved']

    def mark_resolved(self, request, queryset):
        queryset.update(is_resolved=True)
    mark_resolved.short_description = "Belgilangan xabarlarni Hal etilgan deb belgilash"

@admin.register(CalculatorConfig)
class CalculatorConfigAdmin(admin.ModelAdmin):
    list_display = ('name', 'max_risk_percent', 'min_trade_size')

# ... (Boshqa admin klasslar turaversin) ...

@admin.register(QuizQuestion)
class QuizQuestionAdmin(admin.ModelAdmin):
    list_display = ('id', 'question_text', 'num_options', 'correct_answer', 'is_published')
    list_filter = ('num_options', 'is_published')
    search_fields = ('question_text', 'option_a', 'option_b')
    # Rasmlarni ko'rish uchun maxsus maydon qo'shishimiz mumkin (ixtiyoriy)