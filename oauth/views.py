from evernote_sdk_python3.lib.evernote.api.client import EvernoteClient
import evernote_sdk_python3.lib.evernote.edam.type.ttypes as Types
from django.urls import reverse
from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib import messages
from django.http import HttpResponse
from .config import EN_CONSUMER_KEY, EN_CONSUMER_SECRET, MY_ACCESS_TOKEN
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
	request.session['access_token'] = MY_ACCESS_TOKEN

	try:
		client = EvernoteClient(token=request.session['access_token'])
		# note_store = client.get_note_store()
		send_to_evernote(client, post_id)

		messages.success(request, 'Notes successfully sent to Evernote.')

		return redirect(reverse('post-detail', kwargs={'pk':post_id}))

	except:
		client = get_evernote_client()
		callbackUrl = 'http://%s%s' % (
			request.get_host(), reverse('evernote_callback', kwargs={'post_id':post_id}))
		request_token = client.get_request_token(callbackUrl)

		# Save the request token information for later
		request.session['oauth_token'] = request_token['oauth_token']
		request.session['oauth_token_secret'] = request_token['oauth_token_secret']

		# 	# Redirect the user to the Evernote authorization URL
		return redirect(client.get_authorize_url(request_token))

def send_to_evernote(client, post_id):
	'''create specified notes inside evernote'''
	try:
		# noteStore = client.get_note_store()
		# notebooks = noteStore.listNotebooks()
		# for n in notebooks:
		# 	print (n.name, n.guid)

		post = Post.objects.get(pk=post_id)
		title = post.title
		author = post.author
		categories = [c.category for c in post.categories.all()]
		notes = post.notes

		if author:
			categories.append(author)

		notebook_guid = "95069c18-ac04-42e2-84cf-b6b9314e78b7"
		notebook_name = "My Notebook"
		
		noteStore = client.get_note_store()
		note = Types.Note()
		note.title = title
		note.content = '<?xml version="1.0" encoding="UTF-8"?><!DOCTYPE en-note SYSTEM "http://xml.evernote.com/pub/enml2.dtd">'
		note.content += f'<en-note>{notes}</en-note>'
		note.tagNames = categories
		note.notebookGuid = notebook_guid
		note = noteStore.createNote(note)

		print(f'Successfully created notes "{note.title}" in notebook: {notebook_name}, with GUID: {notebook_guid}' )
	except:
		print("Could not create note.")

def callback(request, post_id):
	try:
		client = get_evernote_client()
		access_token = client.get_access_token(
			request.session['oauth_token'],
			request.session['oauth_token_secret'],
			request.GET.get('oauth_verifier', '')
		)
		print(f'access token: {access_token}')
	except KeyError:
		messages.warning(request, 'Could not connect to Evernote.')
		return redirect('/')

	send_to_evernote(client, post_id)
	
	return render(request, 'oauth/callback.html', {'notebooks': notebooks})


def reset(request):
	return redirect('/')