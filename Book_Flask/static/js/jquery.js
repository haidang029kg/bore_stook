// ---------------------------------------------- on scroll
$(window).on('scroll', function () {
	if ($(window).scrollTop()) {
		$('#my-navbar').addClass('black');
	}
	else {
		$('#my-navbar').removeClass('black');
	}
	if ($('.search-modal').css('display') == 'flex') {
		$('.search-modal').stop().animate({ 'marginTop': ($(window).scrollTop()) + 'px', 'marginLeft': ($(window).scrollLeft()) + 'px' }, 500);
	}
});


// --------------------------------------------- advance search
function advance_search() {
	$('.search-modal')[0].style.display = 'flex';
	$('.search-modal').stop().css('marginTop', ($(window).scrollTop()) + 'px').css('marginLeft', ($(window).scrollLeft()) + 'px');
};

function close_search() {
	$('.search-modal')[0].style.display = 'none';
};

// --------------------------------------------- login box
function open_login() {
	$('.login-modal')[0].style.display = 'flex';
	$('.login-modal').stop().css('marginTop', ($(window).scrollTop()) + 'px').css('marginLeft', ($(window).scrollLeft()) + 'px');
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
$('.card-title').ready(function () {
	$('.card-title').each(function () {
		len = $(this).text().length;
		if (len > 50) {
			$(this).text($(this).text().substr(0, 50) + ' ...');
		}
	});
});


//--------------------------------------------- hover to show account
$(document).ready(function () {
	$('.dropdown').hover(function () {
		$('.dropdown-content').css('display', 'block');
	}, function () {
		$('.dropdown-content').css('display', 'none');
	});
});


//----------------------------------------------- modal extra book infor
$(document).ready(function () {
	/*for (var i = 0; i < 20; i++){
		$('.card').eq(i).on('click', {value : i}, function(){
			var mess = $(this).attr('data-id');
			console.log(mess);
		});
	}*/
	$('.card .card-img-top').on('click', function (e) {
		var clicked = $(this).parents('.card').attr('data-id');
		$.ajax({
			data: {
				id: clicked
			},
			type: 'POST',
			dataType: 'json',
			url: '/book_detail',
			success: function (result) {
				$('#ModalExtraInfo').modal('show');
				$('.modal-title').text(result.Title);
				$('.extra-img img').attr('src', result.ImgUrl);

				$('#tb-price').text(result.Price);
				$('#tb-quan').text(result.Quantity);
				$('#tb-rating').text(result.AvgRating);
				$('#tb-ISBN').text(result.ISBN);
				$('#tb-public').text(result.PublicationYear);
				$('#tb-genre a').text(result.GenreName);
				var temp_link = '/home/genre/' + String(result.GenreID)
				$('#tb-genre a').attr("href", temp_link)
				$.ajax({
					data: {
						list_id: result.AuthorsID
					},
					type: 'POST',
					dataType: 'json',
					url: '/list_authors',
					success: function (result_2) {
						$('#tb-author ul').remove()
						$('#tb-author').prepend('<ul></ul>');
						var count = Object.keys(result_2).length;
						$.each(result_2, function (key, value) {
							var temp_link = '/home/author/' + String(key)
							$('#tb-author ul').prepend('<li><a href = "' + temp_link + '">' + value + '</a></li>');
						});
					},
					error: function (result_2) {
						$('#ModalExtraInfo').modal('show');
						$('.modal-title').text('Unavailable');
					}
				});
			},
			error: function (result) {
				$('#ModalExtraInfo').modal('show');
				$('.modal-title').text('Unavailable');
			}
		});
	});
});

//------------------------------------------ auto-scroll
$(document).ready(function () {
	if ($('.div-reg-log')[0]) {
		$('html, body').animate({
			scrollTop: $('.div-reg-log').offset().top - 100
		}, 2000);
	}
});


// -------------------------------------------------------------- shopping cart


var cart = [];

var Item = function (bookid, count, price) {
	this.bookid = bookid;
	this.count = count;
	this.price = price;
	this.count_price = price * count;
};


function saveCart() {
	localStorage.setItem('shoppingcart', JSON.stringify(cart));
}


function loadCart() {
	jsondata = JSON.parse(localStorage.getItem('shoppingcart'));

	for ( var i in jsondata) {
		var item = new Item(jsondata[i].bookid, jsondata[i].count, jsondata[i].price);
		cart.push(item);
	}
}

$(document).ready(function () {
	if (cart.length === 0) {
		loadCart();
	}
});

function addItemToCart(bookid, count, price) {
	for (var i in cart) {
		if (cart[i].bookid === bookid) {
			cart[i].count += count;
			cart[i].count_price = price * cart[i].count;
			saveCart();
			return;
		}
	}
	var item = new Item(bookid, count, price);
	cart.push(item);
	saveCart();
};

function removeItemFromCart(bookid) {
	for (var i in cart) {
		if (cart[i].bookid === bookid) {
			cart[i].count--;
			if (cart[i].count === 0) {
				cart.splice(i, 1);
			}
			saveCart();
			break;
		}
	}
};


function removeItemFromCartAll(bookid) {
	for (var i in cart) {
		if (cart[i].bookid === bookid) {
			cart.splice(i, 1);
			saveCart();
			break;
		}
	}
};


function clearCart() {
	cart.splice(0, cart.length);
	saveCart();
};


function totalCart() {
	var totalCost = 0;
	for (var i in cart) {
		totalCost += cart[i].count_price;
	}
	return totalCost;
};



$(document).ready(function() {
	$('.adding-cart').on('click', function () {
		var bookid = $(this).parents('.card').attr('data-id');
		var count = 1;
		var price = $(this).closest('.card').find('.card-text').text();
		price = Number(price.substr(0, price.length - 2));

		addItemToCart(bookid, count, price);

		$(this).text('Added');
		$(this).addClass('btn-warning');

		console.log(cart);
	});
});