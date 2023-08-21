function default_comment_send() {
	send_comment("publish")
}

function send_comment(requestType, additionaldata = {}) {

	news_content = editor.getData();

	$.ajax({
		url: "/publish_comment/",
		type: 'POST',
		data: {
			'post_id': post_id,
			'content': news_content,
			'secondary_data': additionaldata
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

				post_path = "/post/"+post_id;
				location.reload()
				window.location.replace(post_path);
				window.location.href = post_path;
				window.location = post_path;
			} else {

			}
		}
	});
}
