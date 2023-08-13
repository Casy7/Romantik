
if (!window.mobileCheck()) {
	$('.mobile').hide();
	var divsToHide = document.getElementsByClassName("mobile"); 
    for(var i = 0; i < divsToHide.length; i++){
        divsToHide[i].style.display = "none"; // depending on what you're doing
    }
}