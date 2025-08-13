from django.http import HttpResponse
from django.shortcuts import render

def home(request):
    return render (request,'index.html')
    return HttpResponse("Hello guys, Your at the dilip initial project of home page ")

# def about(request):
#     return render(request,'about.html')
    # return HttpResponse("Hello guys, Your at the dilip initial project of about page")

# def contact(request):
#     return render(request,'contact.html')
    # return HttpResponse("Hello guys, Your at the dilip initial project of contact page ")

