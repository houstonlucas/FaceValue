from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User, Group
from django.core.exceptions import PermissionDenied
from django.views.generic import ListView
from django.contrib.auth.decorators import login_required, user_passes_test


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'accounts/signup.html', {'form': form})


class UserListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = User
    template_name = 'accounts/user_list.html'
    context_object_name = 'users'

    def test_func(self):
        user = self.request.user
        return user.is_superuser or user.groups.filter(name__in=['Admin', 'SuperAdmin']).exists()

    def handle_no_permission(self):
        raise PermissionDenied

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        users = context['users']
        for u in users:
            if u.is_superuser or u.groups.filter(name='SuperAdmin').exists():
                u.highest_role = 'SuperAdmin'
            elif u.groups.filter(name='Admin').exists():
                u.highest_role = 'Admin'
            elif u.groups.filter(name='User').exists():
                u.highest_role = 'User'
            else:
                u.highest_role = 'None'
        context['is_superadmin'] = (
            self.request.user.is_superuser or
            self.request.user.groups.filter(name='SuperAdmin').exists()
        )
        return context


# SuperAdmin-only operations
@login_required
@user_passes_test(lambda u: u.groups.filter(name='SuperAdmin').exists())
def promote_to_admin(request, pk):
    target = get_object_or_404(User, pk=pk)
    admin_group = Group.objects.get(name='Admin')
    target.groups.add(admin_group)
    return redirect('user_list')


@login_required
@user_passes_test(lambda u: u.groups.filter(name='SuperAdmin').exists())
def demote_from_admin(request, pk):
    target = get_object_or_404(User, pk=pk)
    admin_group = Group.objects.get(name='Admin')
    target.groups.remove(admin_group)
    return redirect('user_list')


@login_required
@user_passes_test(lambda u: u.groups.filter(name='SuperAdmin').exists())
def delete_user(request, pk):
    target = get_object_or_404(User, pk=pk)
    if target != request.user:
        target.delete()
    return redirect('user_list')


def logout_view(request):
    """Log the user out via GET and redirect to home."""
    logout(request)
    return redirect('home')
