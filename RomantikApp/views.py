import datetime
import json
import os
from .modules.compressor import ImageCompressor

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import View

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.core.files.storage import default_storage

from romantik.settings import MEDIA_ROOT, secret_settings
from .models import *
from .code.views_functions import *

from asgiref.sync import sync_to_async, async_to_sync

telegram_parser = TelergamParser()

class HomePage(View):
    def get(self, request):

        print(telegram_parser.load_updates())
        
        context = base_context(request)
        context['page_name'] = 'home'
        return render(request, "home.html", context)


class NewsPage(View):
    def get(self, request):

        context = base_context(request, title='Новини', header='Новини')

        news = sorted(NewsPost.objects.all(), key=lambda obj: obj.datetime)
        news.reverse()
        news = news[:5]

        news_dict = []

        for news_post in news:
            upvotes = UpVote.objects.filter(news=news_post)
            downvotes = DownVote.objects.filter(news=news_post)

            int_total_raiting = upvotes.count() - downvotes.count()
            total_raiting = str(int_total_raiting)
            if int_total_raiting > 0:
                total_raiting = "+"+str(int_total_raiting)
            else:
                total_raiting = str(int_total_raiting)

            comments_number = Comment.objects.filter(
                news_post=news_post).count()

            if request.user.is_authenticated:
                user_upvoted = 'yes' if len(UpVote.objects.filter(
                    news=news_post).filter(user=request.user)) != 0 else 'no'
                user_downvoted = 'yes' if len(DownVote.objects.filter(
                    news=news_post).filter(user=request.user)) != 0 else 'no'
            else:
                user_upvoted = 'no'
                user_downvoted = 'no'

            news_dict.append({
                'post_id': news_post.id,
                'post': news_post,
                'total_raiting': total_raiting,
                'upvotes': upvotes,
                'downvotes': downvotes,
                'user_upvoted': user_upvoted,
                'user_downvoted': user_downvoted,
                'comments_number': comments_number,
                'author_full_name': full_name(news_post.user),
                'author_avatar': get_avatar(news_post.user),
                'beauty_datetime': beautify_datetime(news_post.datetime)
                })

        context['news'] = news_dict
        return render(request, "news.html", context)


class PostEditor(View, LoginRequiredMixin):
    def get(self, request, post_id):
        context = base_context(request, title='Редагування', header='Редагування')

        if not len(list(NewsPost.objects.filter(id=post_id))):
            return handler404(request)
        
        context['post'] = NewsPost.objects.get(id=post_id)

        return render(request, "edit_post.html", context)


class AjaxVotePost(View, LoginRequiredMixin):
    def post(self, request):
        form = request.POST
        result = {}
        result['vote_cancelled'] = 'false'
        news_post_exists = True if NewsPost.objects.filter(
            id=form["post_id"]) else False

        if news_post_exists:
            news_post = NewsPost.objects.get(id=form["post_id"])

            if form["vote_type"] == "upvote":

                if len(DownVote.objects.filter(news=news_post, user=request.user)) != 0:
                    downvote = DownVote.objects.filter(
                        news=news_post, user=request.user)[0]
                    downvote.delete()
                    result['vote_cancelled'] = 'true'

                elif UpVote.objects.filter(news=news_post, user=request.user):
                    pass
                else:
                    upvote = UpVote(news=news_post, user=request.user)
                    upvote.save()

            elif form["vote_type"] == "downvote":

                if len(UpVote.objects.filter(news=news_post, user=request.user)) != 0:
                    upvote = UpVote.objects.filter(
                        news=news_post, user=request.user)[0]
                    upvote.delete()
                    result['vote_cancelled'] = 'true'

                elif DownVote.objects.filter(news=news_post, user=request.user):
                    pass
                else:
                    downvote = DownVote(news=news_post, user=request.user)
                    downvote.save()

        upvotes = UpVote.objects.filter(news=news_post)
        downvotes = DownVote.objects.filter(news=news_post)

        int_total_raiting = upvotes.count() - downvotes.count()
        total_raiting = str(int_total_raiting)
        if int_total_raiting > 0:
            total_raiting = "+"+str(int_total_raiting)
        else:
            total_raiting = str(int_total_raiting)

        result['total_raiting'] = total_raiting
        result["result"] = "success"
        return HttpResponse(
            json.dumps(result),
            content_type="application/json"
        )


class AjaxPublishPost(View, LoginRequiredMixin):
    def post(self, request):
        form = request.POST

        news_post = NewsPost(
            user=request.user,
            datetime=datetime.datetime.now(),
            content=form['news_content'],
            img_paths=""
        )
        news_post.save()

        result = {}
        result["result"] = "success"
        return HttpResponse(
            json.dumps(result),
            content_type="application/json"
        )
    

