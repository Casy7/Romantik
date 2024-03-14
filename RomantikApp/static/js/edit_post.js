

function update_post(additionaldata = {}) {

	news_content = editor.getData();

	$.ajax({
		url: "/update_post/",
		type: 'POST',
		data: {
			'post_id': document.getElementById("post_id").value,
			'post_content': news_content,
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