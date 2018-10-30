// ---------------------------------------------- navigation bar
$(window).on('scroll', function() {
	if($(window).scrollTop()) {
		$('#my-navbar').addClass('black');
	}
	else {
		$('#my-navbar').removeClass('black')
	}
})


// --------------------------------------------- advance search
function advance_search() {	
	$('.search-modal')[0].style.display = 'flex';
}

function close_search() {
	$('.search-modal')[0].style.display = 'none';
}


// --------------------------------------------- message popup
function open_message() {	
	$('.message-modal')[0].style.display = 'flex';
}

function close_message() {
	$('.message-modal')[0].style.display = 'none';
}