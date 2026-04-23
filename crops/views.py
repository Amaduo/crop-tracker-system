from django.shortcuts import render, redirect, get_object_or_404
from .models import Field, FieldUpdate
from django import forms
from django.contrib.auth import login, authenticate, logout
from .forms import RegisterForm
from django.http import HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
User = get_user_model()


# ---------------- FORMS ----------------
class FieldForm(forms.ModelForm):
    class Meta:
        model = Field
        fields = '__all__'


class UpdateForm(forms.ModelForm):
    class Meta:
        model = FieldUpdate
        fields = ['stage', 'notes']


def admin_required(view_func):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.role == "admin":
            return view_func(request, *args, **kwargs)
        return HttpResponseForbidden("You are not allowed to access this page")
    return wrapper


# ---------------- DASHBOARD ----------------

def dashboard(request):

    fields = Field.objects.all()

    if hasattr(request.user, "role") and request.user.role == "agent":
        fields = Field.objects.filter(assigned_agent=request.user)

    total_fields = fields.count()
    active = fields.filter(current_stage__in=["Planted", "Growing"]).count()
    ready = fields.filter(current_stage="Ready").count()
    harvested = fields.filter(current_stage="Harvested").count()

    return render(request, "dashboard.html", {
        "fields": fields,
        "total_fields": total_fields,
        "active": active,
        "ready": ready,
        "harvested": harvested,
    })


# ---------------- FIELDS ----------------
def fields_view(request):
    fields = Field.objects.all()

    return render(request, 'fields.html', {
        'fields': fields
    })


def create_field(request):
    if request.method == "POST":

        agent_id = request.POST.get("assigned_agent")

        try:
            agent = User.objects.get(id=agent_id)
        except User.DoesNotExist:
            return render(request, "create_field.html", {
                "error": "Selected agent does not exist",
                "users": User.objects.filter(role="agent")
            })

        Field.objects.create(
            name=request.POST['name'],
            crop_type=request.POST['crop_type'],
            planting_date=request.POST['planting_date'],
            current_stage=request.POST['current_stage'],
            assigned_agent=agent
        )

        return redirect("fields")

    return render(request, "create_field.html", {
        "users": User.objects.filter(role="agent")
    })


def update_field(request, id):
    field = get_object_or_404(Field, id=id)

    if request.method == "POST":
        stage = request.POST.get("stage")
        notes = request.POST.get("notes")

        FieldUpdate.objects.create(
            field=field,
            agent=request.user,
            stage=stage,
            notes=notes
        )

        field.current_stage = stage
        field.save()

        return redirect('fields')

    return render(request, 'update.html', {'field': field})

# ---------------- UPDATES ----------------
def view_updates(request):
    updates = FieldUpdate.objects.all().order_by('-date')
    return render(request, 'updates.html', {'updates': updates})

def field_updates(request, id):
    field = get_object_or_404(Field, id=id)
    updates = FieldUpdate.objects.filter(field=field).order_by('-date')

    return render(request, 'updates_page.html', {
        'field': field,
        'updates': updates
    })

def updates_page(request):
    updates = FieldUpdate.objects.all().order_by('-date')

    return render(request, 'updates_page.html', {
        'updates': updates
    })

def agent_dashboard(request):

    
    fields = Field.objects.filter(assigned_agent=request.user.username)

   
    total_fields = fields.count()
    active = sum(1 for f in fields if f.status == "Active")
    at_risk = sum(1 for f in fields if f.status == "At Risk")
    completed = sum(1 for f in fields if f.status == "Completed")

    return render(request, 'agent_dashboard.html', {
        'fields': fields,
        'total_fields': total_fields,
        'active': active,
        'at_risk': at_risk,
        'completed': completed,
    })




def agent_base(request):
    return render(request, 'agent_base.html')

def field_updates(request, id):
    field = get_object_or_404(Field, id=id)
    updates = FieldUpdate.objects.filter(field=field).order_by('-date')

    return render(request, 'field_updates.html', {
        'field': field,
        'updates': updates
    })

# ---------------- REGISTER ----------------
def register_view(request):
    form = RegisterForm()

    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)

            # ROLE REDIRECT
            if user.role == "admin":
                return redirect("dashboard")
            else:
                return redirect("agent_dashboard")

    return render(request, "register.html", {"form": form})


# ---------------- LOGIN ----------------
def login_view(request):

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            
            if user.is_superuser or user.role == "admin":
                return redirect("dashboard")

            elif user.role == "agent":
                return redirect("agent_dashboard")

            else:
                return redirect("login")

        return render(request, "login.html", {"error": "Invalid credentials"})

    return render(request, "login.html")


# ---------------- LOGOUT ----------------
def logout_view(request):
    logout(request)
    return redirect("login")


from django.contrib.auth.decorators import login_required

@login_required
def agent_dashboard(request):


    fields = Field.objects.filter(assigned_agent=request.user)
    # fields = Field.objects.filter(assigned_agent=request.user.username)

    total_fields = fields.count()
    active = sum(1 for f in fields if f.status() == "Active")
    at_risk = sum(1 for f in fields if f.status() == "At Risk")
    completed = sum(1 for f in fields if f.status() == "Completed")

    return render(request, "agent_dashboard.html", {
        "fields": fields,
        "total_fields": total_fields,
        "active": active,
        "at_risk": at_risk,
        "completed": completed,
        "agent_name": request.user.username
    })