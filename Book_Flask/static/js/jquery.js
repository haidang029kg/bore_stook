// ---------------------------------------------- on scroll
$(window).on('scroll', function() {
	if($(window).scrollTop()) {
		$('#my-navbar').addClass('opa-lblue');
		$('.my-2.my-sm-0').addClass('txt-black');
		$('.nav-link').addClass('txt-black')
	}
	else {
		$('#my-navbar').removeClass('opa-lblue');
		$('.my-2.my-sm-0').removeClass('txt-black');
		$('.nav-link').removeClass('txt-black')
	}
	if($('.search-modal').css('display') == 'flex'){
		$('.search-modal').stop().animate({'marginTop': ($(window).scrollTop()) + 'px', 'marginLeft':($(window).scrollLeft()) + 'px'}, 500);
	}
});


// --------------------------------------------- advance search
function advance_search() {
	$('.search-modal')[0].style.display = 'flex';
	$('.search-modal').stop().css('marginTop', ($(window).scrollTop()) + 'px').css('marginLeft',($(window).scrollLeft()) + 'px');
};

function close_search() {
	$('.search-modal')[0].style.display = 'none';
};

// --------------------------------------------- login box
function open_login() {
	$('.login-modal')[0].style.display = 'flex';
	$('.login-modal').stop().css('marginTop', ($(window).scrollTop()) + 'px').css('marginLeft',($(window).scrollLeft()) + 'px');
};

function close_login() {
	$('.login-modal')[0].style.display = 'none';
};

// --------------------------------------------- message popup
function open_message() {	
	$('.message-modal')[0].style.display = 'flex';
};

function close_message() {
	$('.message-modal')[0].style.display = 'none';
};

//----------------------------------------------- resitrct legth title
$('.card-title').ready(function(){
	$('.card-title').each(function(){
		len = $(this).text().length;
		if (len>50){
			$(this).text($(this).text().substr(0, 50)+' ...');
		}
	});
});


//--------------------------------------------- hover to show account
$(document).ready(function(){
	$('.dropdown').hover(function(){
		$('.dropdown-content').css('display', 'block');
	}, function(){
		$('.dropdown-content').css('display', 'none');
	});
});


//----------------------------------------------- modal extra book infor
$(document).ready(function(){
	/*for (var i = 0; i < 20; i++){
		$('.card').eq(i).on('click', {value : i}, function(){
			var mess = $(this).attr('data-id');
			console.log(mess);
		});
	}*/
	$('.card').on('click', function(e){
		var clicked = $(this).attr('data-id');
		$.ajax({
			data : {
				id : clicked
			},
			type :'POST',
			dataType : 'json',
			url : '/book_detail',
			success : function(result){
				$('#ModalExtraInfo').modal('show');
				$('.modal-title').text(result.Title);
				$('.extra-img img').attr('src', result.ImgUrl);

				$('#tb-price').text(result.Price);
				$('#tb-quan').text(result.Quantity);
				$('#tb-rating').text(result.AvgRating);
				$('#tb-ISBN').text(result.ISBN);
				$('#tb-public').text(result.PublicationYear);
				$('#tb-genre a').text(result.GenreName);
				$('#tb-author').text(result.AuthorsID);
			},
			error : function(result){
				$('#ModalExtraInfo').modal('show');
				$('.modal-title').text('Unavailable');
			}
		});
	});
});

//------------------------------------------ auto-scroll
$(document).ready(function(){
	if ($('.div-reg-log')[0]){
		$('html, body').animate({
			scrollTop: $('.div-reg-log').offset().top - 100
			},2000);
	}
});

