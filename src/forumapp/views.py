from django.shortcuts import render
from forumapp.forms import ForumForm


# Create your views here.
def index(request):
    return render(request, "forumapp/index.html")


def create_forum(request):
    if request.method == "POST":
        form = ForumForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, "forumapp/index.html")
    else:
        form = ForumForm()
    return render(request, "forumapp/create_forum.html", {"form": form})
