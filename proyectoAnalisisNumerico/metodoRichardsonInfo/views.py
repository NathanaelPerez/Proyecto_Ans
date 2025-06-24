from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def home_info(request):
    return render(request, 'informativa_Richardson.html')
