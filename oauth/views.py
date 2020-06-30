from evernote.api.client import EvernoteClient
import evernote.edam.type.ttypes as Types
from django.urls import reverse
from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib import messages
from django.http import HttpResponse
from .config import EN_CONSUMER_KEY, EN_CONSUMER_SECRET
from feed.models import Post

def get_evernote_client(token=None):
	if token:
		return EvernoteClient(token=token, sandbox=True)
	else:
		return EvernoteClient(
			consumer_key=EN_CONSUMER_KEY,
			consumer_secret=EN_CONSUMER_SECRET,
			sandbox=True
		)


def index(request):
	return render(request, 'oauth/index.html', {})


def auth(request, post_id):
	request.session['access_token'] = 'S=s1:U=95fbd:E=17a5ccf31de:C=173051e0400:P=185:A=laurence485-1218:V=2:H=1e53ca4018479345d0f9f1e2069e8b02'

	try:
		client = EvernoteClient(token=request.session['access_token'])
		# note_store = client.get_note_store()
		send_to_evernote(client)

		messages.success(request, 'Notes successfully sent to Evernote.')

		return redirect(reverse('post-detail', kwargs={'pk':post_id}))

	except:
		client = get_evernote_client()
		callbackUrl = 'http://%s%s' % (
			request.get_host(), reverse('evernote_callback'))
		request_token = client.get_request_token(callbackUrl)

		# Save the request token information for later
		request.session['oauth_token'] = request_token['oauth_token']
		request.session['oauth_token_secret'] = request_token['oauth_token_secret']

		# 	# Redirect the user to the Evernote authorization URL
		return redirect(client.get_authorize_url(request_token))

def send_to_evernote(client):
	'''create specified notes inside evernote'''
	try:
		noteStore = client.get_note_store()
		notebooks = noteStore.listNotebooks()
		for n in notebooks:
			print (n.name, n.guid)

		notebook_guid = "95069c18-ac04-42e2-84cf-b6b9314e78b7"
		notebook_name = "My Notebook"

		noteStore = client.get_note_store()
		note = Types.Note()
		note.title = "I'm a test note!"
		note.content = '<?xml version="1.0" encoding="UTF-8"?><!DOCTYPE en-note SYSTEM "http://xml.evernote.com/pub/enml2.dtd">'
		note.content += '<en-note><strong>Hello world test!</strong></en-note>'
		note.tagNames = ['author', 'cat1','cat2']
		note.notebookGuid = notebook_guid
		note = noteStore.createNote(note)

		print(f"Successfully created a new note in notebook: {notebook_name}, with GUID: {notebook_guid}" )
	except:
		print("Could not create note.")

def callback(request):
	try:
		client = get_evernote_client()
		client.get_access_token(
			request.session['oauth_token'],
			request.session['oauth_token_secret'],
			request.GET.get('oauth_verifier', '')
		)
	except KeyError:
		messages.warning(request, 'Could not connect to Evernote.')
		return redirect('/')

	send_to_evernote(client)
	
	return render(request, 'oauth/callback.html', {'notebooks': notebooks})


def reset(request):
	return redirect('/')