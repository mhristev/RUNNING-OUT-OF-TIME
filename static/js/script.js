dragula([
	document.getElementById('1'),
	document.getElementById('2'),
	document.getElementById('3')
])

.on('drag', function(el) {
	
	// add 'is-moving' class to element being dragged
	//window.document.write($(el).parents('ul').first().attr('id'))
	el.classList.add('is-moving');
})
.on('dragend', function(el) {
	var p = $(el).parents('ul').first().attr('id');
    console.log(el)
	var k = $(el).attr('id');
	k = k.substring(2);
	var name = "#my-button" + k;

	if (p == 3) {
		//window.document.getElementById('my-button').show();
		//window.document.write(p);
		// vliza, no ne namira butona
		$(name).show();
		
		//window.WritableStream("asd");
		//window.document.getElementsByClassName("drag-inner-list")[p-1].getElementById('my-button').hidden();
		//window.document.getElementById('my-button').hidden();
		
	} else {
		$(name).hide();
	}
	
	//window.document.write("here1");
	//var p = window.document.getElementsByClassName("drag-inner-list")[1].id;
	//window.document.write(el.attr("id"));


	// after dragging has stopped
	el.classList.remove('is-moving');
	

	window.setTimeout(function() {
		el.classList.add('is-moved');
		window.setTimeout(function() {
			el.classList.remove('is-moved');
		}, 600);
	}, 100);

	//var p = window.document.getElementsByClassName("drag-inner-list").id;
	//window.document.write(p);
});


createOptions.create();
showOptions.init();


$(function () {
    $('[data-toggle="tooltip"]').tooltip();
});
