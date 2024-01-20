function range(start, end, fill='num') {
    var ans = [];
    for (let i = start; i <= end; i++) {

        switch (fill){
            case 'num':
                ans.push(i)
                break;
            case 'NaN':
                ans.push(NaN)
                break;

        }


    }
    return ans;
}


day_of_year =range(1, 365, 'num')
console.log(day_of_year)
fill = range(1,100,'NaN')

data1 = [].concat( fill, [860,1140,1060,1060,1070,860,1140,1060,1060,1070,860,1140,1060,1060,1070,860,1140,1060,1060,1070,860,1140,1060,1060,1070,860,1140,1060,1060,1070])

const xValues = day_of_year;

new Chart("myChart", {
  type: "line",
  data: {
    labels: xValues,
    datasets: [{
          data: data1,
          borderColor: "red",
          fill: false
    },{
      data: [].concat(data1,[1110,1330,2210,7830,2478]),
      borderColor: "green",
      fill: false
    }]
  },
  options: {
    legend: {display: false}
  }
});