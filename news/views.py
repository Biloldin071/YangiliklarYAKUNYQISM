# 🔚🔜
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse



from django.db.models import Q

from hitcount.utils import get_hitcount_model
from hitcount.views import HitCountMixin

from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView, UpdateView, DeleteView, CreateView


from .models import News, Category

from news_lohih.custom_permissions import OnlyLoggedSuperUser

from .forms import ContactForm, CommentForm





def news_list_view(request):
    news_list = News.published.all()
    top_news = News.published.all()[:5]


    local_one = News.published.filter(category__name='Mahalliy')[0]
    local_news = News.published.filter(category__name='Mahalliy')[1:4]

    fashionn_none = News.published.filter(category__name='Xorij')[0]
    fashin_news = News.published.filter(category__name='Xorij')[1:3]

    technalog_noon = News.published.filter(category__name='Sport')[0]
    technalogiy_news = News.published.filter(category__name='Sport')[1:3]

    iqtisod_game = News.published.filter(category__name='Iqtisodiy')[0]
    iqtisod_gam = News.published.filter(category__name='Iqtisodiy')[1:3]

    # yangilik_lar = News.published.filter(category__name='Yangiliklar')[0]
    #yangilik_larr = News.published.filter(category__name='Yangiliklar')[1:4]


    context = {
        'news_list': news_list,
        'top_news': top_news,
        #Mahalliy
        'local_one': local_one,
        'local_news': local_news,
        #Xorij
        'fashionn_none': fashionn_none,
        'fashin_news': fashin_news,
        #Sport
        'technalog_noon': technalog_noon,
        'technalogiy_news': technalogiy_news,
        #Iqtisod
        'iqtisod_game': iqtisod_game,
        'iqtisod_gam': iqtisod_gam,
        #yangilik
        #'yangilik_lar': yangilik_lar,
        #'yangilik_larr': yangilik_larr,
    }
    return render(request, template_name='home.html', context=context)




def news_detail_view(request,slug):
    news_detail = get_object_or_404(News, slug = slug, status = News.Status.Published)

    context = {}

    hit_count = get_hitcount_model().objects.get_for_object(news_detail)
    hits = hit_count.hits
    hitcontext = context['hitcount'] = {'pk': hit_count.pk}
    hit_count_response = HitCountMixin.hit_count(request, hit_count)
    if hit_count_response.hit_counted:
        hits = hits + 1
        hitcontext['hit_counted'] = hit_count_response.hit_counted
        hitcontext['hit_message'] = hit_count_response.hit_message
        hitcontext['total_hits'] = hits


    comments = news_detail.comments.filter(active=True)
    new_comment = None
    comment_count = len(comments)

    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():

            new_comment = comment_form.save(commit=False)
            new_comment.news = news_detail
            new_comment.user = request.user
            new_comment.save()
            comment_form = CommentForm()

    else:
        comment_form = CommentForm()


    context = {
        "news_detail" : news_detail,
        'comments' : comments,
        'new_comment': new_comment,
        'comment_form' : comment_form,
        'comment_count' : comment_count,
    }

    return render(request,"single_page.html",context)





class SearchResultsList(ListView):
    model = News
    template_name = 'search_results.html'
    context_object_name = 'barcha_yangiliklar'


    def get_queryset(self):
        query = self.request.GET.get('q')
        return News.objects.filter(
            Q(title__icontains=query) | Q(body__icontains=query)
        )



def contact_view(request):
    form = ContactForm(request.POST)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return HttpResponse("<h2>Biz bilan bog'langaningiz uchun tashakkur</h2>")

    context = {
        'form' : form
    }
    return render(request,'contact.html',context)



def about_us_view(request):
    context = {

    }

    return render(request, 'about_us.html', context)


def Mahalliy_view(request):
    news_detail = News.objects.filter(category__name = 'Mahalliy')
    context = {
        'local_news': news_detail

    }

    return render(request, 'Mahalliy.html', context)


def xorij_view(request):
    news_detail = News.objects.filter(category__name = 'Xorij')
    context = {
        'local_news': news_detail

    }

    return render(request, 'xorij.html', context)



def sport_view(request):
    news_detail = News.objects.filter(category__name = 'Sport')
    context = {
        'local_news': news_detail

    }

    return render(request, 'sport.html', context)


def iqtisod_view(request):
    news_detail = News.objects.filter(category__name = 'Iqtisodiy')
    context = {
        'local_news': news_detail

    }

    return render(request, 'iqtisod.html', context)









class NewsUpdateView(OnlyLoggedSuperUser, UpdateView):
    template_name = 'crud/update.html'
    model = News
    fields = ['title', 'slug', 'body', 'image']


class NewsDeleteView(OnlyLoggedSuperUser, DeleteView):
    model = News
    template_name = 'crud/delete.html'
    success_url = reverse_lazy('home_page')


class NewsCreateView(OnlyLoggedSuperUser,  CreateView):
    model = News
    fields = ('title','slug','image','body','category','status')
    template_name = 'crud/create.html'

