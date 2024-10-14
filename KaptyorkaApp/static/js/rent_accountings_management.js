
function send_rent_time(requestType, accounting_id, data="") {
	$.ajax({
		url: "set_rent_time/",
		type: 'POST',
		data: {
			'requestType': requestType,
			'accounting_id': accounting_id,
			'data': data
		},
		//DO NOT EDIT!
		beforeSend: function (xhr, settings) {
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
			if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
				// Only send the token to relative URLs i.e. locally.
				xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
			}
		},
		//EDITABLE CODE
		success: function a(json) {
			// alert(json);
			// alert(json.exist);
			if (json.result === "success") {
				if (requestType == "setStart") {
					$("#acc_interval_"+accounting_id).after(`<p>Start date: ${json.time_of_start_rent}</p>`);
					$("#acc_control_"+accounting_id).empty();
					$("#acc_control_"+accounting_id).append(`<button class="btn btn-primary" type="button" onclick="send_rent_time('setEnd', '`+accounting_id+`')">End time</button>`);
				}
				else if (requestType == "setEnd") {
					$("#acc_interval_"+accounting_id).after(`<p>End date: ${json.time_of_end_rent}</p>`);
					$("#acc_control_"+accounting_id).empty();
				}
				// alert("Ну, чё. Намана");
			} else {
				alert("Изменения не сохранены");
			}
		}
	});
}
