
function collectCookies(xhr) {

	function getCookie(name) {
		var cookieValue = null;
		if (document.cookie && document.cookie != '') {
			var cookies = document.cookie.split(';');
			for (var i = 0; i < cookies.length; i++) {
				var cookie = jQuery.trim(cookies[i]);
				// Does this cookie string begin with the name we want?
				if (cookie.substring(0, name.length + 1) == (name + '=')) {
					cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
					break;
				}
			}
		}
		return cookieValue;
	}
	xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
	
}


function toggleDropdown(dropdownId) {
	if (!document.getElementById(dropdownId).classList.contains("dropdown-animate")) 
	{
		document.getElementById(dropdownId).classList.add("dropdown-animate");
		document.getElementById(dropdownId).classList.remove("dropdown-animate-close");		

		$("#"+ dropdownId +" .dropdown-item").addClass("dropdown-item-animate");
		$("#"+ dropdownId +" .dropdown-item").removeClass("dropdown-item-animate-close");
	}
	else {
		document.getElementById(dropdownId).classList.remove("dropdown-animate");
		document.getElementById(dropdownId).classList.add("dropdown-animate-close");

		$("#"+ dropdownId +" .dropdown-item").addClass("dropdown-item-animate-close");
		$("#"+ dropdownId +" .dropdown-item").removeClass("dropdown-item-animate");
	}
}

function exists(querySelectorRule) {
	var element = document.querySelector(querySelectorRule);
	return element != null;
}

function byId(id) {
	return document.getElementById(id);
}

function getCookie(name) {
	var cookieValue = null;
	if (document.cookie && document.cookie != '') {
		var cookies = document.cookie.split(';');
		for (var i = 0; i < cookies.length; i++) {
			var cookie = jQuery.trim(cookies[i]);
			// Does this cookie string begin with the name we want?
			if (cookie.substring(0, name.length + 1) == (name + '=')) {
				cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
				break;
			}
		}
	}
	return cookieValue;
}


function attachCSRFToken(xhr) {
	xhr.setRequestHeader("X-CSRFToken", getCSRFToken());
}

function getCSRFToken() {
    return document.querySelector('input[name="csrfmiddlewaretoken"]').value;
}