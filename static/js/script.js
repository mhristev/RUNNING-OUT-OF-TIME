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



// SELECT MAIL
function email(termsCheckBox){
	if(termsCheckBox.checked){
		document.getElementById("email_input").disabled = false;
	} else{           
		document.getElementById("email_input").disabled = true;    
	}
}

// MANAGE
function date(termsCheckBox){
	var p = $(termsCheckBox).attr('id');
	p = p.substring(8);
	//window.document.write(p);
	date1 = "date_input" + p;
	date2 = "date_input2" + p;

	if(termsCheckBox.checked){
		document.getElementById(date1).disabled = false;
		document.getElementById(date2).disabled = false;
	} else{           
		document.getElementById(date1).disabled = true;    
		document.getElementById(date2).disabled = true;  
	}
}

function validateFormEdit(formata) {
	
	first = "date_input" + formata;
	second = "date_input2" + formata;

	edit4e = "edit" + formata;

    var date1 = document.forms[edit4e][first].value;
    var date2 = document.forms[edit4e][second].value;

	

	if (!document.getElementById(first).disabled) {
		if (date1 == null || date1 == "", date2 == null || date2 == "") {
			alert("Please Fill All Required Field");
			return false;
		}
	}
  }

  // SHIFT
  function s(termsCheckBox) {
	var p = $(termsCheckBox).attr('id');
	p = p.substring(5);
	
	shft = "shift" + p;

	if(termsCheckBox.checked){
		document.getElementById(shft).disabled = false;
	} else{           
		document.getElementById(shft).disabled = true;  
	}
}