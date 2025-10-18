from django import forms
from .models import Community, CommunitySubmission, Category


# -------------------------
# Community Submission Form (public users)
# -------------------------
class CommunitySubmissionForm(forms.ModelForm):
    class Meta:
        model = CommunitySubmission
        fields = [
            "name",
            "description",
            "category",
            "location",
            "founded_date",
            "website",
            "facebook_page",
        ]
        widgets = {
            "description": forms.Textarea(attrs={"rows": 4, "placeholder": "Describe the community"}),
            "founded_date": forms.DateInput(attrs={"type": "date"}),
            "website": forms.URLInput(attrs={"placeholder": "https://example.com"}),
            "facebook_page": forms.URLInput(attrs={"placeholder": "https://facebook.com/page"}),
        }
        labels = {
            "name": "Community Name",
            "description": "Description",
            "category": "Category",
            "location": "Location",
            "founded_date": "Founded Date",
            "website": "Website URL",
            "facebook_page": "Facebook Page URL",
        }


# -------------------------
# Community Form (for Admin editing)
# -------------------------
class CommunityForm(forms.ModelForm):
    class Meta:
        model = Community
        fields = [
            "name",
            "description",
            "category",
            "location",
            "founded_date",
            "website",
            "facebook_page",
            "approved",
            "status",
        ]
        widgets = {
            "description": forms.Textarea(attrs={"rows": 4}),
            "founded_date": forms.DateInput(attrs={"type": "date"}),
        }


# -------------------------
# Category Form (for Admin editing/creating)
# -------------------------
class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ["name", "is_approved"]
