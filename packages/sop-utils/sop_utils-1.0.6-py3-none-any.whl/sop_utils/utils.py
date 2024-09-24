from django.contrib.auth.mixins import AccessMixin
from django.contrib import messages
from django.shortcuts import redirect, render, get_object_or_404
from django.utils.translation import gettext_lazy as _
from django.db import transaction
from django.views import View

from utilities.querydict import normalize_querydict
from utilities.forms import restrict_form_fields
from utilities.exceptions import PermissionsViolation
from utilities.permissions import get_permission_for_model

from extras.models import CustomFieldChoiceSet
from netbox.views.generic.utils import get_prerequisite_model
from netbox.views import generic
from dcim.models import Site

from extras.models import CustomFieldChoiceSet


__all__ = (
    'CustomAddView',
    'CustomEditView',
    'CheckJSONMaintainerImport',
    'CheckJSONImportFormat',
    'count_all_sda_list',
    'get_object_or_create',
    'get_choices',
)


'''
scripts
'''


class CustomViewMixin:
    '''
    Mixin metaclass for every CustomView class
    '''

    def get_choices(self, value: str) -> list[list[str]] | None:
        '''
        value is the name of the CustomFieldChoiceSet

        return the right choice set
        '''
        try:
            choices = CustomFieldChoiceSet.objects.filter(name=f'{value}')
            return choices.first().extra_choices
        except:
            return None

    def get_form_context(self, form, pk=None):
        '''
        customizes a form field queryset
        edit this function when you call the CustomEditView class
          - example:

            form.fields['name'].choices = get_choices('str')
            # where str is the targeted CustomFieldChoiceSet.name
        '''
        return form

    def get_extra_context(self, request, pk=None) -> dict:
        '''
        returns extra context for the form
        '''
        form = self.form(request.GET)
        form = self.get_form_context(form, pk)
        return_url = self.get_return_url(request, pk)
        return {
            'object': self.model, 'form': form, 'model': self.model._meta.verbose_name.title(),
            'return_url': return_url
        }

    def get_return_url(self, request, pk=None) -> str:
        '''
        the default return url
        '''
        if pk is not None:
            return f'/dcim/sites/{pk}/voice/'
        return '/dcim/sites/'

    def get_error_url(self, request, pk=None) -> str:
        '''
        the return url of any error
        '''
        return self.get_return_url(request, pk)

    def check_errors(self, request, pk=None) -> bool:
        '''
        check validators before returning the view
        '''
        return False

    
class CustomEditView(View, CustomViewMixin, AccessMixin):
    '''
    edits an existing model instance with extra custom params
    '''
    template_name: str = 'sop_utils/tools/form.html'
    model = None
    form = None

    def get_extra_context(self, request, pk=None) -> dict:
        '''
        returns extra context for the form
        '''
        instance = self.model.objects.filter(pk=pk).first()
        form = self.form(instance=instance)
        form = self.get_form_context(form, pk)
        return_url = self.get_return_url(request, pk)
        return {
            'object': instance, 'form': form, 'model': self.model._meta.verbose_name.title(),
            'return_url': return_url, 'title': f'Edit {instance.__str__()}'
        }

    def get(self, request, pk):
        if not request.user.has_perm(get_permission_for_model(self.model, 'change')):
            return self.handle_no_permission()
        if self.check_errors(request, pk):
            return redirect(self.get_error_url(request, pk))
        return render(request, self.template_name, self.get_extra_context(request, pk))

    def save_form(self, request, form, pk):
        '''
        saves the form data to the targeted model instance
        '''
        instance = self.model.objects.filter(pk=pk)
        instance = form.save()
        instance.save()
        messages.success(request, _(f'Successfully edited {self.model._meta.verbose_name}.'))

    def post(self, request, pk):
        if not request.user.has_perm(get_permission_for_model(self.model, 'change')):
            return self.handle_no_permission()
        instance = self.model.objects.filter(pk=pk).first()
        form = self.form(request.POST, instance=instance)
        form = self.get_form_context(form, pk)
        if form.is_valid():
            self.save_form(request, form, pk)
            return redirect(self.get_return_url(request, pk))
        return redirect(self.get_return_url(request, pk))


