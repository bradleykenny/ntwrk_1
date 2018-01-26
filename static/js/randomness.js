var images = [
					'clover.jpg',
					'geometry.jpg',
					'heavenroad.jpg',
					'roadtoLV.jpg',
					'sand.jpg',
					'waterlily.jpg',
					'atlantisneb.jpg',
					'babyelephants.jpg',
					'moonearthorbit.jpg',
					'mountainsview.jpg',
					'redtheatre.jpg',
					'sandydesert.jpg',
					'seatwilight.jpg',
					'spiralgalaxy.jpg',
					'tuscany.jpg',
					];

var primaryColor = [
					'#237b31', // clover.jpg
					'#3199d8', // geometry.jpg
					'#4b5208', // heavenroad.jpg
					'#7b563f', // roadtoLV.jpg
					'#bd8d5c', // sand.jpg
					'#0f3f3d', // waterlily.jpg
					'#07101d', // atlantisneb.jpg
					'#74712b', // babyelephants.jpg
					'#1e3a60', // moonearthorbit.jpg
					'#141d24', // mountainsview.jpg
					'#d93617', // redtheatre.jpg
					'#d5a867', // sandydesert.jpg
					'#537c9f', // seatwilight.jpg
					'#162051', // spiralgalaxy.jpg
					'#2e2212', // tuscany.jpg
					];

var secondColor = [
					'#156530', // clover.jpg
					'#2e80b2', // geometry.jpg
					'#363e14', // heavenroad.jpg
					'#5f422e', // roadtoLV.jpg
					'#9c764b', // sand.jpg
					'#002b29', // waterlily.jpg
					'#010006', // atlantisneb.jpg
					'#5b5b21', // babyelephants.jpg
					'#132a4b', // moonearthorbit.jpg
					'#000008', // mountainsview.jpg
					'#b52d1d', // redtheatre.jpg
					'#ae8b54', // sandydesert.jpg
					'#446886', // seatwilight.jpg
					'#0f103c', // spiralgalaxy.jpg
					'#060000', // tuscany.jpg
					];

var rndmNum = Math.floor(Math.random() * images.length);

$('html').css({'background': 'url(../static/img/' + images[rndmNum] + ')' + ' no-repeat center center fixed'});
$('html').css({'background-size':'cover'});
$('html').css({'-moz-background-size':'cover'});
$('html').css({'-webkit-background-size':'cover'});
$('html').css({'-o-background-size':'cover'});

function init() {
	$('.logo').css('color', primaryColor[rndmNum]);
	$('button').css('background-color', primaryColor[rndmNum]);

	$('.logo').hover(function(){$('.logo').css('color', secondColor[rndmNum])}, function(){$('.logo').css('color', primaryColor[rndmNum])});
	$('button').hover(function(){$('button').css('background-color', secondColor[rndmNum])}, function(){$('button').css('background-color', primaryColor[rndmNum])});

	/*  === TEST BLOCK ===
		> THE BLOCK BELOW IS USED TO TEST COLOURS WHEN ADDING NEW ONES
		> CHANGE THE NUMBER IN THE [] TO TEST A SPECIFC COMBO
		> USEFUL WHEN ADDING NEW PHOTOS AND COLOURS AND WANTING TO SEE HOW THEY'LL LOOK
		> REMEMBER TO COMMENT OUT ABOVE BLOCK OR PROBABLY WONT WORK
		> ALSO CHANGE THE PICTURE IN 'IMAGES[RNDMNUM]' ABOVE IN HTML.CSS CODE

	$('.logo').css('color', primaryColor[1]);
	$('button').css('background-color', primaryColor[1]);

	$('.logo').hover(function(){$('.logo').css('color', secondColor[1])}, function(){$('.logo').css('color', primaryColor[1])});
	$('button').hover(function(){$('button').css('background-color', secondColor[1])}, function(){$('button').css('background-color', primaryColor[1])});
	*/

	// $('#bottombar').css('background-color', primaryColor[rndmNum]);
}

document.addEventListener("DOMContentLoaded", init, false);
