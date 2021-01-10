from django.http import Http404, HttpResponse 
from django.shortcuts import render 

#Crete your views here.
def index(request):
    return render(request, "singlepage/index.html")


texts = ["Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua." , 
    "Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.", 
    "Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."]

def section(request, num):
    if 1 <= num <=3:
        return HttpResponse(texts[num-1])
    else:
        raise Http404("No such section")