
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