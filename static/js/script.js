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
	console.log(p);
	
	if (p == 2 || p == 3) {
		$(el).find('input').prop('disabled', true);
		console.log(1);
		console.log($(el).find('input').value);
	} else {
		$(el).find('input').prop('disabled', false);
		console.log(2);
		console.log($(el).find('input').value);
	}
	

    var normalTask = 1;
    var k = $(el).attr('id');

    if(k[0] == "t"){
        normalTask = 0;
        k = k.substring(6);
    } else{
        normalTask = 1;
        k = k.substring(2);
    }

    if(p == 3 && normalTask == 1){
        // Call flask function which will remove the task
        $.post("/movedtask3", {javascript_data: k});

    } else if(p == 2 && normalTask == 1){

        $.post("/movedtask2", {javascript_data: k});

    } else if(p == 1 && normalTask == 1){

        $.post("/movedtask1", {javascript_data: k});

    } else if(p == 3 && normalTask == 0){

        $.post("/movedtemptask3", {javascript_data: k});

    } else if(p == 2 && normalTask == 0){

        $.post("/movedtemptask2", {javascript_data: k});

    } else if(p == 1 && normalTask == 0){

        $.post("/movedtemptask1", {javascript_data: k});

    }

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

var containers = $('#asd').toArray();
            dragula(containers);

$( "div input " ).click(function() {
    $(this).focus();
});


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
	periods = "periods" + p;
	days_months = "days_months" + p;

	if(termsCheckBox.checked){
		document.getElementById(date1).disabled = false;
		document.getElementById(periods).disabled = false;
		document.getElementById(days_months).disabled = false;
	} else{           
		document.getElementById(date1).disabled = true;
		document.getElementById(periods).disabled = true;
		document.getElementById(days_months).disabled = true;     
	}
}

function checking_fields(formata) {
	data_id = "date_input" + formata;
	edit4e = "edit" + formata;
	period_id = "periods" + formata;
	shift_id = "shift" + formata;

    var date1 = document.forms[edit4e][data_id].value;
	var period = document.forms[edit4e][period_id].value;
	var shift = document.forms[edit4e][shift_id].value;
	//	window.document.write(date1);
	var name = document.forms[edit4e]["task_name_edit"].value;
	//var desc = document.forms[edit4e]["task_bio_edit"].value;

	var current = new Date();
	var wanted_date = new Date(date1);

	if (current > wanted_date) {
		alert("Тази дата е минала!");
		return false;
	}



	if (!document.getElementById(data_id).disabled) {
		if (date1 == null || date1 == "" || period == null || period == "" ) {
			alert("Моля попълнете всички данни!");
			return false;
		}
	}

	if (!document.getElementById(shift_id).disabled) {
		if (shift == null || shift == "") {
			alert("Моля попълнете смяна!");
			return false;
		}
	}

	if (name == null || name == "") {
		alert("Моля попълнете име!");
		return false;
	}


}

function megaqko(da) {
	
	name_id = "task_name";
	first_date_id = "date_input";
	periods_id = "per";

	var name2 = document.getElementById("task_name").value;
	var date2 = document.getElementById(first_date_id).value;
	var per2 = document.getElementById(periods_id).value;

	if (per2 == null || per2 == "" || date2 == null || date2 == "" || name2 == null || name2 == "") {
		alert("Моля попълнете всички данни!!");
		return false;
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

