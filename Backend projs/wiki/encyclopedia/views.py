from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.http.response import HttpResponse
from random import choice
from django import forms
import markdown
import re


from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request , TITLE):
    content = util.get_entry(TITLE)
    
    if content:
        return render(request, "encyclopedia/entries.html" , {
        "title": TITLE,
        "content": markdown.markdown(content)
        })
    else:   
        return render(request, "encyclopedia/error.html" , {
            "message" : TITLE +" does not exist"
        })

def search(request):
    q = request.GET['q']
    content = util.get_entry(q)

    if content:
        return HttpResponseRedirect(reverse('wiki_entry', args=[q]))
    else:
        entries = util.list_entries()
        possibilities = []
        string = re.compile("(?i)(" + q + ")")

        for entry in entries:
            if string.search(entry):
                possibilities.append(entry)

        return render(request, "encyclopedia/search.html", {
            "string": q,
            "possibilities": possibilities
        })

def random(request):
    title = choice(util.list_entries())
    return HttpResponseRedirect(reverse('wiki_entry', args=[title]))

class NewPageForm(forms.Form):
    title = forms.CharField(label="Title:", widget=forms.TextInput(attrs={'class': 'form-control w-75 mb-2'}))
    description = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control w-75'}), label="Description:")

def newpage(request):
    if request.method == "POST":
        form = NewPageForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            description = form.cleaned_data["description"]
            if (util.get_entry(title)):
                return render(request,"encyclopedia/error.html", {
                    "message": "This entry already exists."
                })
            else:
                util.save_entry(title, description)
                return HttpResponseRedirect(reverse('wiki_entry', args=[title]))
    else:
        return render(request, "encyclopedia/newpage.html", {
                "form": NewPageForm()
            })  

class EditPageForm(forms.Form):
    edit_content = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'cols': '90'}), label="Description:")

def edit(request, title):
    form = EditPageForm(initial={'edit_content': util.get_entry(title)})

    if request.method == "POST":
        update = EditPageForm(request.POST)
        if update.is_valid():
            newcontent = update.cleaned_data["edit_content"]
            util.save_entry(title, newcontent)
            return HttpResponseRedirect(reverse('wiki_entry', args=[title]))
    else:
        return render(request, "encyclopedia/edit.html", {
            "title": title,
            "form": form
        })  