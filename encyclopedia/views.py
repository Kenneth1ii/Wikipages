import markdown2
import random
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django import forms
from django.shortcuts import redirect
from . import util


class Newpageform(forms.Form):
    title = forms.CharField(label = "title" ) # variable title is the key dictionary.
    markdown = forms.CharField(widget=forms.Textarea, label="markdown")



def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def entry(request, title):
    if not util.get_entry(title):
        return render(request, "encyclopedia/notfound.html", {
            "title": title
        })
    else:
        print(title)
        return render(request, "encyclopedia/entry.html", {
            "title": title,
            "data": markdown2.markdown(util.get_entry(title)),
        })

def search(request):
    if request.POST.get('q'):
        temp = request.POST.get('q')
        if util.get_entry(temp):
            return render(request, "encyclopedia/entry.html", {
            "data": markdown2.markdown(util.get_entry(temp))
        })
        else:
            newentry = []
            entry = util.list_entries()
            for D in entry:
                if temp.lower() in D.lower():
                    newentry.append(D)
            return render(request, "encyclopedia/searchresults.html", {
                "searchresults": newentry
            })
    else:
        return render(request,"encyclopedia/searchresults.html")
    

def newpage(request):
    if request.method == "POST":
        form = Newpageform(request.POST)
        if form.is_valid():
            newdata = form.cleaned_data
            title = newdata["title"]
            markdown = newdata["markdown"]
            util.save_entry(title,markdown)
            return HttpResponseRedirect(reverse("index"))

    return render(request, 'encyclopedia/newpage.html', {
            "form": Newpageform()
        })

def editpage(request, title):
    f = Newpageform(initial={'title': title, 'markdown': util.get_entry(title) })

    if request.method == "POST":
        form = Newpageform(request.POST)
        if form.is_valid():
            newdata = form.cleaned_data
            title = newdata["title"]
            markdown = newdata["markdown"]
            util.save_entry(title,markdown)
            return HttpResponseRedirect(reverse("index"))

    return render(request,f"encyclopedia/editpage.html",{
        'form': f
    })

def randoms(request):
    listcount = len(util.list_entries()) - 1
    seed = random.randint(0,listcount)
    entry = util.list_entries()[seed]
    return redirect(f'/{entry}')

