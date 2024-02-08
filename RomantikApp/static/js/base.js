
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

if (!window.mobileCheck()) {
	$('.mobile').hide();
	var divsToHide = document.getElementsByClassName("mobile"); 
    for(var i = 0; i < divsToHide.length; i++){
        divsToHide[i].style.display = "none"; // depending on what you're doing
    }
}

function toggleDropdown(dropdownId) {
	if (!document.getElementById(dropdownId).classList.contains("dropdown-animate")) 
	{
		document.getElementById(dropdownId).classList.add("dropdown-animate"); 
		document.getElementById(dropdownId).classList.remove("dropdown-animate-close");		
	}
	else {
		document.getElementById(dropdownId).classList.remove("dropdown-animate");
		document.getElementById(dropdownId).classList.add("dropdown-animate-close");
	}
}