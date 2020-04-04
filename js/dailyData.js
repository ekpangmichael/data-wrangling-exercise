



const parseDate = d3.timeParse("%Y-%m-%d");
d3.csv("./csvfiles/gas_daily_prices.csv")
      .row((d)=> {
        return {
          
          date: parseDate(d.date),
          price: Number(d.price)
         
        }
      })
      .get((error, data)=>{
        const height = 400;
        const width = 600
        const maxDate = d3.max(data, (d)=>{
          return d.date});
        const minDate = d3.min(data, (d)=>{
            return d.date});
        const maxPrice = d3.max(data,(d)=>{
          return d.price
        });

        const y = d3.scaleLinear()
                    .domain([0,maxPrice])
                    .range([height,0]);
        const x = d3.scaleTime()
                    .domain([minDate, maxDate])
                    .range([0,width]);
        const yAxis = d3.axisLeft(y);
        const xAxis = d3.axisBottom(x);

        const svg = d3.select("body").append("svg")
                      .attr("height", "100%")
                      .attr("width", "100%");
        
        const chartGroup = svg.append("g")
                          .attr("transform", "translate(50,50)");
        const line = d3.line()
                        .x(function(d){return x(d.date);})
                        .y(function(d){return y(d.price);});

          chartGroup.append("path").attr("d",line(data));
          chartGroup.append("g").attr("class", "x axis").attr("transform", "translate(0,"+height+")").call(xAxis);
          chartGroup.append("g").attr("class", "y axis").call(yAxis);
      });
