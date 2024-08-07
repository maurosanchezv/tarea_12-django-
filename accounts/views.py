from django.urls import reverse_lazy, reverse
from django.contrib.auth import login, authenticate, logout
from django.shortcuts import redirect
from .forms import (
    CustomUserCreationForm,
    UserUpdateForm,
)
from django.contrib.auth import get_user_model
from django.views.generic import (
    CreateView, DetailView, UpdateView, DeleteView,)    # cambiar
from django.contrib.auth.views import (
    PasswordChangeView, PasswordChangeDoneView)
from django.contrib.auth.mixins import UserPassesTestMixin    # Apéndice


User = get_user_model()


class OnlyYouMixin(UserPassesTestMixin):
    def test_func(self):
        user = self.request.user
        return user.pk == self.kwargs['pk'] or user.is_superuser


class UserCreateAndLoginView(CreateView):
    form_class = CustomUserCreationForm
    template_name = "signup.html"
    success_url = reverse_lazy('tasks:index')

    def form_valid(self, form):
        response = super().form_valid(form)
        email = form.cleaned_data.get("email")
        raw_pw = form.cleaned_data.get("password1")
        user = authenticate(email=email, password=raw_pw)
        login(self.request, user)
        return response


class UserDetail(DetailView):
    model = User
    template_name = 'user_detail.html'


class UserUpdate(UpdateView):
    model = User
    form_class = UserUpdateForm
    template_name = 'user_edit.html'

    def get_success_url(self):
        return reverse('user_detail', kwargs={'pk': self.kwargs['pk']})


class PasswordChange(PasswordChangeView):
    template_name = 'password_change.html'


class PasswordChangeDone(PasswordChangeDoneView):
    template_name = 'user_detail.html'


class UserDelete(DeleteView):
    model = User
    template_name = 'user_delete.html'
    success_url = reverse_lazy('login')
