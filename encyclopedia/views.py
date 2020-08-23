from django.shortcuts import render
from . import util
from django.http import HttpResponseRedirect
from django.urls import reverse
from django import forms
import random
from django.shortcuts import redirect
import markdown2

#Style parameters
style = 'form-control w-75 m-3'


class NewPageForm(forms.Form):
    entry_title = forms.CharField(label="", widget=forms.TextInput(attrs={'class' : style,'placeholder': 'Title...'}))
    entry_text = forms.CharField(label="", widget=forms.Textarea(attrs={'class' : style, 'placeholder':'Write entry...'}))
 
class EditPageForm(forms.Form):
    entry_text = forms.CharField(label="", widget=forms.Textarea(attrs={'class' : style, 'placeholder':'Write entry...'}))

    
def index(request):
    if request.POST.get("search"):
        return searchResults(request, request.POST.get("search"))
    
    return render(request, 'encyclopedia/index.html', {'entries': util.list_entries()})


def createpage(request):
    if request.POST.get("search"):
        return entry(request, request.POST.get("search"))
    
    if(request.POST.get("PostEntry")):
        
        form = NewPageForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['entry_title']
            content = form.cleaned_data['entry_text']
            
            if title.casefold() in (entry.casefold() for entry in util.list_entries()):
                title = util.title(title)
                return render(request, "encyclopedia/createpage.html", {'new_page_form': form,'message':f'Page with title "{title}" already exists'})
            else:
                util.save_entry(title,content)
                return HttpResponseRedirect(reverse('wiki:entry',kwargs={'title':title}))
        else:
            return render(request, "encyclopedia/createpage.html",{ "new_page_form": form })
       
    return render(request, "encyclopedia/createpage.html", {
        "new_page_form": NewPageForm()
    })
        
    
def entry(request, title):
    
    if not util.entry_exists(title):
        return noSuchPage(request,title)
    if request.POST.get('search'):
        return searchResults(request,request.POST.get('search'))
    
    title = util.title(title)
    return render(request,'encyclopedia/entry.html',{'title':title,'content': markdown2.markdown(util.get_entry(title),safe_mode=True)})


def edit(request,title):
    if request.POST.get('search'):
        return searchResults(request,request.POST.get('search'))
    
    form = EditPageForm(initial={'entry_text':util.get_entry(title)})
    
    if request.POST.get('EditEntry'):
        form = EditPageForm(request.POST,initial={'entry_text': util.get_entry(title)})
        
        if form.is_valid():
            content = form.cleaned_data['entry_text']
            util.save_entry(title,content)
            return HttpResponseRedirect(reverse('wiki:entry',kwargs={'title': title}))
        else:
            return render(request, "encyclopedia/editpage.html",{ "edit_page_form": form })
        
    return render(request, "encyclopedia/editpage.html", {
        "edit_page_form": form, 'title': title})

      
def noSuchPage(request, search):
    if request.POST.get('search'):
        return searchResults(request, request.POST.get('search'))
    
    return render(request, "encyclopedia/nosuchpage.html",{
        "search": search
    })

def searchResults(request, search):
    if util.entry_exists(request.POST.get('search')):
            content = (util.get_entry(request.POST.get('search')))
            return HttpResponseRedirect(reverse('wiki:entry',kwargs={'title': util.title(request.POST.get('search'))}))
        
    results = []
    for title in util.list_entries():
        if title.casefold().startswith(search.casefold()):
            results.append(title)
    request.session['results'] = results
    
    if results:
        return HttpResponseRedirect(reverse('wiki:matches'))
    else:
        return HttpResponseRedirect(reverse('wiki:nosuchpage',kwargs={'search':search}))

def randompage(request):
    randomTitle = random.choice(util.list_entries())
    return HttpResponseRedirect(reverse('wiki:entry', kwargs = {'title': randomTitle}))
    
    
def matches(request):
    if request.POST.get("search"):
        return searchResults(request, request.POST.get("search"))
    results = request.session['results']
    return render(request, 'encyclopedia/matches.html', {'entries': results})
    
