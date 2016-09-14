from django.contrib.postgres.forms.array import SimpleArrayField
from django.forms import SelectMultiple, CheckboxSelectMultiple


class ArraySelect(SimpleArrayField):
    """
    This class fixes an issue when converting back to python
    but the data is already a list
    """
    def to_python(self, value):
        if value:
            if not isinstance(value, list):
                items = value.split(self.delimiter)
            else:
                items = value
        else:
            items = []
        errors = []
        values = []
        for index, item in enumerate(items):
            try:
                values.append(self.base_field.to_python(item))
            except ValidationError as error:
                errors.append(prefix_validation_error(
                    error,
                    prefix=self.error_messages['item_invalid'],
                    code='item_invalid',
                    params={'nth': index},
                ))
        if errors:
            raise ValidationError(errors)
        return values


class ArrayWidget(CheckboxSelectMultiple):

    def render(self, name, value, attrs=None):
        value = value.split(',')
        print value
        return super(ArrayWidget, self).render(name, value, attrs)
