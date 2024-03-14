

function update_post(additionaldata = {}) {

	news_content = editor.getData();
	post_id = document.getElementById("post_id").value;

	$.ajax({
		url: "/update_post/",
		type: 'POST',
		data: {
			'post_id': post_id,
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
				new_location = "/post/" + post_id;
				window.location.replace(new_location);
				window.location.href = new_location;
				window.location = new_location;
			} else {
				alert("Изменения не сохранены");
				alert("Ошибка сегментации диска. Компьютер будет перезагружен.");
			}
		}
	});
}