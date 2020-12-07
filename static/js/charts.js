$(document).ready(function() {
    var labels = []
    var values = []
    var profits = []
    var stocks = []
    $.ajax({
        type : 'GET',
        url : '/_upd_charts/',
        success: function(data){
            labels = data.labels
            values = data.values
            profits = data.profits 
            stocks = data.stocks
            setChart()
        }
    })
    function getRandomColor(darker=0) {
        colors=[];
        for(let i=0;i<labels.length;i++){
            //1,5,3,6,2,4
            if(i%6==0){
                this.colors.push('rgba('+ (255-darker) + ',' + (100-darker) + ',' + Math.floor(Math.random()*(155-darker)+100).toString()+',0.35)');
            }
            else{
                if(i%6==1){
                    this.colors.push('rgba('+Math.floor(Math.random()*(155-darker)+120).toString() + ',' +  (255-darker) + ',' + (100-darker) + ',0.35)');
                }
                else{
                    if(i%6==2){
                        this.colors.push('rgba(' + (100-darker) + ',' +Math.floor(Math.random()*(155-darker)+120).toString() + ',' +  (255-darker) + ',0.35)');
                    }
                    else{
                        if(i%6==3){
                            this.colors.push('rgba('+ (255-darker) + ',' +Math.floor(Math.random()*(155-darker)+100).toString() + ',' + (100-darker) + ',0.35)');
                        }
                        else{
                            if(i%6==4){
                                this.colors.push('rgba(' +Math.floor(Math.random()*(155-darker)+120).toString() + ',' +  (100-darker) + ',' + (255-darker) + ',0.35)');
                            }
                            else{
                                this.colors.push('rgba(' + (100-darker) + ',' + (255-darker) + ',' + Math.floor(Math.random()*(155-darker)+100).toString() + ',0.35)');
                                }
                            }
                        }
                    }
                }
            }
        return colors;
    }

    function order_labels_profits(stocks) {

        var items = Object.keys(stocks).map(function(key) {
            return [key, stocks[key]];
          });

        items.sort(function(a, b) {

            return a[1]['profit'] - b[1]['profit'];
        });

        names = []
        for(var key in items) {
            names.push(items[key][0])
        }
        console.log(names)

    return names;
    }

    function order_profits(stocks) {

        var items = Object.keys(stocks).map(function(key) {
            return [key, stocks[key]];
          });

        items.sort(function(a, b) {

            return a[1]['profit'] - b[1]['profit'];
        });

        values = []
        for(var key in items) {
            values.push(items[key][1]['profit'])
        }
        console.log(values)

    return values;
    }

    function setChart(){
    var ctx = document.getElementById('myChart');
    var ctx2 = document.getElementById('myChart2');
    var backgroundColors = getRandomColor(0)
    var borderColor = getRandomColor(100)
    var myChart = new Chart(ctx, {
        type: 'pie',
        data: {
            labels: labels,
            datasets: [{
                label: '# of Votes',
                data: values,
                rotation: 90,
                backgroundColor: backgroundColors,
                borderColor: borderColor,
                borderWidth: 2,
            }]
        },
        options: {
            title:{
                display: true,
                text: 'Managed money',
                fontSize: 20,
                padding: 20,
            }
        }
    });
    var myChart = new Chart(ctx2, {
        type: 'bar',
        data: {
            labels: order_labels_profits(stocks),
            datasets: [{
                label: '# of Votes',
                data: order_profits(stocks),
                backgroundColor: backgroundColors,
                borderColor: borderColor,
                borderWidth: 3
            }]
        },
        options: {
            scales: {
                yAxes: [{
                    ticks: {
                        beginAtZero: true
                    }
                }]
            },
            title:{
                display: true,
                text: 'Gains/Losses of each bought stock in %',
                padding: 20,
                fontSize: 20,
            },
            legend: {
                display: false,
            }
        }
    });
    };
})


/*backgroundColor: [
    'rgba(255, 99, 132, 0.2)',
    'rgba(54, 162, 235, 0.2)',
    'rgba(255, 206, 86, 0.2)',
    'rgba(75, 192, 192, 0.2)',
    'rgba(153, 102, 255, 0.2)',
    'rgba(255, 159, 64, 0.2)'
],
borderColor: [
    'rgba(255, 99, 132, 1)',
    'rgba(54, 162, 235, 1)',
    'rgba(255, 206, 86, 1)',
    'rgba(75, 192, 192, 1)',
    'rgba(153, 102, 255, 1)',
    'rgba(255, 159, 64, 1)'
],*/