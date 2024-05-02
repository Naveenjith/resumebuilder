from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Resume
from .forms import ResumeForm
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
# ----------------------------------------------#
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from io import BytesIO
from reportlab.lib.units import inch
from reportlab.lib.utils import ImageReader
from reportlab.lib import colors
from django.template.loader import render_to_string
from xhtml2pdf import pisa
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Resume

# Create your views here.
def index(request):
    return render(request,'index.html')

def home(request):
    return render(request,'home.html')


# ---------------------------------------------------------------#

@login_required
def create_resume(request):
    if request.method == 'POST':
        form = ResumeForm(request.POST,request.FILES)
        if form.is_valid():
            resume = form.save(commit=False)
            resume.user = request.user
            resume.save()
            return redirect('view_resume')
    else:
        form = ResumeForm()
    return render(request, 'resume_form.html', {'form': form})

@login_required
def update_resume(request, pk):
    resume = get_object_or_404(Resume, pk=pk, user=request.user)
    if request.method == 'POST':
        form = ResumeForm(request.POST, instance=resume)
        if form.is_valid():
            form.save()
            return redirect('view_resume')
    else:
        form = ResumeForm(instance=resume)
    return render(request, 'resume_form.html', {'form': form})

@login_required
def view_resume(request):
    resumes = Resume.objects.filter(user=request.user)
    return render(request, 'resume_view.html', {'resumes': resumes})


# ----------------------------------------------------------------#
def loginview(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            uname = form.cleaned_data['username']
            pwrd = form.cleaned_data['password']
            user = authenticate(request, username=uname, password=pwrd)
            if user is not None:
                login(request, user)
                return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, "registration/login.html", {'form': form})


        
def logout_view(request):
    logout(request)
    return redirect('login')


def sign_up(request):
        uform = UserCreationForm(request.POST)
        if request.method == "POST":
            if uform.is_valid():
                uname = uform.cleaned_data.get('username')
                pwrd = uform.cleaned_data.get('password1')
                email=uform.cleaned_data.get('email')
                user1=User.objects.create_user(username=uname,password=pwrd,email=email)
                user1.save()
                user = authenticate(request, username=uname, password=pwrd)
                login(request,user)
                return redirect('home')
        else:
            uform = UserCreationForm()
        return render(request, 'registration/sign_up.html', {'form': uform})
    
def Resethome(request):
    return render(request,'registration/ResetPassword.html')

def resetPassword(request):
    responseDic={}
    try:
        usern = request.POST['username']
        recepient=request.POST['email']
        pwd=request.POST['password']
        #subject="Password reset"
        try:
            user=User.objects.get(uname=usern)
            if user is not None:
                user.set_password(pwd)
                user.save()
                #send_mail(subject,message, EMAIL_HOST_USER, [recepient])
                responseDic["errmsg"]="Password Reset Successfully"
                return render(request,"registration/ResetPassword.html",responseDic)
        except Exception as e:
            print(e)
            responseDic["errmsg"]="Email doesnt exist"
            return render(request,"registration/ResetPassword.html",responseDic)
        
    except Exception as e:
        print(e)
        responseDic["errmsg"]="Failed to reset password"
        return render(request,"registration/ResetPassword.html",responseDic)
# ---------------------------download-----------------------#


from django.template.loader import render_to_string
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from xhtml2pdf import pisa
from .models import Resume
import base64

@login_required
def download_resume(request, pk):
    resume = get_object_or_404(Resume, pk=pk, user=request.user)

    # Encode the image data to base64
    if resume.image:
        with open(resume.image.path, "rb") as image_file:
            encoded_image = base64.b64encode(image_file.read()).decode('utf-8')
    else:
        encoded_image = None

    # Render the resume details into an HTML template
    html = render_to_string('resume_template.html', {'resume': resume, 'encoded_image': encoded_image})

    # Create a PDF file
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="resume.pdf"'

    # Convert HTML to PDF
    pisa_status = pisa.CreatePDF(html, dest=response)
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')

    return response
