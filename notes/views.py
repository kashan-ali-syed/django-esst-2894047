from django.shortcuts import render, get_object_or_404
from django.http import Http404, HttpResponseRedirect
from django.urls import reverse
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from .models import Notes
from .form import NotesForm

def add_like_view(request, pk):
    if request.method == 'POST':
        note = get_object_or_404(Notes, id=pk)
        note.likes += 1
        note.save()
        return HttpResponseRedirect(reverse('notes.detail', args=[pk]))
    raise Http404("Invalid request method")

class NotesCreateView(CreateView):
    model = Notes
    success_url = '/smart/notes/'
    form_class = NotesForm

class NotesListView(ListView):
    model = Notes
    context_object_name = 'notes'
    template_name = 'notes/notes_list.html'

## list only view that have more than one likes
class PopularNotesListView(ListView):
    model = Notes
    context_object_name = 'notes'
    template_name = 'notes/popular_notes_list.html'
    queryset = Notes.objects.filter(likes__gte=1)

class NotesDetailView(DetailView):
    model = Notes
    context_object_name = 'note'
    template_name = 'notes/notes_details.html'

class NotesUpdateView(UpdateView):
    model = Notes
    success_url = '/smart/notes/'
    form_class = NotesForm

class NotesDeleteView(DeleteView):
    model = Notes
    success_url = '/smart/notes/'
    template_name = 'notes/notes_delete.html'

def details(request, pk):
    try:
        note = Notes.objects.get(id=pk)
    except Notes.DoesNotExist:
        raise Http404("Note does not exist")
    return render(request, 'notes/notes_details.html', {'note': note})