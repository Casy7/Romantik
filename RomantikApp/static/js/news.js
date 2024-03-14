function default_news_sent() {
	publish_post("publish");
}

function publish_post(requestType, additionaldata = {}) {

	news_content = editor.getData();

	$.ajax({
		url: "/publish_post/",
		type: 'POST',
		data: {
			'requestType': requestType,
			'news_content': news_content,
			'secondary_data': additionaldata
		},
		//DO NOT EDIT!
		beforeSend: function (xhr, settings) {
			collectCookies(xhr);
		},
		//EDITABLE CODE
		success: function a(json) {
			// alert(json);
			// alert(json.exist);
			if (json.result === "success") {
				location.reload()
				window.location.replace('/news/');
				window.location.href = "/news/";
				window.location = "/news/";
				// alert("Ну, чё. Намана");
			} else {
				alert("Изменения не сохранены");
				alert("Ошибка сегментации диска. Компьютер будет перезагружен.");
			}
		}
	});
}

function show_editor() {
	if ($('#editor-hidden-box').is(":visible")) {
		$('#editor-hidden-box').collapse('hide');
	}
	else {
		$('#editor-hidden-box').collapse('show');
	}

}

function vote_post(post_id, vote_type, additionaldata = {}) {

	$.ajax({
		url: "/vote_post/",
		type: 'POST',
		data: {
			'post_id': post_id,
			vote_type: vote_type,
			'secondary_data': additionaldata
		},
		//DO NOT EDIT!
		beforeSend: function (xhr, settings) {
			collectCookies(xhr);
		},

		//EDITABLE CODE
		success: function a(json) {
			// alert(json);
			// alert(json.exist);
			if (json.result === "success") {

				$("#post_raiting_" + post_id).text(json.total_raiting);

				if (json.vote_cancelled == "true") {
					$("#downvote_post_" + post_id).removeClass('downvoted');
					$("#upvote_post_" + post_id).removeClass('upvoted');
				}

				else {

					if (vote_type === "upvote") {
						$("#downvote_post_" + post_id).removeClass('downvoted');
						$("#upvote_post_" + post_id).addClass('upvoted');
					} else if (vote_type === "downvote") {
						$("#upvote_post_" + post_id).removeClass('upvoted');
						$("#downvote_post_" + post_id).addClass('downvoted');
					}
				}

			} else {
				alert("Не вийшло проголосувати. Перевірте Інтернет-з'єднання");
			}
		}
	});
}