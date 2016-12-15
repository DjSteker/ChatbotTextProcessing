from django.conf.urls import url

from api import views
from api.views import nltkAcronymToPartOfSpeech, nltkAnnotateSentence

urlpatterns = [
    url(r'^$', views.index, name="index"),
    url(r'^nltk/part-of-speech.*$', name="nltkAcronymToPartOfSpeech", view=nltkAcronymToPartOfSpeech),
    url(r'^nltk/sentence-annotation.*$', name="nltkAnnotateSentence", view=nltkAnnotateSentence),
    url(r'^.*$', views.unknownRoute, name='unknownRoute')
]
