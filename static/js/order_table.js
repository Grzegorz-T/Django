$(document).ready(function() {

	$(document).on('click','.btn-outline-secondary', function(event) {
        let n = $(this).attr('name');

		req = $.ajax({
            data : {
                name: n,
            },
			type : 'POST',
			url : '/_order_table/'
        })
        req.done(function(data) {
                $.each(data.stocks,function(i,stock){
                $('#name'+(i+1)).text(stock.name);
                if(stock.change>0){
                    $('#price'+(i+1)).text(stock.price).css("color","rgb(0, 200, 0)");
                    $('#change'+(i+1)).text(stock.change).css("color","rgb(0, 200, 0)");
                    $('#perc'+(i+1)).text(stock.perc+'%').css("color","rgb(0, 200, 0)");
                }
                else if(stock.change==0){
                    $('#price'+(i+1)).text(stock.price).css("color","rgb(0, 0, 0)");
                    $('#change'+(i+1)).text(stock.change).css("color","rgb(0, 0, 0)");
                    $('#perc'+(i+1)).text(stock.perc+'%').css("color","rgb(0, 0, 0)");
                }
                else{
                    $('#price'+(i+1)).text(stock.price).css("color","rgb(225, 0, 0)");
                    $('#change'+(i+1)).text(stock.change).css("color","rgb(225, 0, 0)");
                    $('#perc'+(i+1)).text(stock.perc+'%').css("color","rgb(225, 0, 0)");
                }
                $('#opening'+(i+1)).text(stock.opening);
                $('#stock_max'+(i+1)).text(stock.stock_max);
                $('#stock_min'+(i+1)).text(stock.stock_min);
                $('#buy_button'+(i+1)).attr('stock_name', stock.name);
                $('#sell_button'+(i+1)).attr('stock_name', stock.name);
                if(data.bought_stocks[stock.name]){
                    $('#quantity'+(i+1)).text('Owned: '+data.bought_stocks[stock.name]['quantity']);
                    $('#value'+(i+1)).text('Value: '+data.bought_stocks[stock.name]['value']+'$');
                    
                    if(data.bought_stocks[stock.name]['profit']>0){
                        $('#profit'+(i+1)).text(data.bought_stocks[stock.name]['profit']+'%').css("color","rgb(0, 200, 0)");
                    }
                    else if(data.bought_stocks[stock.name]['profit']==0){
                        $('#profit'+(i+1)).text(data.bought_stocks[stock.name]['profit']+'%').css("color","rgb(0, 0, 0)");
                    }
                    else{
                        $('#profit'+(i+1)).text(data.bought_stocks[stock.name]['profit']+'%').css("color","rgb(225, 0, 0)");
                    }
                }
                else{
                    $('#quantity'+(i+1)).text('Owned: 0');
                    $('#value'+(i+1)).text('Value: 0$');
                    $('#profit'+(i+1)).text('0%').css("color","rgb(0, 0, 0)");
                }
            });
        });
        event.preventDefault();
    });

});