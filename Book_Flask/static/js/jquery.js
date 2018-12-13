// ---------------------------------------------- on scroll
$(window).on('scroll', function onscroll() {
	if ($(window).scrollTop()) {
		$('#my-navbar').addClass('opa-lblue');
		$('.my-2.my-sm-0').addClass('txt-black');
		$('.dropdown-toggle').addClass('txt-black');
	}
	else {
		$('#my-navbar').removeClass('opa-lblue');
		$('.my-2.my-sm-0').removeClass('txt-black');
		$('.dropdown-toggle').removeClass('txt-black');

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

//----------------------------------------------- resitrct legth title
$('.card-title').ready(function resitrct_title_length () {
	$('.card-title').each(function () {
		len = $(this).text().length;
		if (len > 40) {
			$(this).text($(this).text().substr(0, 40) + ' ...');
		}
	});
});

//----------------------------------------------- modal extra book infor
$(document).ready(function ajax_bookdetail () {
	/*for (var i = 0; i < 20; i++){
		$('.card').eq(i).on('click', {value : i}, function(){
			var mess = $(this).attr('data-id');
			console.log(mess);
		});
	}*/
	$('.card .hvrbox-layer_top').on('click', function (e) {
		e.preventDefault();

		var clicked = $(this).parents('.card').attr('data-id');
		$.ajax({
			data: {
				id: clicked
			},
			type: 'POST',
			dataType: 'json',
			url: '/book_detail',
			success: function (result) {
				$('#tb-bookid').attr('data-bookid', clicked);
				$('#ModalExtraInfo').modal('show');
				$('.modal-title').text(result.Title);
				$('.extra-img img').attr('src', result.ImgUrl);

				$('#tb-price').text(result.Price);
				$('#tb-quan').text(result.Quantity);
				$('#tb-rating').text(result.AvgRating);
				$('#tb-ISBN').text(result.ISBN);
				$('#tb-public').text(result.PublicationYear);
				$('#tb-genre a').text(result.GenreName);
				var temp_link = '/home/genre/' + String(result.GenreID);
				$('#tb-genre a').attr("href", temp_link);
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
							var temp_id = Number(key);
							var temp_link = '/home/author/' + String(temp_id);
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
$(document).ready(function auto_scroll() {
	if ($('.div-reg-log')[0]) {
		$('html, body').animate({
			scrollTop: $('.div-reg-log').offset().top - 100
		}, 1500);
	}

	if ($('.contianer')[0]) {
		$('html, body').animate({
			scrollTop: $('.contianer').offset().top - 100
		}, 2000);
	}

	if ($('.cart-container')[0]) {
		$('html, body').animate({
			scrollTop: $('.cart-container').offset().top - 100
		}, 2000);
	}

	if ($('.checkout-container')[0]) {
		$('html, body').animate({
			scrollTop: $('.checkout-container').offset().top - 100
		}, 2000);
	}

});


// -------------------------------------------------------------- shopping cart
var cart = [];

var Item = function (bookid, title, count, price, image) {
	this.bookid = bookid;
	this.title = title;
	this.count = count;
	this.price = price;
	this.image = image;
	this.count_price = (price * count).toFixed(2);
};


function saveCart() {
	localStorage.setItem('shoppingcart', JSON.stringify(cart));
};


function loadCart() {
	jsondata = JSON.parse(localStorage.getItem('shoppingcart'));

	for (var i in jsondata) {
		var item = new Item(jsondata[i].bookid, jsondata[i].title, jsondata[i].count, jsondata[i].price, jsondata[i].image);
		cart.push(item);
	}
};

$(document).ready(function loadCart_auto () {
	cart.splice(0, cart.length);
	loadCart();
});

function addItemToCart(bookid, title, count, price, image) {
	for (var i in cart) {
		if (cart[i].bookid === bookid) {
			var temp = Number(cart[i].count) + Number(count);
			cart[i].count = temp;
			cart[i].count_price = price * cart[i].count;
			saveCart();
			return;
		}
	}
	var item = new Item(bookid, title, count, price, image);
	cart.push(item);
	saveCart();
};

function updateItemCount(bookid, new_count) {
	for (var i in cart) {
		if (cart[i].bookid === bookid) {
			cart[i].count = new_count;
			break;
		}
	}
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
		totalCost += Number(cart[i].count_price);
	}
	totalCost = Number(totalCost).toFixed(2);
	return totalCost;
};

$(document).ready(function addingbookfromhome () {
	$('.adding-cart').on('click', function (e) {
		e.preventDefault();

		var bookid = $(this).parents('.card').attr('data-id');
		var title = $(this).closest('.card').find('.card-title').text();
		var count = 1;
		var price = $(this).closest('.card').find('.card-text').text();
		var image = $(this).closest('.card').find('img').attr('src');

		price = Number(price.substr(0, price.length - 2));

		addItemToCart(bookid, title, count, price, image);

		$(this).text('Added');
		$(this).css('background-color','yellow');

		cart_blink();
	});
});

$(document).ready(function addboookfromajax() {
	$('.adding-cart-ajax').on('click', function (e) {
		e.preventDefault();

		var count = $(this).closest('.modal-footer').find('#slct').val();
		var bookid = $('#tb-bookid').attr('data-bookid');
		var price = Number($('#tb-price').text());
		var title = $('.modal-title').text();
		var image = $('#ModalExtraInfo img').attr('src');

		addItemToCart(bookid, title, count, price, image);

		$(this).text('Added');
		$(this).css('background-color','yellow');

		cart_blink();
	})
})


function displayCart() {
	var output = '';
	for (var i in cart) {
		var bookid = cart[i].bookid
		var title = cart[i].title;
		var count = cart[i].count;
		var image = cart[i].image;
		var price = cart[i].price;
		var count_price = cart[i].count_price;

		output += "<tr data-bookid=" + bookid + "><td data-th='Product'><div class='row'><div class='col-sm-2 hidden-xs'><img src='" + image + "' alt='...' class='img-responsive' /></div><div class='col-sm-10'><h4 class='nomargin'>" + title + "</h4></div></div></td><td class='price-for-an-item' data-th='Price'>" + price + "</td><td data-th='Quantity'><input type='number' min='1' class='form-control text-center input-count' value='" + count + "'></td><td data-th='Subtotal' class='text-center price-for-items'>" + count_price + "</td><td class='actions' data-th=''><button class='btn btn-danger btn-sm remove-item'><i class='fas fa-trash-alt'></i></button></td></tr>"
	}
	$('#cart-data').html(output);

	$('#num-items').fadeOut(300, function(){
		$(this).text('Number of items: ' + cart.length);
		$(this).fadeIn(300);
	});

	$('#total-price').fadeOut(300, function(){
		$(this).text('Total   $' + totalCart());
		$(this).fadeIn(300);
	});
};

$(document).ready(function () {
	displayCart();
});

$(document).ready(function clear_the_cart () {
	$('#clear-cart').on('click', function (e) {
		e.preventDefault();
		clearCart();
		displayCart();
	});
});

$(document).on('click', '.remove-item', function remove_item (e) {
	e.preventDefault();
	var bookid = $(this).closest('tr').attr('data-bookid');
	removeItemFromCartAll(bookid);
	displayCart();
});

$(document).on('change', '.input-count', function changes_on_count_number (e) {
	e.preventDefault();

	var bookid = $(this).closest('tr').attr('data-bookid');
	var count = $(this).val();
	updateItemCount(bookid, count);
	var price = Number($(this).closest('tr').find('.price-for-an-item').text());
	var count_price = Number(price * count).toFixed(2);
	
	cart.splice(0, cart.length);
	loadCart();

	$(this).closest('tr').find('.price-for-items').fadeOut(1, function () {
		$(this).text(count_price);
		$(this).fadeIn(300);
	});


	$('#total-price').fadeOut(1, function() {
		$(this).text('Total   $' + totalCart());
		$(this).fadeIn(300);
	});

});

function cart_blink () {
	$('#sticky-cart').effect('shake');
};