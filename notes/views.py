from django.shortcuts import render, get_object_or_404
from django.http import Http404, HttpResponseRedirect
from django.urls import reverse
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin

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

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())

class NotesListView(LoginRequiredMixin, ListView):
    model = Notes
    context_object_name = 'notes'
    template_name = 'notes/notes_list.html'
    login_url = '/admin'

## list only view that have more than one likes
class PopularNotesListView(LoginRequiredMixin, ListView):
    model = Notes
    context_object_name = 'notes'
    template_name = 'notes/popular_notes_list.html'
    queryset = Notes.objects.filter(likes__gte=1)
    login_url = '/admin'

    def get_queryset(self):
        return self.request.user.notes_set.all().order_by('-likes')

class NotesPublicDetailView(DetailView):
    model = Notes
    context_object_name = 'note'
    queryset = Notes.objects.filter(is_public=True)
    template_name = 'notes/notes_public_details.html'

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

## Add new class to mark notes as public or private
class NotesPrivacyUpdateView(UpdateView):
    model = Notes
    success_url = '/smart/notes/'
    fields = ['is_public']
    template_name = 'notes/notes_privacy_update.html'

def details(request, pk):
    try:
        note = Notes.objects.get(id=pk)
    except Notes.DoesNotExist:
        raise Http404("Note does not exist")
    return render(request, 'notes/notes_details.html', {'note': note})

