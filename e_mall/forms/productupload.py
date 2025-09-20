from django import forms
from e_mall.models.products import Products 
from e_mall.models.location import * 
from django.core.exceptions import ValidationError

def validate_phone(value):
    if not value.isdigit():
        raise ValidationError('Phone must have digits in format 777777777')
    if len(value)>=10:
        raise ValidationError("write number in format 777777777")
def validate_money(values):
    try:
        float(values)
        if len(str(values))>12:
            raise ValidationError("value must not be more than 10 digits")
    except ValueError:
        raise ValidationError('nyora mushe')
    
def file_size_validator(value):
    if value.size > 1024 * 1024 * 20:  # 20MB limit
        raise ValidationError('Image size is too large')
COUNTRY_PHONE_CODES = [
    ('+263', 'Zim (+263)'),
    ('+27', 'RSA (+27)'),
    ('+1', 'USA (+1)'),
    ('+44', 'UK (+44)'),
    ('+91', 'Ind (+91)'),
]

class ProductsForm(forms.ModelForm):
    phone_no=forms.CharField(validators=[validate_phone])
    price=forms.FloatField(validators=[validate_money],required=False)
    image1=forms.ImageField(required=False, validators=[file_size_validator])
    image2=forms.ImageField(required=False, validators=[file_size_validator])
    image3=forms.ImageField(required=False, validators=[file_size_validator])
    image4=forms.ImageField(required=False, validators=[file_size_validator])
    image5=forms.ImageField(required=False, validators=[file_size_validator])
    image6=forms.ImageField(required=False, validators=[file_size_validator])
    image7=forms.ImageField(required=False, validators=[file_size_validator])
    image8=forms.ImageField(required=False, validators=[file_size_validator])
    image9=forms.ImageField(required=False, validators=[file_size_validator])
    image10=forms.ImageField(required=False, validators=[file_size_validator])
    country = forms.ModelChoiceField(queryset=Country.objects.all(), required=False)
    location = forms.ModelChoiceField(queryset=Location.objects.none(), required=False)
    country_code = forms.ChoiceField(choices=COUNTRY_PHONE_CODES, required=False)
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['phone_no'].widget.attrs.update({'placeholder':'777777777'})
        self.fields['price'].widget.attrs.update({'placeholder':'US$, (optional)'})
        self.fields['description'].widget.attrs.update({'placeholder':'optional but recommended'})
        if 'country' in self.data:
            try:
                country_id = int(self.data.get('country'))
                self.fields['location'].queryset = Location.objects.filter(country_id=country_id).order_by('name')
            except (ValueError, TypeError):
                pass  # Invalid input; fallback to empty Location queryset
        elif self.instance.pk and self.instance.country:
            self.fields['location'].queryset = self.instance.country.locations.order_by('name')
    class Meta:
        model = Products
        fields = ['name','price','category','description', 'location','phone_no','image1','image2','image3',
                  'image4','image5','image6','image7','image8','image9','image10','country_code', 'international']
        widgets={'description':forms.Textarea(attrs={'required':False,'rows':5,'cols':20, 'style':'resize:none;'}),}

    def save(self, commit=True):
        instance = super().save(commit=False)
        # Combine country code and phone number before saving
        country_code = self.cleaned_data.get('country_code')
        phone_no = self.cleaned_data.get('phone_no')
        if country_code and phone_no:
            instance.phone_no = f"{country_code} {phone_no}"
        if commit:
            instance.save()
        return instance
    