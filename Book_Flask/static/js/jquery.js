// ---------------------------------------------- navigation bar
$(window).on('scroll', function() {
	if($(window).scrollTop()) {
		$('#my-navbar').addClass('black');
	}
	else {
		$('#my-navbar').removeClass('black');
	}
})


// --------------------------------------------- scroll to container
$('.btn-scrollauto').on('click', function(){
	scrollTo(500);
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

//----------------------------------------------- resitrct legth title
$('.card-title').ready(function(){
	$('.card-title').each(function(){
		len = $(this).text().length;
		if (len>50){
			$(this).text($(this).text().substr(0, 50)+' ...');
		}
	})
})