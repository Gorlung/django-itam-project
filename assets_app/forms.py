from django import forms
from assets_app.models import Asset,Employee,Location

class AssetForm(forms.ModelForm):

    class Meta():
        model = Asset
        fields = ('inventory_number', 'category', 'location', 'serial_number', 'vendor', 'state', 'aquisition_date', 'warranty_expiry_date', 'legal_entity', 'invoice_number', 'host_name', 'comments', 'model_name')
        widgets = {
            'inventory_number':forms.TextInput(attrs={'class':'textinputclass'}),
            'category':forms.Select(),
            'location':forms.Select(),
            'serial_number':forms.TextInput(attrs={'class':'textinputclass'}),
            'vendor':forms.Select(),
            'state':forms.Select(),
            'aquisition_date':forms.SelectDateWidget(),
            'warranty_expiry_date':forms.SelectDateWidget(),
            'legal_entity':forms.TextInput(attrs={'class':'textinputclass'}),
            'invoice_number':forms.TextInput(attrs={'class':'textinputclass'}),
            'host_name':forms.TextInput(attrs={'class':'textinputclass'}),
            'comments':forms.Textarea(attrs={'class':'editable medium-editor-textarea postcontent'}),
            }
    def __init__(self, *args, **kwargs):
        self.user_id = kwargs.pop('user_id')
        super(AssetForm, self).__init__(*args, **kwargs)
        self.fields['location'] = forms.ModelChoiceField(queryset=Location.objects.filter(id__in=Employee.objects.filter(user=self.user_id).values('permitted_locations')))