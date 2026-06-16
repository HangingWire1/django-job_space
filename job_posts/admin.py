from django.contrib import admin
from django import forms  # <--- Make sure this is here!
from job_posts.models import Category, JobPost
from authentication.models import Location, State, Township

# Register your models here.
admin.site.register(Category)

class JobPostAdminForm(forms.ModelForm):
    # Manually add the fields you want the Admin to type in
    state = forms.ModelChoiceField(queryset=State.objects.all())
    township = forms.ModelChoiceField(queryset=Township.objects.all())
    detail_address = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = JobPost
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Check if this form is editing an existing JobPost (has an instance and a location)
        if self.instance and self.instance.pk and self.instance.location:
            self.fields['state'].initial = self.instance.location.state
            self.fields['township'].initial = self.instance.location.township
            self.fields['detail_address'].initial = self.instance.location.detail_address

@admin.register(JobPost)
class JobPostAdmin(admin.ModelAdmin):
    form = JobPostAdminForm

    exclude = ('location', 'slug',)

    def save_model(self, request, obj, form, change):
        # 1. Create/Update the Location first
        loc, created = Location.objects.get_or_create(
            state=form.cleaned_data['state'],
            township=form.cleaned_data['township'],
            detail_address=form.cleaned_data['detail_address']
        )
        # 2. Link it to the Job
        obj.location = loc
        super().save_model(request, obj, form, change)
