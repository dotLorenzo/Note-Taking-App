var note_type = "#div_id_note_type";
var author = "#div_id_author";
var rating = "#div_id_rating";

show_input_field([author,rating], false);

$(note_type).change(function(){
// Get the value of the option
	var value = $(note_type +" option:selected").val();

	// Check the value
	if (value === "book") {
		show_input_field([author,rating], true);
		}
	else if(value == "doc") {
	    $(rating).show();
	    $(author).hide();
		}
	else {
		show_input_field([author,rating], false);
	}
});

function show_input_field(ids, show) {
	ids.forEach(id => show ? $(id).show() : $(id).hide());
}
