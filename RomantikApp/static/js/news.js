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

let postsOffset = 5;
const csrftoken = getCookie('csrftoken');
let after_last_update_timer_finished = true;

async function after_last_update_delay(ms) {
	after_last_update_timer_finished = false;
	await new Promise(resolve => setTimeout(resolve, ms));
	after_last_update_timer_finished = true;
  }


$(document).ready(function () {

	function isScrolledToBottom() {
		return $(window).scrollTop() + $(window).height() >= $(document).height() - 400;
	}

	function loadMorePosts() {
		// Проверяем, долистал ли пользователь страницу до конца
		if (isScrolledToBottom() && after_last_update_timer_finished) {
			after_last_update_delay(5000);
			console.log("Loading more posts...");


			$.ajax({
				url: "/load_more_posts/",
				type: 'POST',
				data: {
					'posts_offset': postsOffset
				},
				beforeSend: function (xhr) {
					function getCookie(name) {
						let cookieValue = null;
						if (document.cookie && document.cookie !== '') {
							const cookies = document.cookie.split(';');
							for (let i = 0; i < cookies.length; i++) {
								const cookie = cookies[i].trim();
								// Does this cookie string begin with the name we want?
								if (cookie.substring(0, name.length + 1) === (name + '=')) {
									cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
									break;
								}
							}
						}
						return cookieValue;
					}
					csrftoken_val = collectCookies(xhr);
					csrftoken_val = getCookie('csrftoken');
					if (csrftoken_val == "") {
						csrftoken_val = document.getElementsByName('csrfmiddlewaretoken')[0].value;
					}
					xhr.setRequestHeader('X-CSRF-Token', csrftoken_val);
				},
				success: function a(json) {
					if (json.result === "success") {
						console.log(json);
						postsOffset += 10;
						json.posts.forEach(post => {
							addPostToPage(post);
						});
					} else {
					}
				}
			});

		}
	}

	$(window).scroll(function () {
		loadMorePosts();
	});
});

function addPostToPage(post) {
	
	user_upvoted_class = "";
	if (post.user_upvoted == "yes") {
		user_upvoted_class = "upvoted";
	}

	user_downvoted_class = "";
	if (post.user_downvoted == "yes") {
		user_downvoted_class = "downvoted";
	}


	raw_post = `
	<div class="news-post" id="post_` + post.id + `">


            <div class="inline-panel post-author">
                <div class="post-avatar-container">
                    
                    <img class="glyphicon big post-avatar" src="`+post.author_avatar+`">
                    
                </div>
                <div class="user-name-container">
                    <div>
                        <p>`+post.author_full_name+`</p>
                    </div>
                    <small><a href="/user/`+ post.author_username +`">
                            @`+ post.author_username +`</a>,
                        15:57:13,
                        12.03.2024 (`+ post.beauty_datetime +`)</small>
                </div>
            </div>

            <div class="news-content ck-content">
			`+ post.content +`
            </div>
            <div class="post-control-panel">
                <div class="vote-panel">

                    <a href="/post/` + post.id + `/edit" class="link-icon"><img class="icon negative" src="/static/icons/edit.svg" alt="edit"></a>
                    


                    <a href="/post/` + post.id + `" class="link-icon"><img class="icon negative" src="/static/icons/comment.svg" alt="down"><p class="comments-number">0</p></a>

                    

                    
                    <button class="btn btn-outline-secondary left-control ` + user_downvoted_class + `" type="button" id="downvote_post_` + post.id + `" onclick="vote_post('` + post.id + `', 'downvote')"><img class="mini-icon negative" src="/static/icons/down.svg" alt="down"></button>
                    

                    <div class="post-raiting-box">
                        <p class="post-raiting" id="post_raiting_` + post.id + `">` + post.total_raiting + `
                        </p>
                    </div>
                    
                    <button class="btn btn-outline-secondary right-control ` + user_upvoted_class + `" type="button" id="upvote_post_` + post.id + `" onclick="vote_post('` + post.id + `', 'upvote')"><img class="mini-icon negative" src="/static/icons/up.svg" alt="up"></button>
                    

                    


                </div>
            </div>
            <hr>
        </div>
	`
	$(".posts-list").append(raw_post);
}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