class CustomAddView(View, CustomViewMixin, AccessMixin):
    '''
    create a new model instance with extra custom params
    '''

    template_name: str = 'sop_utils/tools/form.html'
    model = None
    form = None

    def get(self, request, pk=None):
        if not request.user.has_perm(get_permission_for_model(self.model, 'add')):
            return self.handle_no_permission()
        if self.check_errors(request, pk):
            return redirect(self.get_error_url(request, pk))
        return render(request, self.template_name, self.get_extra_context(request, pk))

    def save_form(self, request, form, site=None) -> None:
        '''
        saves the form data to a new model instance
        '''
        if site is None:
            try:
                instance = self.model(**form.cleaned_data)
                instance.save()
                messages.success(request, _(f'Successfully added a {self.model._meta.verbose_name}.'))
            except:
                messages.error(request, _(f'Error adding a {self.model._meta.verbose_name}.'))
            return
        try:
            instance = self.model(
                site=site,
                **form.cleaned_data
            )
            instance.save()
            messages.success(request, _(f'Successfully added a {self.model._meta.verbose_name}.'))
        except:
            messages.error(request, _(f'Error adding a {self.model._meta.verbose_name}.'))

    def post(self, request, pk=None):
        if not request.user.has_perm(get_permission_for_model(self.model, 'add')):
            return self.handle_no_permission()
        form = self.form(request.POST)
        form = self.get_form_context(form)
        site = None
        if form.is_valid():
            if pk is not None:
                site = get_object_or_404(Site, pk=pk)
            self.save_form(request, form, site)
            return redirect(self.get_return_url(request, pk))
        return redirect(self.get_return_url(request, pk))


def get_object_or_create(model, site: Site) -> object | None:
    '''
    get the model object or create it
    (for dcim/site extra models)
    '''
    if model is None:
        return None
    target = model.objects.filter(site=site)
    if target.exists():
        return target.first()
    target = model(site=site)
    target.save()
    return target


def get_choices(value: str, current: str) -> str | None:
    '''
    returns the label name of the customfield choice
    example:
      - model.object = get_choices('str', model.object)
    '''
    try:
        choices = CustomFieldChoiceSet.objects.filter(name=f'{value}')
        choices = choices.first().extra_choices
        if choices is None:
            raise Exception
        for choice in choices:
            if choice[0] == current:
                return choice[1]
    except:
        return current


class count_all_sda_list:
    """counts all SDA numbers in a SDA_List instance
    
    Args:
        sda_list (instance)
    Returns:
```python
    __int__():
        return (self.phone_count, self.range_count)
```
    """
    def __init__(self, sda_list) -> None:
        self.sda_list = sda_list
        self.phone_count, self.range_count = self.count()

    def format(self, phone: str) -> int:
        '''
        converts phone string to an int
        '''
        try:
            return int(''.join(n for n in phone if n.isdigit()))
        except:
            return 0

    def count_range(self, start: str, end: str) -> int:
        '''
        simply counts the number of phone numbers in a range
        '''
        x: int = self.format(start)
        y: int = self.format(end)

        if x > y:
            return 0
        if x == y:
            return 1
        if x < y:
            return (y - x) + 1
        return 0

    def count(self) -> tuple[int, int]:
        range_count: int = 0
        phone_count: int = 0

        try:
            for sda in self.sda_list:
                range_count += 1
                phone_count += self.count_range(sda.start, sda.end)
        except:
            try:
                phone_count += self.count_range(self.sda_list.start, self.sda_list.end)
                range_count += 1
            except:pass
        return phone_count, range_count

    def __int__(self) -> tuple[int, int]:
        '''
        ```python
        return (self.phone_count, self.range_count)
        ```
        '''
        return (self.phone_count, self.range_count)


class CheckJSONImportFormat:
    """Check the JSON format of the SDA List import

    Args:
        data (list): the JSON data

    Returns:
        checked_data (list) if valid
        else None (None)
    """
    def __init__(self, data):
        self.data = data

    def format(self, value: str) -> str:
        invalid:list = ['\t', ' ', '\n', ' ', '\"', '[', ']', '\'', '>']

        try:return ''.join(n for n in value if n not in invalid)
        except:return value

    def check_format(self) -> list[dict[str, str]]|None:
        '''
        tries to create a list of dicts from the JSON data
        returns None if invalid
        '''
        checked: list[dict[str, str]] = []

        for data in self.data:
            if len(data) <= 1:
                return None
            try:
                data.split('\n')
                try:start, end = data.split('>>')
                except:start = data; end = start
                checked.append({"start":self.format(start), "end":self.format(end)})
            except:return None

        return checked


class CheckJSONMaintainerImport:
    def __init__(self, data):
        self.data = data

    def format(self, value: str) -> str:
        invalid:list = ['\t', '\n', '\"', '[', ']', '\'', '>', '<']

        try:return ''.join(n for n in value if n not in invalid)
        except:return value

    def check_format(self) -> list[str]|None:
        checked = []

        try:
            for data in self.data:
                checked.append(data)
            return checked
        except:return None
