let checkbox = $('#autosave_checked');
let autosave = checkbox.prop('checked');
checkbox.change(function() {
	if($(this).is(':checked')) {
		autosave = true;
	}
	else autosave = false;
})


function autosaveCheck() {
	return autosave;
}