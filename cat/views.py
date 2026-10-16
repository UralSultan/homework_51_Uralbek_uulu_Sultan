from random import randint

from django.shortcuts import redirect, render

from .models import Cat


SESSION_CAT_ID = 'cat_id'

SAD_AVATAR = 'cat/images/cat_sad.jpg'
CALM_AVATAR = 'cat/images/cat_calm.jpg'
HAPPY_AVATAR = 'cat/images/cat_happy.jpg'
SLEEPING_AVATAR = 'cat/images/cat_sleeping.jpg'


def normalize_stats(cat):
    cat.fullness = max(0, min(100, cat.fullness))
    cat.happiness = max(0, min(100, cat.happiness))


def feed_cat(cat):
    if cat.is_sleeping:
        return

    cat.fullness += 15
    cat.happiness += 5

    if cat.fullness > 100:
        cat.happiness -= 30

    normalize_stats(cat)


def play_with_cat(cat):
    if cat.is_sleeping:
        cat.is_sleeping = False
        cat.happiness -= 5
        normalize_stats(cat)
        return

    cat.happiness += 15
    cat.fullness -= 10

    if randint(1, 3) == 1:
        cat.happiness = 0

    normalize_stats(cat)


def put_cat_to_sleep(cat):
    cat.is_sleeping = True
    normalize_stats(cat)


def perform_cat_action(cat, action):
    if action == 'feed':
        feed_cat(cat)
    elif action == 'play':
        play_with_cat(cat)
    elif action == 'sleep':
        put_cat_to_sleep(cat)


def get_cat_avatar(cat):
    if cat.is_sleeping:
        return SLEEPING_AVATAR
    if cat.happiness <= 30:
        return SAD_AVATAR
    if cat.happiness <= 70:
        return CALM_AVATAR
    return HAPPY_AVATAR


def get_cat_mood(cat):
    if cat.is_sleeping:
        return 'спит'
    if cat.happiness <= 30:
        return 'грустит'
    if cat.happiness <= 70:
        return 'спокоен'
    return 'счастлив'


def index(request):
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        if name:
            cat = Cat.objects.create(name=name)
            request.session[SESSION_CAT_ID] = cat.id
            return redirect('cat_info')

    return render(request, 'cat/index.html')


def cat_info(request):
    cat_id = request.session.get(SESSION_CAT_ID)
    if not cat_id:
        return redirect('index')

    try:
        cat = Cat.objects.get(id=cat_id)
    except Cat.DoesNotExist:
        return redirect('index')

    if request.method == 'POST':
        perform_cat_action(cat, request.POST.get('action'))
        cat.save()
        return redirect('cat_info')

    context = {
        'cat': cat,
        'avatar': get_cat_avatar(cat),
        'mood': get_cat_mood(cat),
    }
    return render(request, 'cat/cat_info.html', context)