class AjaxAddPhotoToPost(View, LoginRequiredMixin):
    def post(self, request):
        form = request.POST

        # filename =
        uploaded_file = request.FILES['upload']

        file_name = datetime.datetime.now().strftime(
            "%d_%m_%Y_%H_%M_%S") + '_' + uploaded_file.name

        file_path = default_storage.save(file_name, uploaded_file)

        abs_file_path = os.path.join(MEDIA_ROOT, file_name)

        ImageCompressor().process(abs_file_path)

        result = {}
        result["result"] = "success"
        result["filename"] = file_name
        result["url"] = "/media/"+file_path

        return HttpResponse(
            json.dumps(result),
            content_type="application/json"
        )


class AjaxPublishComment(View, LoginRequiredMixin):
    def post(self, request):
        form = request.POST
        result = {}

        comment = Comment(
            user=request.user,
            news_post=NewsPost.objects.get(id=form["post_id"]),
            content=form["content"]
        )
        comment.save()

        result["result"] = "success"

        return HttpResponse(
            json.dumps(result),
            content_type="application/json"
        )


class AjaxUploadUserAvatar(View, LoginRequiredMixin):
    def post(self, request):
        result = {}
        data = request.POST
        user = request.user
        user_profile = UserInfo.objects.get(user=user)
        if data['action'] == 'update':
            
            user_profile.avatar = decode_base64_file(data['secondary_data'])
            user_profile.save()
        else:
            user_profile.avatar.delete()
            user_profile.save()

        result["result"] = "success"
        return HttpResponse(json.dumps(result), content_type="application/json")
    

class AjaxUpdatePost(View, LoginRequiredMixin):
    def post(self, request):
        form = request.POST
        result = {}

        post_id = form['post_id']

        if not len(list(NewsPost.objects.filter(id=post_id))):
            result["result"] = "error"
            return HttpResponse(json.dumps(result), content_type="application/json")
        
        news_post = NewsPost.objects.get(id=post_id)

        if not news_post.user == request.user:
            result["result"] = "error"
            return HttpResponse(json.dumps(result), content_type="application/json")


        news_post.content = form['post_content']
        news_post.was_updated = True
        news_post.last_update = datetime.datetime.now()
        news_post.save()
        result["result"] = "success"
        return HttpResponse(json.dumps(result), content_type="application/json")


class Login(View):

    def __init__(self):
        self.error = 0

    def get(self, request):

        context = base_context(
            request, title='Вхід', header='Вхід', error=0)
        context['error'] = 0

        # context['form'] = self.form_class()
        return render(request, "signin.html", context)

    def post(self, request):
        context = {}
        form = request.POST

        username = form['username']
        password = form['password']

        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                context['name'] = username
                return HttpResponseRedirect("/")

        else:
            context = base_context(request, title='Вхід', header='Вхід')
            logout(request)
            context['error'] = 1
            # return Posts.get(self,request)
            return render(request, "signin.html", context)


class Logout(View):
    def get(self, request):
        logout(request)
        return HttpResponseRedirect("/")


class SignUp(View):
    def get(self, request):

        context = base_context(
            request, title='Реєстрація', header='Реєстрація', error=0)

        return render(request, "signup.html", context)

    def post(self, request):
        context = {}
        form = request.POST
        user_props = {}
        username = form['username']
        password = form['password']

        # new_post.author = Author.objects.get(id = request.POST.author)
        # new_post.save()
        user_with_this_username_already_exists = bool(User.objects.filter(username=username))
        if not user_with_this_username_already_exists:
            for prop in form:
                if prop not in ('csrfmiddlewaretoken', 'username', 'gender', 'phone_number') and form[prop] != '':
                    user_props[prop] = form[prop]

            user = User.objects.create_user(
                username=form['username'],
                first_name=form['first_name'],
                last_name=form['last_name'],
                password=form['password'])

            user_profile = UserInfo.objects.create(user=user)
            user_profile.email = form['email']

            user_profile.save()

            user = authenticate(username=username, password=password)
            login(request, user)
            return HttpResponseRedirect("/")

        else:
            context = base_context(
                request, title='Реєстрація', header='Реєстрація')

            for field_name in form.keys():
                context[field_name] = form[field_name]

            context['error'] = 1
            return render(request, "signup.html", context)


class AboutUs(View):
    def get(self, request):

        context = base_context(
            request, title='Про нас', header='Про нас', error=0)

        return render(request, "about_us.html", context)


class Rules(View):
    def get(self, request):

        context = base_context(
            request, title='Правила клубу', header='Правила клубу', error=0)

        return render(request, "rules.html", context)


class OldRules(View):
    def get(self, request):

        context = base_context(
            request, title='Правила (повні)', header='Правила клубу (повні)', error=0)

        return render(request, "old_rules.html", context)


class History(View):
    def get(self, request):

        context = base_context(
            request, title='Історія клубу', header='Історія клубу', error=0)

        return render(request, "history.html", context)


class Contacts(View):
    def get(self, request):

        context = base_context(
            request, title='Контакти', header='Контакти', error=0)

        return render(request, "contacts.html", context)


class Hymn(View):
    def get(self, request):

        context = base_context(
            request, title='Гімн клубу', header='Гімн клубу', error=0)

        return render(request, "hymn.html", context)


