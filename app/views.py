
from .models import CommunitySubmission, Category, Location
from .forms import CommunitySubmissionForm
#----
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Q
from django.core.paginator import Paginator

from .models import Community, CommunitySubmission
from .forms import CommunitySubmissionForm


from django.contrib.auth.decorators import login_required, user_passes_test

from .models import Community, CommunitySubmission, Category
from .forms import CommunitySubmissionForm, CommunityForm, CategoryForm

from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# Login View
def login_user(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "Login successful!")
            return redirect("home")
        else:
            messages.error(request, "Invalid username or password.")
    return render(request, "app/login.html")

# Logout View
@login_required
def logout_user(request):
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect('home')





# ----------------------
# Home page
# ----------------------
def home(request):
    """Show recent approved communities."""
    communities = Community.objects.filter(approved=True).order_by('-added_at')[:6]
    categories = Category.objects.all().order_by('name')

    return render(request, 'app/home.html', {'communities': communities, 'categories': categories,})








# ----------------------
# Communities list with search + pagination
# ----------------------
def communities_list(request):
    """List approved communities with optional search."""
    query = request.GET.get('q', '')
    communities = Community.objects.filter(approved=True)
    categories = Category.objects.all().order_by('name')

    if query:
        communities = communities.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query) |
            Q(category__name__icontains=query) |
            Q(location__name__icontains=query)
        )

    communities = communities.order_by('-added_at')

    # Pagination: 9 per page
    paginator = Paginator(communities, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(
        request,
        'app/communities_list.html',
        {'communities': page_obj, 'query': query, 'categories': categories, }
    )


# ----------------------
# Community detail page
# ----------------------
def community_detail(request, slug):
    categories = Category.objects.all().order_by('name')

    """Show details of a single approved community."""
    community = get_object_or_404(Community, slug=slug, approved=True)
    
    return render(request, 'app/community_detail.html', {'community': community, 'categories': categories,})




# ----------------------
# Public submission (unlogged users)
# ----------------------
def submit_community(request):
    """Allow unlogged users to submit a community for review with option to add category/location."""
    categories = Category.objects.filter(is_approved=True).order_by('name')
    locations = Location.objects.all().order_by('name')  # approved check optional

    if request.method == "POST":
        form = CommunitySubmissionForm(request.POST)
        new_category_name = request.POST.get("new_category", "").strip()
        new_location_name = request.POST.get("new_location", "").strip()

        # Create new category if provided
        if new_category_name:
            category, created = Category.objects.get_or_create(name=new_category_name)
            if created:
                category.is_approved = False  # new category pending approval
                category.save()
            form.instance.category = category

        # Create new location if provided
        if new_location_name:
            location, created = Location.objects.get_or_create(name=new_location_name)
            form.instance.location = location

        if form.is_valid():
            submission = form.save(commit=False)
            submission.approved = False  # default to pending
            submission.save()
            messages.success(request, "Your community submission was sent for review!")
            return redirect("home")
    else:
        form = CommunitySubmissionForm()

    context = {
        "form": form,
        "categories": categories,
        "locations": locations,
    }
    return render(request, "app/submit_community.html", context)






# -------------------------
# Check if user is admin
# -------------------------
def is_admin(user):
    return user.is_staff or user.is_superuser

@login_required
@user_passes_test(is_admin)
def admin_dashboard(request):
    """Admin dashboard with communities, submissions, categories."""
    # Approved data
    approved_communities = Community.objects.filter(approved=True)
    approved_categories = Category.objects.filter(is_approved=True)

    # Pending submissions
    submissions = CommunitySubmission.objects.filter(approved=False)

    #submissions = CommunitySubmission.objects.filter(is_approved=False)
    pending_categories = Category.objects.filter(is_approved=False)

    if request.method == "POST":
        action = request.POST.get("action")
        target = request.POST.get("target")
        target_id = request.POST.get("id")

        # ----------------
        # Community Actions
        # ----------------
        if target == "community":
            community = get_object_or_404(Community, id=target_id)

            if action == "delete":
                community.delete()
                messages.error(request, f"Community '{community.name}' deleted.")
            elif action == "edit":
                form = CommunityForm(request.POST, instance=community)
                if form.is_valid():
                    form.save()
                    messages.success(request, f"Community '{community.name}' updated.")
            return redirect("admin_dashboard")

        # ----------------
        # Community Submission Actions
        # ----------------
        elif target == "submission":
            submission = get_object_or_404(CommunitySubmission, id=target_id)

            if action == "approve":
                submission.approve_submission()
                messages.success(request, f"Submission '{submission.name}' approved.")
            elif action == "decline":
                submission.is_approved = False
                submission.save()
                messages.warning(request, f"Submission '{submission.name}' declined.")
            elif action == "delete":
                submission.delete()
                messages.error(request, f"Submission '{submission.name}' deleted.")
            return redirect("admin_dashboard")

        # ----------------
        # Category Actions
        # ----------------
        elif target == "category":
            category = get_object_or_404(Category, id=target_id)

            if action == "delete":
                category.delete()
                messages.error(request, f"Category '{category.name}' deleted.")
            elif action == "edit":
                form = CategoryForm(request.POST, instance=category)
                if form.is_valid():
                    form.save()
                    messages.success(request, f"Category '{category.name}' updated.")
            return redirect("admin_dashboard")

        # ----------------
        # Category Submission Actions
        # ----------------
        elif target == "category_submission":
            category = get_object_or_404(Category, id=target_id)

            if action == "approve":
                category.is_approved = True
                category.save()
                messages.success(request, f"Category '{category.name}' approved.")
            elif action == "reject":
                category.is_approved = False
                category.save()
                messages.warning(request, f"Category '{category.name}' rejected.")
            return redirect("admin_dashboard")

    context = {
        "approved_communities": approved_communities,
        "submissions": submissions,
        "approved_categories": approved_categories,
        "pending_categories": pending_categories,
    }
    return render(request, "app/dashboard.html", context)
