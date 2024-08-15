from django.shortcuts import render, get_object_or_404, redirect
from forumapp.forms import ForumForm, LoginForm, ConnexionForum
from account.models import ForumUser
from forumapp.models import MemberForum


# Create your views here.
def index(request):
    return render(request, "forumapp/index.html")


def create_forum(request):
    if request.method == "POST":
        form = ForumForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, "forumapp/forum.html")
    else:
        form = ForumForm()
    return render(request, "forumapp/create_forum.html", {"form": form})


def signup_to_forum(request):
    if request.method == "POST":
        form_forum = LoginForm(request.POST, request.FILES)
        if form_forum.is_valid():
            forum_instance = form_forum.save(commit=False)
            forum_instance.user = request.user
            forum_instance.save()
            return render(request, "forumapp/forum.html")

    else:
        form_forum = LoginForm()
    return render(request, "forumapp/signup_forum.html", {"form": form_forum})


def connexion_to_forum(request):
    if request.method == "POST":
        userid = request.user.id
        forumid = request.POST.get("forum")
        form_forum = ConnexionForum(request.POST)
        if form_forum.is_valid():
            member_exist = get_object_or_404(MemberForum, user_id=userid, forum_id=forumid)
            if member_exist:
                context = {"avatar_url": member_exist.avatar.url if member_exist.avatar else None}
                # return render(request, "forumapp/forum.html", {"context": context})
                return redirect("forumapp:forum_slug", slug=member_exist.forum.slug)
            else:
                return render(request, "connexion_to_forum.html", {"form": form_forum})
    else:
        form_forum = ConnexionForum()
        return render(request, "forumapp/connexion_to_forum.html", {"form": form_forum})


def forum_slug(request, slug):
    return render(request, "forumapp/forum.html")


def post_forum_messages(request):
    if request.method == "POST":
        forum_id = request.POST.get("forum")
        forum = get_object_or_404(MemberForum, forum_id=forum_id)
        message_title = request.POST.get("threadTitle")
        message_contente = request.POST.get("message_content")
        print("hello post forum message")
        # forum.message = message
        forum.save()
        return render(request, "forumapp/forum.html")
    else:
        pass
    return render(request, "forumapp/forum.html")
