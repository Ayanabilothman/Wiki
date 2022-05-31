from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from . import util
from django import forms
from random import choices

class Create_Edit_Form(forms.Form):
    content = forms.CharField(widget=forms.Textarea, label="")

class Create_New_Form(forms.Form):
    title = forms.CharField(max_length=100, label="", widget=forms.TextInput(attrs={'placeholder': 'Entry Title'}))
    content = forms.CharField(label="", widget= forms.Textarea(attrs={'placeholder': 'Entry Content in Markdown'}))


def index(request):
    if request.method == "POST":
        keyword = request.POST['q']
        if keyword.lower() in map(lambda file: file.lower(), util.list_entries()):
            return HttpResponseRedirect(reverse("encyclopedia:entry",
            kwargs = {"entry":keyword}))
        else:
            return HttpResponseRedirect(reverse("encyclopedia:search",
            kwargs = {"keyword":keyword}))

    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def display_entry(request, entry):
    return render(request, "encyclopedia/entry.html", {
    "entry": entry,
    "content": util.to_HTML(entry)})

def edit(request, entry):
    if request.method == "POST":
        submitted_data = Create_Edit_Form(request.POST) # As if I create an object from this class and pass the data that the user sumbit, request.POST is a dictionary where the keys are the boxes the user enter the data in and the values are the data themselves
        if submitted_data.is_valid():
            content = submitted_data.cleaned_data['content']
            util.edit_entry(entry, content)
            return HttpResponseRedirect(reverse("encyclopedia:entry", kwargs = {"entry": entry}))

        else:
            return render(request, "encyclopedia/edit.html", {
            "form": submitted_data,
            "entry": entry})

    data = Create_Edit_Form(initial = {"content": util.get_entry(entry)})
    return render(request, "encyclopedia/edit.html", {
    "form": data,
    "entry": entry})

def search(request, keyword):
    results = util.check(keyword, util.list_entries())
    return render(request, "encyclopedia/search.html", {
        "keyword": keyword,
        "results": results
    })


def new(request):
    message = ""
    if request.method == "POST":
        submitted_data= Create_New_Form(request.POST)
        if submitted_data.is_valid():
            title = submitted_data.cleaned_data['title']
            content = submitted_data.cleaned_data['content']

            if title.lower() not in map(lambda file: file.lower(), util.list_entries()):
                util.save_entry(title, content)
                return HttpResponseRedirect(reverse("encyclopedia:entry",
                kwargs = {"entry": title}))
            else:
                message = "Sorry this entry already exist!"

    return render(request, "encyclopedia/new.html", {
    "form": Create_New_Form(),
    "message": message
    })

def random(request):
    return HttpResponseRedirect(reverse("encyclopedia:entry",
    kwargs = {"entry": choices(util.list_entries(), k=1)[0]}))
