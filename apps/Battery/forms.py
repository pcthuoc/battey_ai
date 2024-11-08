# apps/Battery/forms.py
from django import forms
from .models import Battery

class BatteryForm(forms.ModelForm):
    class Meta:
        model = Battery
        fields = ['name', 'nominal_capacity', 'voltage_min', 'voltage_max']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'bg-gray-50 border border-gray-300 text-gray-900 sm:text-sm rounded-lg focus:ring-primary-500 focus:border-primary-500 block w-full p-2.5',
                'placeholder': 'Tên Pin',
            }),
            'nominal_capacity': forms.NumberInput(attrs={
                'class': 'bg-gray-50 border border-gray-300 text-gray-900 sm:text-sm rounded-lg focus:ring-primary-500 focus:border-primary-500 block w-full p-2.5',
                'placeholder': 'Dung lương pin (mAh)',
            }),
            'voltage_min': forms.NumberInput(attrs={
                'class': 'bg-gray-50 border border-gray-300 text-gray-900 sm:text-sm rounded-lg focus:ring-primary-500 focus:border-primary-500 block w-full p-2.5',
                'placeholder': 'Điện áp thấp nhất (V)',
            }),
            'voltage_max': forms.NumberInput(attrs={
                'class': 'bg-gray-50 border border-gray-300 text-gray-900 sm:text-sm rounded-lg focus:ring-primary-500 focus:border-primary-500 block w-full p-2.5',
                'placeholder': 'Điện áp cao nhất (V)',
            }),
        }
