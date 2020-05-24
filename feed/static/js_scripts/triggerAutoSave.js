let checkbox = $('#autosave_checked');
let autosave = checkbox.prop('checked');
checkbox.change(function() {
	if($(this).is(':checked')) {
		autosave = true;
		alert("checked");
	}
	else autosave = false;
})


function autosaveCheck() {
	return autosave;
}