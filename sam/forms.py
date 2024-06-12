from django.forms import ModelForm
from django import forms
from .models import Software,  Staff, Contract, UserAllocation
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

class SoftwareForm(ModelForm):

        def __init__(self, *args, **kwargs):
            super(SoftwareForm, self).__init__(*args, **kwargs)
            self.helper = FormHelper()
            self.helper.form_method = 'post'
            self.helper.add_input(Submit('submit', 'Save Software'))
            self.fields['created_date'].widget.attrs['readonly'] = True
            self.fields['last_updated'].widget.attrs['readonly'] = True
            self.fields['software_id'].widget.attrs['readonly'] = True



        class Meta:
            model = Software

            fields = '__all__'
            widgets = {'software_id': forms.HiddenInput(),
                       'created_date': forms.HiddenInput(),
                       'last_updated': forms.HiddenInput(),
                       'number_of_users':forms.HiddenInput(),
                       'contract_value': forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Please fill this in'}),
                       'number_of_licenses': forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Please fill this in'}),
                       'software_name': forms.TextInput(attrs={'class':'form-control','placeholder':'Please fill this in'}),
                       'managed_by': forms.TextInput(attrs={'class': 'form-control'}),
                       'vendor': forms.TextInput(attrs={'class': 'form-control'}),
                       'approval_status': forms.TextInput(attrs={'class': 'form-control'}),
                       'status': forms.Select(attrs={'class': 'form-control'}),
                       'category': forms.Select(attrs={'class': 'form-control',}),
                       'software_type': forms.Select(attrs={'class': 'form-control'}),
                       'contract_type': forms.Select(attrs={'class': 'form-control'})

                       }




class UserForm(ModelForm):

    # def __init__(self, *args, **kwargs):
    #     super(UserForm, self).__init__(*args, **kwargs)
    #     self.fields['software'].widget.attrs['readonly'] = True
    #     self.fields['last_updated'].widget.attrs['readonly'] = True

    class Meta:
        model = Staff

        fields = '__all__'
        # widgets = {'created_date': forms.HiddenInput(),'last_updated': forms.HiddenInput()  }

class UserAllocationForm(forms.ModelForm):
    users = forms.ModelMultipleChoiceField(
        queryset=Staff.objects.all(),
        widget=forms.SelectMultiple(attrs={'class': 'select2'})
    )

    class Meta:
        model = UserAllocation
        fields = ['software', 'users']
        widgets = {'software': forms.HiddenInput()}

    def __init__(self, *args, **kwargs):
        self.software_instance = kwargs.pop('software_instance', None)
        super().__init__(*args, **kwargs)
        self.fields['users'].queryset = Staff.objects.all()
        if self.software_instance:
            self.fields['software'].initial = self.software_instance



class StaffForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super(StaffForm, self).__init__(*args, **kwargs)
        self.fields['created_date'].widget.attrs['readonly'] = True
        self.fields['last_updated'].widget.attrs['readonly'] = True

    class Meta:
        model = Staff

        fields = '__all__'
        widgets = {'created_date': forms.HiddenInput(),
                   'last_updated': forms.HiddenInput(),
                   'employee_id': forms.TextInput(attrs={'class': 'form-control'}),
                   'first_name': forms.TextInput(attrs={'class': 'form-control'}),
                   'last_name': forms.TextInput(attrs={'class': 'form-control'}),
                   'department': forms.Select(attrs={'class': 'form-control'}),
                   'position': forms.TextInput(attrs={'class': 'form-control'}),
                   'email': forms.EmailInput(attrs={'class': 'form-control'}),}



#
class ContractForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super(ContractForm, self).__init__(*args, **kwargs)
        self.fields['software_id'].widget.attrs['readonly'] = True
        self.fields['contract_id'].widget.attrs['readonly'] = True
        self.fields['added'].widget.attrs['readonly'] = True
        self.fields['last_updated'].widget.attrs['readonly'] = True

    class Meta:
        model = Contract
        fields = '__all__'
        widgets = {'software_id': forms.HiddenInput(),
                   'added': forms.HiddenInput(),
                   'last_updated': forms.HiddenInput(),
                   'contract_id': forms.HiddenInput(),
                   'license_type': forms.Select(attrs={'class': 'form-control'}),
                   'numer_of_licenses': forms.TextInput(attrs={'class': 'form-control'}),
                   'contact_status': forms.Select(attrs={'class': 'form-control'}),
                   'renewal_status': forms.Select(attrs={'class': 'form-control'}),
                   'start_date': forms.DateInput(attrs={'class': 'form-control'}),
                   'end_date': forms.DateInput(attrs={'class': 'form-control'}),
                  }