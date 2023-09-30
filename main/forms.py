from django import forms


class SignUpForm(forms.Form):
    attrs = {
        'class': 'w-full bg-gray-800 bg-opacity-40 rounded border border-gray-700 focus:border-green-500 focus:bg-gray-900 focus:ring-2 focus:ring-green-900 text-base outline-none text-gray-100 py-1 px-3 leading-8 transition-colors duration-200 ease-in-out',
    }
    first_name = forms.CharField(
        label='First Name', max_length=255, widget=forms.TextInput(attrs=attrs))
    last_name = forms.CharField(
        label='Last Name', max_length=255, widget=forms.TextInput(attrs=attrs))
    profile_picture = forms.ImageField(label='Upload Profile Picture')
    username = forms.CharField(
        label='Username', max_length=255, widget=forms.TextInput(attrs=attrs))
    email = forms.EmailField(
        label='Email', max_length=255, widget=forms.TextInput(attrs=attrs))
    password = forms.CharField(
        label='Password', max_length=255, widget=forms.PasswordInput(attrs=attrs))
    confirm_password = forms.CharField(
        label='Confirm Password', max_length=255, widget=forms.PasswordInput(attrs=attrs))
    address_line_1 = forms.CharField(
        label='Address Line 1', max_length=255, widget=forms.TextInput(attrs=attrs))
    city = forms.CharField(label='City', max_length=255,
                           widget=forms.TextInput(attrs=attrs))
    state = forms.CharField(label='State', max_length=255,
                            widget=forms.TextInput(attrs=attrs))
    pin_code = forms.CharField(
        label='Pin Code', max_length=255, widget=forms.TextInput(attrs=attrs))


class PostForm(forms.Form):
    attrs = {
        'class': 'w-full bg-gray-800 bg-opacity-40 rounded border border-gray-700 focus:border-green-500 focus:bg-gray-900 focus:ring-2 focus:ring-green-900 text-base outline-none text-gray-100 py-1 px-3 leading-8 transition-colors duration-200 ease-in-out',
    }
    title = forms.CharField(
        label='Title', max_length=255, widget=forms.TextInput(attrs=attrs))
    category = forms.CharField(
        label='Category', max_length=255, widget=forms.TextInput(attrs=attrs))
    image = forms.ImageField(label='Upload Image')
    summary = forms.CharField(
        label='Summary', widget=forms.Textarea(attrs=attrs))
    content = forms.CharField(
        label='Content', widget=forms.Textarea(attrs=attrs))
    draft = forms.BooleanField(label='Draft', required=False)


class EditPostForm(forms.Form):
    attrs = {
        'class': 'w-full bg-gray-800 bg-opacity-40 rounded border border-gray-700 focus:border-green-500 focus:bg-gray-900 focus:ring-2 focus:ring-green-900 text-base outline-none text-gray-100 py-1 px-3 leading-8 transition-colors duration-200 ease-in-out',
    }
    title = forms.CharField(
        label='Title', max_length=255, widget=forms.TextInput(attrs=attrs))
    category = forms.CharField(
        label='Category', max_length=255, widget=forms.TextInput(attrs=attrs))
    image = forms.ImageField(label='Upload Image', required=False)
    summary = forms.CharField(
        label='Summary', widget=forms.Textarea(attrs=attrs))
    content = forms.CharField(
        label='Content', widget=forms.Textarea(attrs=attrs))
    draft = forms.BooleanField(label='Draft', required=False)


class AppointmentForm(forms.Form):
    attrs = {
        'class': 'w-full bg-gray-800 bg-opacity-40 rounded border border-gray-700 focus:border-green-500 focus:bg-gray-900 focus:ring-2 focus:ring-green-900 text-base outline-none text-gray-100 leading-8 transition-colors duration-200 ease-in-out px-3 py-1',
    }
    required_speciality = forms.ChoiceField(
        choices=([('Default', '--- Select Speciality ---'),
                  ('Urology', 'Urology'),
                  ('Oncology', 'Oncology'),
                  ('Radiology', 'Radiology'),
                  ('Neurology', 'Neurology'),
                  ('Psychiatry', 'Psychiatry'),
                  ('Geriatrics', 'Geriatrics'),
                  ('Cardiology', 'Cardiology'),
                  ('Pediatrics', 'Pediatrics'),
                  ('Dermatology', 'Dermatology'),
                  ('Orthopedics', 'Orthopedics')
                  ]),
        required=True, label='Required Speciality', widget=forms.Select(attrs={'class': f"{attrs['class']}py-2".replace('py-1', '')}))
    date = forms.DateField(
        label='Appointment Date', widget=forms.DateInput(attrs={'class': attrs['class'], 'type': 'date'}))
    start_time = forms.TimeField(
        label='Start Time', widget=forms.TimeInput(attrs={'class': attrs['class'], 'type': 'time'}))
