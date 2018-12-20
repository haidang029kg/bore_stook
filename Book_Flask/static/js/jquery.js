// -------------------------------------------------------- on scroll window
$(window).on('scroll', function onscroll() {
	// navigation bar
	if ($(window).scrollTop()) {
		$('#my-navbar').addClass('opa-lblue');

	} else {
		$('#my-navbar').removeClass('opa-lblue');

	}
	// modal search
	if ($('.search-modal').css('display') == 'flex') {
		$('.search-modal').stop().animate({
			'marginTop': ($(window).scrollTop()) + 'px',
			'marginLeft': ($(window).scrollLeft()) + 'px'
		}, 700);
	}
	// sticky cart
	$('#sticky-cart').stop().animate({
		'marginTop': ($(window).scrollTop()) + 'px',
		'marginLeft': ($(window).scrollLeft()) + 'px'
	}, 200);

	// bill information
	var $marginSecBackground = $(window).scrollTop() - $('#sec-background').height();
	if ($marginSecBackground > 0 && ($marginSecBackground < ($('.col-50').height() - $('.bill').height() - 100))) {
		$('.bill').stop().animate({
			'marginTop': ($(window).scrollTop() - $('#sec-background').height() + 75) + 'px'
		}, 500);

	} else if ($marginSecBackground < 0) {
		$('.bill').stop().animate({
			'marginTop': 0
		});
	} else {
		$('.bill').stop().animate({
			'marginTop': $maxMar
		});
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
$('.card-title').ready(function resitrct_title_length() {
	$('.card-title').each(function () {
		len = $(this).text().length;
		if (len > 40) {
			$(this).text($(this).text().substr(0, 40) + ' ...');
		}
	});
});

//----------------------------------------------- modal extra book infor
$(document).ready(function ajax_bookdetail() {
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

// ------------------------------------------------------ fade out alert

$(document).ready(function() {
	window.setTimeout("fadeAlert();", 2000); //call fade in 3 seconds
  }
 )

function fadeAlert() {
	$(".alert").fadeOut('slow');
 }
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

$(document).ready(function loadCart_auto() {
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

$(document).ready(function addingbookfromhome() {
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
		$(this).css('background-color', 'yellow');

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
		$(this).css('background-color', 'yellow');

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

	$('#num-items').fadeOut(300, function () {
		$(this).text('Number of items: ' + cart.length);
		$(this).fadeIn(300);
	});

	$('#total-price').fadeOut(300, function () {
		$(this).text('Total   $' + totalCart());
		$(this).fadeIn(300);
	});
};

$(document).ready(function () {
	displayCart();
});

$(document).ready(function clear_the_cart() {
	$('#clear-cart').on('click', function (e) {
		e.preventDefault();
		clearCart();
		displayCart();
	});
});

$(document).on('click', '.remove-item', function remove_item(e) {
	e.preventDefault();
	var bookid = $(this).closest('tr').attr('data-bookid');
	removeItemFromCartAll(bookid);
	displayCart();
});

$(document).on('change', '.input-count', function changes_on_count_number(e) {
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


	$('#total-price').fadeOut(1, function () {
		$(this).text('Total   $' + totalCart());
		$(this).fadeIn(300);
	});

});

function cart_blink() {
	$('#sticky-cart').effect('shake');
};

$(document).ready(function loading_checkout() {
	var output = '';
	for (var i in cart) {
		output += "<tr><td>" + String(cart[i].title) + "</td><td>" + cart[i].count + "</td><td>" + cart[i].count_price + "</td></tr>"
	}

	$('#tb-checkout').html(output);
	$('#total-checkout').text('$ ' + totalCart());
	$maxMar = $('.col-50').height() - $('.bill').height() - 35;
});


// payment method ready
$(document).ready(function payment_ready() {
	$('#payment').tabs().tabs('option', 'active', 0);
});

function bill_form_check() {
	var forms_check = $('.bill').find('#fname, #phone, #email, #adr, #city').serializeArray();
	var temp_check = true;
	$.each(forms_check, function (i, form) {
		if (!form.value) {
			alert(form.name + ' is required');
			temp_check = false;
			return false;
		}
	});

	if (temp_check) {
		return true;
	}
	return false;
};

function credit_card_check() {
	var forms_check = $('#nav-tab-credit-card').find('#credit-name, #credit-cardnumber, #credit-card-month, #credit-card-year, #credit-card-ccv').serializeArray();
	var temp_check = true;
	$.each(forms_check, function (i, form) {
		if (!form.value) {
			alert('Credit card info is required!');
			temp_check = false;
			return false;
		}
	});

	return temp_check;
};

var Order = function (address, phone, totalprice, ispaid, status, paymentmethod) {
	this.Address = address;
	this.Phone = phone;
	this.TotalPrice = totalprice;
	this.IsPaid = ispaid;
	this.Status = status;
	this.PaymentMethod = paymentmethod;
};

var Order_Details = function (bookid, count) {
	this.BookID = bookid;
	this.Quantity = count;
}


function create_order(payment_index) {
	// getting address
	var Address = $('.bill #adr').val();
	Address += (' ' + $('.bill #city').val());
	// getting total price
	var TotalPrice = totalCart();
	// geting isPaid
	var IsPaid = 1;
	// getting status
	var Status = 1;
	// getting payment method
	var PaymentMethod = Number(payment_index) + 1;
	// getting phone
	var Phone = $('.bill #phone').val()

	var order = new Order(Address, Phone, TotalPrice, IsPaid, Status, PaymentMethod);

	return order;
}

function create_order_detail() {
	var order_list = [];
	for (var i in cart) {
		var item = new Order_Details(cart[i].bookid, cart[i].count);
		order_list.push(item);
	}

	return order_list;
}

function ajax_sending_order(payment_index) {
	var temp_order = create_order(payment_index);

	var temp_order_detail = create_order_detail();

	temp_order_detail = JSON.stringify(temp_order_detail);

	temp_order['Detail'] = temp_order_detail;

	$.ajax({
		data: {
			order: JSON.stringify(temp_order)
		},
		type: 'POST',
		dataType: 'json',
		url: '/create_order',
		success: function (result) {
			clearCart();
			window.location.href = "/home";
		},
		error: function () {
			alert('error');
		}
	});
};

function payment_method_check() {
	var payment_index = $('#payment').tabs().tabs('option', 'active');

	switch (payment_index) {

		case 0:
			{
				if (credit_card_check()) {
					alert('This payment method is not available!');
				}
			}
			break;
		case 1:
			{
				ajax_sending_order(payment_index);
			}
			break;
		case 2:
			{
				ajax_sending_order(payment_index);
			}
			break;
		};
};

$(document).ready(function finish_checkout() {
	$('#finish-checkout').on('click',function (e) {
		e.preventDefault();

		if (bill_form_check()) {
			payment_method_check();
		}
	});
});

//Carousel
$(document).ready(function () {
	$('#new-carousel').slick({
		slidesToShow: 3,
		slidesToScroll: 2,
		prevArrow: '<button type="button" class="slick-prev" style="left: -15px;">Previous</button>',
		nextArrow: '<button type="button" class="slick-next" style="right: -15px;">Next</button>',
		autoplay: true,
		dots: true,
		autoplaySpeed: 3000,
	});
	$('#related-carousel').slick({
		slidesToShow: 3,
		slidesToScroll: 2,
		prevArrow: '<button type="button" class="slick-prev" style="left: -10px;">Previous</button>',
		nextArrow: '<button type="button" class="slick-next" style="right: 0px;">Next</button>',
		autoplay: true,
		autoplaySpeed: 3000,
	});
	$('#also-buy-carousel').slick({
		slidesToShow: 3,
		slidesToScroll: 2,
		prevArrow: '<button type="button" class="slick-prev" style="left: -10px;">Previous</button>',
		nextArrow: '<button type="button" class="slick-next" style="right: 0px;">Next</button>',
		autoplay: true,
		autoplaySpeed: 3000,
	});
});


// ----------------------------------------------- more ordered detail
$(document).ready(function more_ordered_detail () {
	$('.btn-more-ordered-detail').on('click', function (e) {
		e.preventDefault();

		click_id = $(this).parents('tr').attr('data-order-id');

		$.ajax({
			data : {
				ordered_id : click_id
			},
			type : 'GET',
			dataType : 'json',
			url : '/ordered_detail',
			success : function (result) {
				
				$('#modal-content-more-ordered-detail h4').text('Ordered ID: ' + String(result.ordered_id));
				$('#modal-content-more-ordered-detail #total-price').text('Total $' + String(result.total_price));
				$('#modal-content-more-ordered-detail #num-items').text('Number of items: ' + String(result.items.length));

				

				var items = result.items;
				html_output = '';
				for (var i = 0; i < items.length; i++) {
					var sub_total = (Number(items[i].Quantity) * Number(items[i].Price)).toFixed(2);
					html_output += "<tr><td><div class='row'><div class='col-sm-2 hidden-xs'><img src='" + items[i].ImgUrl + "' class='img-responsive'></div></div></td><td class='text-center'>" + items[i].Title + "</td><td class='text-center'>" + items[i].Price + "</td><td class='text-center'>" + items[i].Quantity + "</td><td class='text-center'>" + sub_total + "</td></tr>";
				};

				$('#tb-body-ordered-detail').html(html_output);
			},
			error : function () {
				alert('error!!!');
			}
		});
	});
});


//set background color
$(document).ready(function () {
	if(window.location.href.indexOf("home") == -1 && window.location.href.indexOf("ordered_history") == -1 && window.location.href.indexOf("chart") == -1) {
		$('.my-container').css('background', 'transparent');
	}
})

//Genre filter
function genreFilter() {
	var input = document.getElementById("filter");
	var filter = input.value.toLowerCase();
	var nodes = document.getElementsByClassName('genre');
  
	for (i = 0; i < nodes.length; i++) {
	  if (nodes[i].innerText.toLowerCase().includes(filter)) {
		nodes[i].style.display = "block";
	  } else {
		nodes[i].style.display = "none";
	  }
	};
  };


//chart draw
window.onload = function () {
	var top5booksChart = new CanvasJS.Chart("top5booksChart", {
		title:{
			text: "Top 5 books sold yesterday"              
		},
		data: [              
		{
			type: "doughnut",
			dataPoints: [
				{ label: "SpiderMan",  y: 10  },
				{ label: "IronMan", y: 15  },
				{ label: "SuperMan", y: 25  },
				{ label: "AquaMan",  y: 30  },
				{ label: "Thor",  y: 28  },
				{ label: "Others", y: 5}
			]
		}
		]
	});
	top5booksChart.render();

	var salesChart = new CanvasJS.Chart("salesChart", {
		title:{
			text: "Sales in 5 previous day"              
		},
		data: [              
		{
			type: "line",
			dataPoints: [
				{ label: "Jan 1",  y: 10  },
				{ label: "Jan 2", y: 15  },
				{ label: "Jan 3", y: 25  },
				{ label: "Jan 4",  y: 30  },
				{ label: "Jan 5",  y: 28  },
			]
		}
		]
	});
	salesChart.render();
}