class FullPost(View):
    def get(self, request, post_id):
        context = base_context(
            request, title='Коментарі', header='Коментарі', error=0)

        if not NewsPost.objects.filter(id=post_id):
            return handler404(request)

        news_post = NewsPost.objects.get(id=post_id)
        context['post'] = news_post

        upvotes = UpVote.objects.filter(news=news_post)
        downvotes = DownVote.objects.filter(news=news_post)

        int_total_raiting = upvotes.count() - downvotes.count()
        total_raiting = str(int_total_raiting)
        if int_total_raiting > 0:
            total_raiting = "+"+str(int_total_raiting)
        else:
            total_raiting = str(int_total_raiting)

        if request.user.is_authenticated:
            user_upvoted = 'yes' if len(UpVote.objects.filter(
                news=news_post).filter(user=request.user)) != 0 else 'no'
            user_downvoted = 'yes' if len(DownVote.objects.filter(
                news=news_post).filter(user=request.user)) != 0 else 'no'
        else:
            user_upvoted = 'no'
            user_downvoted = 'no'

        context.update({
            'post_id': news_post.id,
            'post': news_post,
            'total_raiting': total_raiting,
            'upvotes': upvotes,
            'downvotes': downvotes,
            'user_upvoted': user_upvoted,
            'user_downvoted': user_downvoted})

        comments = sorted(Comment.objects.filter(
            news_post=news_post), key=lambda obj: obj.datetime)
        comments.reverse()

        comment_info = []

        for comment in comments:
            comment_author = comment.user
            comment_author_full_name = full_name(comment_author)
            comment_author_avatar = get_avatar(comment_author)
            comment_author_has_avatar = bool(len(comment_author_avatar))

            comment_info.append({
                'content': comment,
                'comment_author': comment_author,
                'comment_author_full_name': comment_author_full_name,
                'comment_author_has_avatar': comment_author_has_avatar,
                'comment_author_avatar': comment_author_avatar
            })
        context['comments'] = comment_info

        return render(request, "full_post.html", context)


class Hikes(View):
    def get(self, request):
        context = base_context(request, title='Походи',
                               header='Походи', error=0)
        return render(request, "hikes.html", context)


class AccountEditor(View, LoginRequiredMixin):
    def get(self, request):
        if not is_user_authenticated(request):
            return HttpResponseRedirect("/signin")

        user = request.user
        context = base_context(request, title='Мій акаунт',
                               header='Мій акаунт', error=0)

        context['user'] = user
        context['username'] = user.username
        context['first_name'] = user.first_name
        context['last_name'] = user.last_name

        if not UserInfo.objects.filter(user=user).exists():
            user_profile = UserInfo.objects.create(user=user)
            user_profile.save()

        user_profile = UserInfo.objects.get(user=user)

        context['email'] = user_profile.email
        context['phone'] = user_profile.phone
        context['telegram'] = user_profile.telegram

        context['about'] = user_profile.about
        context['avatar'] = user_profile.avatar

        context['is_email_public'] = user_profile.is_email_public
        context['is_phone_public'] = user_profile.is_phone_public
        context['is_telegram_public'] = user_profile.is_telegram_public

        return render(request, "account_editor.html", context)

    def post(self, request):

        if not is_user_authenticated(request):
            return HttpResponseRedirect("/signin")
        
        form = request.POST

        user = request.user
        user.first_name = form['first_name']
        user.last_name = form['last_name']
        user.save()

        user_profile = UserInfo.objects.get(user=user)
        user_profile.email = form['email']
        user_profile.phone = form['phone']
        user_profile.about = form['about']
        user_profile.telegram = form['telegram']

        if 'is_email_public' in form.keys():
            user_profile.is_email_public = True
        else:
            user_profile.is_email_public = False
        
        if 'is_phone_public' in form.keys():
            user_profile.is_phone_public = True
        else:
            user_profile.is_phone_public = False
        
        if 'is_telegram_public' in form.keys():
            user_profile.is_telegram_public = True
        else:
            user_profile.is_telegram_public = False

        user_profile.save()

        return HttpResponseRedirect("/my_account")
    

class UserProfile(View):
    def get(self, request, username):

        current_user = User.objects.filter(username=username)
        if len(current_user) == 0:
            return handler404(request)
        
        current_user = current_user[0]

        user_profile = None

        if len(UserInfo.objects.filter(user=current_user)):
            user_profile = UserInfo.objects.get(user=current_user)
        else:
            user_profile = UserInfo.objects.create(user=current_user)
            user_profile.save()
        
        context = base_context(request, title=current_user.username,
                               header=current_user.username, error=0)
        

        context['avatar'] = get_avatar(current_user)
        context['has_avatar'] = bool(len(context['avatar']))
        context['full_name'] = full_name(current_user)
        context['current_user'] = current_user
        context['current_user_profile'] = user_profile

        return render(request, "profile.html", context)


class ReturnRobotsTxt(View):
    def get(self, request):
        return render(request, "robots.txt", content_type="text/plain")

def handler404(request, exception=""):
    context = base_context(
        request, title='404 - Не знайдено', header='404 - Не знайдено', error=0)
    return render(request, "not_found.html", context)
