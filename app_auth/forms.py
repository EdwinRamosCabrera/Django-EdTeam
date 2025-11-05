from django import forms

class ClientForm(forms.Form):
    dni = forms.CharField(max_length=8, label='DNI')
    first_name = forms.CharField(max_length=200, label='Nombre')
    last_name = forms.CharField(max_length=200, label='Apellidos')
    email = forms.EmailField(label='Correo Electrónico', required=True)
    address = forms.CharField(widget=forms.Textarea, label='Dirección')
    phone = forms.CharField(max_length=15, label='Teléfono')
    gender = forms.ChoiceField(choices=[('M', 'Masculino'), ('F', 'Femenino')], label='Género')
    birth_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), input_formats=['%Y-%m-%d'], label='Fecha de Nacimiento')
