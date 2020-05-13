$(function() {
	let title = "#id_title";
	let note_type = "#id_note_type";
	let category = "#id_category";
	let status = "#id_status";
	let author = "#id_author";
	let rating = "#id_rating";

	let prevNotes = CKEDITOR.instances.id_notes.getData();
	let currentNotes = CKEDITOR.instances.id_notes;

	let fields = [title, note_type, category, status, author, rating]
	const states = {}

	for (const field of fields) {
		cookie = getCookie(field);
		cookie ? states[field] = cookie : states[field] = $(field).val();
	}

	console.log(document.cookie);

	getCookie('CKEDITOR') ? states["CKEDITOR"] = getCookie('CKEDITOR') : states["CKEDITOR"] = prevNotes

	checkChange();

	//check if cookie exists and return it and set field value to the cookie if it does
	function getCookie(field) {
		cookies = document.cookie.split(";");
		for (let cookie of cookies) {
			cookie = cookie.trim();
			if (cookie.startsWith(field)) {
				cookieVal = decodeURIComponent(cookie.substring(field.length+1,cookie.length));
				field != "CKEDITOR" ? $(field).val(cookieVal) : currentNotes.setData(cookieVal);
				return cookieVal;
			}
		}
		return null;
	}

	function checkChange() {
		update = setInterval(() => {
			for (let state in states) {
				prevState = states[state];

				if (state != "CKEDITOR") {
					currentState = $(state).val();

					if(prevState != currentState) {
						states[state] = currentState;
						setCookie(state,currentState,7);
					}
				}
				else {
					if(prevState != currentNotes.getData()) {
						states[state] = currentNotes.getData();
						setCookie("CKEDITOR",currentNotes.getData(),7);
					}
				}
			}
		},2000);
		
	}

	function setCookie(name,value,days) {
		value = encodeURIComponent(value);
		let date = new Date();
		date.setTime(date.getTime()+(days*24*60*60*1000));
		let expires = "; expires="+date.toGMTString();

		document.cookie = `${name}=${value}${expires}`;
	}

	//delete cookies on form submission
	$("form").submit(function() {
		let cookies = document.cookie.split(";");
		for (let i = 0; i < cookies.length; i++) {
		  setCookie(cookies[i].split("=")[0],"",-1);
		}
	});		
})