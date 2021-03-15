from django.contrib import messages


class ErrorMessageMixin:
    """
    Add a success message on successful form submission.
    """
    error_message = ''

    def form_invalid(self, form):
        response = super().form_invalid(form)
        error_message = self.get_error_message(form.cleaned_data)
        if error_message:
            messages.error(self.request, error_message)
        return response

    def get_error_message(self, cleaned_data):
        return self.error_message % cleaned_data
