$(function() {
	let postID = $("#post-id").attr("post-id");
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

	getCookie('CKEDITOR') ? states["CKEDITOR"] = getCookie('CKEDITOR') : states["CKEDITOR"] = prevNotes;

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

			// ($('#autosave_checked').length) ? console.log("exists") : console.log("does not exist");

			//if autosave selected on Create View and required fields filled out then redirect to the edit page after submit
			if ($('#autosave_checked').length) {
				if( $('#autosave_checked').is(':checked') ) {
					if($(title).val() && $(category).val() && $(note_type).val() && states["CKEDITOR"]) {
						console.log('atuosave checked and minimum fields filled out');
						$.ajax({
					        method: 'POST',
					        url: '/post/autocreate/',
					        data: {"autocreate":true},
					        success: function(data) {
					        	console.log('autosave session created');
					        },
					        error: function(data) {
					        	console.log('could not create autosave session');
					        }	
						});
						$('form').submit();
					}
				}
				else {
					$.ajax({
				        method: 'POST',
				        url: '/post/autocreate/',
				        data: {"autocreate":false},
				        success: function(data) {
				        	console.log('autosave session deleted');
				        },
				        error: function(data) {
				        	console.log('could not delete autosave session');
				        }	
					});
				}
			}

			for (let state in states) {
				prevState = states[state];

				if (state != "CKEDITOR") {
					currentState = $(state).val();

					if(prevState != currentState) {
						if(state!=category && state!=title) {
						
						states[state] = currentState;

						
						saveData({"field": state, "value":currentState, "id":postID})
						}
						//format title field...remove multi-white space
						//formatt category field ...remove multi-white space and special chars
						else {
							let formattedState;
							state == category ? formattedState = currentState.trim().replace(/\s\s+/g, ' ').replace(/[!&\/\\#+()£$~%.'":*?<>{}]/g,'') : formattedState = currentState.trim().replace(/\s\s+/g, ' ');
							states[state] = formattedState;
							saveData({"field": state, "value":formattedState, "id":postID});
						}
					}
				}
				else {
					if(prevState != currentNotes.getData()) {
						states[state] = currentNotes.getData();
						
						saveData({"field": "CKEDITOR", "value":currentNotes.getData(), "id":postID})
					}
				}
			}
		},3000);
		
	}

	function setCookie(name,value,days) {
		value = encodeURIComponent(value);
		let date = new Date();
		date.setTime(date.getTime()+(days*24*60*60*1000));
		let expires = "; expires="+date.toGMTString();

		document.cookie = `${name}=${value}${expires}`;

		console.log("setting cookie", name, value, days);
	}


	//if minimum number of fields are filled out then save the field on the db
	function saveData(fieldData) {
    	$.ajax({
	        method: 'POST',
	        url: '/post/autosave/',
	        data: fieldData,
	        success: function (data) {
	             console.log("successfully updated db");
	             if(!$('#autosave_message').length) {
		             let message_container = $("<div class='container-fluid w-75'>").append("<div class='alert alert-success text-center' id='autosave_message'>" + data + "</div></div>");
		             $("#div_id_status").after(message_container);
	        	}
	        	else {
	        		$('#autosave_message').text(data);
	        	}
	        },
	        error: function (data) {
	             setCookie(fieldData.field, fieldData.value, 7);
	        }
    	});
    	deleteCookies();
	}

	//delete cookies on form submission
	$("form").submit(function() {
		deleteCookies();
	});	
	
	function deleteCookies() {
		let cookies = document.cookie.split(";");
		for (let i = 0; i < cookies.length; i++) {
		  if (!cookies[i].trim().startsWith("csrftoken"))
		  setCookie(cookies[i].split("=")[0],"",-1); //delete - set expiry to -1 days
		}
	}
})