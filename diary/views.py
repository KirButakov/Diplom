from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from .models import DiaryEntry
from .forms import DiaryEntryForm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from django.contrib import messages

@login_required
def create_entry(request):
    if request.method == 'POST':
        form = DiaryEntryForm(request.POST, request.FILES)
        if form.is_valid():
            entry = form.save(commit=False)
            entry.user = request.user
            entry.save()
            return redirect('entry_detail', entry.id)
    else:
        form = DiaryEntryForm()
    return render(request, 'diary/create_entry.html', {'form': form})

@login_required
def edit_entry(request, entry_id):
    entry = get_object_or_404(DiaryEntry, id=entry_id, user=request.user)
    if request.method == 'POST':
        form = DiaryEntryForm(request.POST, request.FILES, instance=entry)
        if form.is_valid():
            form.save()
            return redirect('entry_detail', entry.id)
    else:
        form = DiaryEntryForm(instance=entry)
    return render(request, 'diary/edit_entry.html', {'form': form})

@login_required
def entry_detail(request, entry_id):
    entry = get_object_or_404(DiaryEntry, id=entry_id, user=request.user)
    return render(request, 'diary/entry_detail.html', {'entry': entry})

@login_required
def entry_list(request):
    entries = DiaryEntry.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'diary/entry_list.html', {'entries': entries})

@login_required
def search_entries(request):
    query = request.GET.get('q')
    tag = request.GET.get('tag')
    entries = DiaryEntry.objects.filter(user=request.user)

    if query:
        entries = entries.filter(
            Q(title__icontains=query) | Q(content__icontains=query)
        )
    if tag:
        entries = entries.filter(tags__name__in=[tag])

    entries = entries.order_by('-created_at')
    return render(request, 'diary/entry_list.html', {'entries': entries})

@login_required
def export_entry_pdf(request, entry_id):
    entry = get_object_or_404(DiaryEntry, id=entry_id, user=request.user)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{entry.title}.pdf"'

    # Регистрируем шрифт с полным путем (добавляем шрифт для кириллицы)
    pdfmetrics.registerFont(TTFont('DejaVuSans', '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'))
    pdfmetrics.registerFont(TTFont('DejaVuSansCyrillic', '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'))

    doc = SimpleDocTemplate(response, pagesize=letter)
    styles = getSampleStyleSheet()
    styles['BodyText'].fontName = 'DejaVuSansCyrillic'
    styles['Title'].fontName = 'DejaVuSansCyrillic'

    story = []

    # Заголовок
    story.append(Paragraph(entry.title, styles['Title']))
    story.append(Spacer(1, 12))

    # Текст
    story.append(Paragraph(entry.content, styles['BodyText']))
    story.append(Spacer(1, 12))

    # Изображение
    if entry.image:
        img = Image(entry.image.path, width=400, height=300)
        story.append(img)

    doc.build(story)
    return response

@login_required
def delete_entry(request, entry_id):
    entry = get_object_or_404(DiaryEntry, id=entry_id, user=request.user)
    entry.delete()
    messages.success(request, 'Запись успешно удалена.')
    return redirect('entry_list')

