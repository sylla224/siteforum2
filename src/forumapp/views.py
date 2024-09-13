import datetime

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from forumapp.forms import ForumForm, LoginForm, ConnexionForum, MessageForm
from account.models import ForumUser
from forumapp.models import MemberForum, Forum, Thread, Message


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
    forum = get_object_or_404(Forum, slug=slug)
    # i get all members user of the forum
    # members_of_forum = MemberForum.objects.filter(forum_id=forum.id, user_id=request.user.id)
    members_of_forum = get_object_or_404(MemberForum, forum_id=forum.id, user_id=request.user.id)
    # i get all threads of the forum
    threads = Thread.objects.filter(identifiant_forum=forum.id)
    # i get all messages of the threads
    messages = [message for thread in threads for message in Message.objects.filter(thread_in=thread.id) if
                message.parent is None]
    # i get all the replies of the messages
    replies = [reply for message in messages for reply in Message.objects.filter(parent=message.id)]
    # i want to count the number of replies of each message
    number_of_replies = dict()
    for message in Message.objects.all():
        number_of_replies[message.id] = len(Message.objects.filter(parent=message.id))
    if forum:
        context_forum = {
            "forum": forum,
            "messages": messages,
            "members": members_of_forum,
            "replies": replies,
            "replies_count": number_of_replies,
        }
        return render(request, "forumapp/forum.html", context=context_forum)
    return render(request, "forumapp/forum.html", {"forum": forum})


def post_forum_messages(request):
    if request.method == "POST":
        form = MessageForm(request.POST)
        title_du_message = request.POST.get("titre")
        content_du_message = request.POST.get("contenu")
        forum_id = request.POST.get("forum_id")
        if form.is_valid():
            print("helllo world")
            member_exist = get_object_or_404(MemberForum, user_id=request.user.id, forum_id=forum_id)
            forum_du_user_category = member_exist.forum.identifiant_category
            # i want to create a new thread before creating a message
            thread = Thread.objects.create(name=title_du_message, created_by=request.user,
                                           identifiant_forum=member_exist.forum,
                                           created_at=datetime.datetime.now, updated_at=datetime.datetime.now)
            thread.save()
            form_instance = form.save(commit=False)
            form_instance.posted_by = request.user
            form_instance.published_at = datetime.datetime.now()
            form_instance.thread_in_id = thread.id
            form_instance.save()
            # recuperation des donnes du context
            # members_of_forum = get_object_or_404(MemberForum, forum_id=forum_id, user_id=request.user.id)
            threads = Thread.objects.filter(identifiant_forum=forum_id)
            messages = [message for thread in threads for message in Message.objects.filter(thread_in=thread.id)]
            context = {
                "forum": member_exist.forum,
                "messages": messages,
                "members": member_exist
            }
            # return render(request=request, template_name="forumapp/forum.html", context=context)
            return redirect("forumapp:forum_slug", slug=member_exist.forum.slug)
        else:
            print(form.errors)
    else:
        form = MessageForm()
        return render(request, "forumapp/new_message.html", {"form": form})


def message_reply_request(request, message_id):
    message = get_object_or_404(Message, id=message_id)
    if request.method == "POST":
        form = MessageForm(request.POST)
        if form.is_valid():
            form_instance = form.save(commit=False)
            form_instance.posted_by = request.user
            form_instance.published_at = datetime.datetime.now()
            form_instance.thread_in_id = message.thread_in_id
            form_instance.parent = message
            form_instance.save()
            return redirect("forumapp:forum_slug", slug=message.thread_in.identifiant_forum.slug)
    else:
        form = MessageForm()
        return render(request, "forumapp/new_message.html", {"form": form})


def edit_message(request, message_id):
    message = get_object_or_404(Message, id=message_id)
    if request.method == "POST":
        form = MessageForm(request.POST, instance=message)
        if form.is_valid():
            form.save()
            return redirect('forumapp:forum_slug', slug=message.thread_in.identifiant_forum.slug)
    else:
        form = MessageForm(instance=message)
    return render(request, 'forumapp/edit_message.html', {'form': form})


@login_required
def delete_message(request, message_id):
    message = get_object_or_404(Message, id=message_id)
    if request.user == message.posted_by:
        message.delete()
    return redirect('forumapp:forum_slug', slug=message.thread_in.identifiant_forum.slug)


def delete_sub_message(request, reply_id):
    reply = get_object_or_404(Message, id=reply_id)
    reply.delete()
    return redirect('forumapp:forum_slug', slug=reply.thread_in.identifiant_forum.slug)
