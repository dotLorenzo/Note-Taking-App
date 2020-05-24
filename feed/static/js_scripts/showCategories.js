$(function() {

	let id_categories = $("#id_category");

	//this is the first time we are adding a button, so add button container 
	id_categories.after("<p id='category_buttons'></p>");

	showCategories();

	id_categories.on("input", function() {

		showCategories();

	});

	function showCategories() {

		let categories = id_categories.val().split(",");
		let formatted_categories = [];

		for (let category of categories) {
			//trim and replace multi-splaces, tabs and new-lines with single space, remove special characters
			category = category.trim().replace(/\s\s+/g, ' ').replace(/[!&\/\\#,+()£$~%.'":*?<>{}]/g,'');
			formatted_categories.push(category);

			//change spaces to underscores for button ids (.replace wont work?)
			category_id = category.split(/\s/).join("_");
			let id = `category_button_${category_id}`;
			// console.log(category, category_id, typeof category);

			button = $("<a class='btn btn-primary btn-sm ml-2' style='text-transform:capitalize;' href='#'></a>").text(category).attr("id", id);
			
			//if we havnt already created the button
			if (!$(`#${id}`).length) {
				$('#category_buttons').append(button);
			}
		}

		//delete buttons that are no longer relevant (deleted categories)
		$('#category_buttons').children('a').each(function() {
			if(!formatted_categories.includes($(this).text())) {
				$(this).remove();
			}
		})
	}


});