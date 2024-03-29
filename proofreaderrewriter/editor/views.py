from django.http import HttpResponse, JsonResponse
from django.shortcuts import render

from .Article_Checker import *
from .spell_checker import *
from .Tense_Checker import *
from .Demonstrative_Checker import *
from .Interrogative_Checker import *
from .Preposition_Checker import *
from .ContextSpellCheck import *
from .adj import *
from .syn import *
from .punc import *
# from scripts.Trial import *

def index(request):
	return render(request, 'editor/index.html', {})

def parser(request):
	if request.method == 'GET':
		checks = [
		spell_check, 
		SpellCheck, 
		Article_Checker,
		Tense_Checker,
		Demonstrative_Checker,
		Preposition_Checker,
		Interrogative_Checker,
		punctuation,
		adjective,
		synonym]
		s = request.GET['st']
		et = int(request.GET['type'])
		type = et;
		l = []

		for checker in checks[et:]:
			if(l == [] or sum([0 if p[1] == [] else 1 for p in l]) == 0):
				l = checker(s)
				type += 1
			else:
				break

		if(l == []):
			l = [(s,
				[])]

		return JsonResponse({'text': l, 'type': type})
	else:
		return HttpResponse("Request method is not a GET")
