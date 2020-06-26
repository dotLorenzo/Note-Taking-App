from evernote.api.client import EvernoteClient
import evernote.edam.type.ttypes as Types

try:
	dev_token = "S=s1:U=95fbd:E=17a48581d36:C=172f0a6f0e0:P=1cd:A=en-devtoken:V=2:H=36e8dedf986a4a3896d0e184e6142fc8"
	client = EvernoteClient(token=dev_token)
	userStore = client.get_user_store()
	user = userStore.getUser()
	print(f"Connected Evernote user {user.username}")
except:
	print(f"Could not connect to Evernote")

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

# noteStore = client.get_note_store()
# notebook = Types.Notebook()
# notebook.name = "My Notebook"
# notebook = noteStore.createNotebook(notebook)

