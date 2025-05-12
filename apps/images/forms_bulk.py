from django import forms

class BulkDeleteImagesForm(forms.Form):
    image_ids = forms.MultipleChoiceField(choices=[], required=True)

    def __init__(self, *args, **kwargs):
        # Permitir aceitar qualquer lista de IDs recebida via POST
        super().__init__(*args, **kwargs)
        if 'data' in kwargs:
            ids = kwargs['data'].getlist('image_ids') if hasattr(kwargs['data'], 'getlist') else kwargs['data'].get('image_ids', [])
            self.fields['image_ids'].choices = [(i, i) for i in ids]
        else:
            self.fields['image_ids'].choices = []
