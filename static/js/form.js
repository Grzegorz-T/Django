$(document).ready(function() {

	$(document).on('click','.btn-outline-success', function(event) {

		let stock_name = $(this).attr('stock_name');
		let row = $(this).attr('row_id');
		let quant = $('#Stock_Input'+row).val();
		req = $.ajax({
			data : {
				name: stock_name,
				quantity: quant,
				buy: true,
			},
			type : 'POST',
			url : '/_process/'
		})
		req.done(function(data) {
			if(quant>0){
				$('#quantity'+row).text('Owned: '+ data.quantity);
				$('#value'+row).text('Value: '+ data.value +'$');
				$('#profit'+row).text(data.profit +'%');
				$('#money').text(data.money +'$');
			}
		});

		event.preventDefault();

	});

	$(document).on('click','.btn-outline-danger', function(event) {

		let stock_name = $(this).attr('stock_name');
		let row = $(this).attr('row_id');
		let quant = $('#Stock_Input'+row).val();
		req = $.ajax({
			data : {
				name: stock_name,
				quantity: quant,
				buy: false,
			},
			type : 'POST',
			url : '/_process/'
		})
		req.done(function(data) {
			if(quant>0){
				$('#quantity'+row).text('Owned: '+ data.quantity);
				$('#value'+row).text('Value: '+ data.value +'$');
				$('#profit'+row).text(data.profit +'%');
				$('#money').text(data.money +'$').css("color","rgb(255, 193, 7)");
			}
		});

		event.preventDefault();

	});

});