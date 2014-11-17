## Mixins to inherit into Class based views
from django.shortcuts import redirect

class UserCheckMixin(object):
	# Base Mixin to create permission based checks
	user_check_failure_path = '/login/'  # can be path, url name or reverse_lazy

	def check_user(self, user):
		return True

	def user_check_failed(self, request, *args, **kwargs):
		return redirect(self.user_check_failure_path)

	def dispatch(self, request, *args, **kwargs):
		if not self.check_user(request.user):
			return self.user_check_failed(request, *args, **kwargs)
		return super(UserCheckMixin, self).dispatch(request, *args, **kwargs)



class LoginRequiredMixin(UserCheckMixin):
	# Class Based view mixin to replicate the 'login_required' decorator. Redirects on fail
	def check_user(self, user):
		return user.is_authenticated()

class PermissionRequiredMixin(UserCheckMixin):
	# Checks a given permission on the View as per the required_permission attribute. 
	# Similar to the 'permission_required' decorator
	required_permission = None

	def check_user(self, user):
		if user.is_authenticated() and self.required_permission:
			return self.request.user.has_perm(self.required_permission)
		return False


class UserGroupRequiredMixin(UserCheckMixin):
	# CBV Mixin requiring the current user to be in a givenpermission group.
	# Set required_group as the 'name' of the permission group
	required_group = None

	def check_user(self, user):
		if user.is_authenticated() and self.required_group:
			return self.required_group in user.groups.all().values_list('name', flat=True)
		return False
