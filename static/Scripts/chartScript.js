// Function to create Chartist Bar Chart
function CreateBarChart(target, series, backgroundColor) {
    return new Chartist.BarChart(target, {
      series: series,
      backgroundColor: backgroundColor,
    }, {
      horizontalBars: true,
      stackBars: true,
      axisX: {
        showLabel: false,
        showGrid: false
      },
      axisY: {
        showLabel: false,
        showGrid: false
      },
      lineSmooth: Chartist.Interpolation.none(),
    });
  }
  
  // Function to customize bar drawing logic
  function CustomizeBarDrawing(data, series, colors) {
    if (data.type === 'bar' && data.seriesIndex !== undefined) {
        var seriesIndex = data.seriesIndex;
    
        // Remove the default line element and add a custom rectangle element
        data.element._node.parentNode.removeChild(data.element._node);
        var rect = document.createElementNS('http://www.w3.org/2000/svg', 'rect');
        rect.setAttribute('x', data.x1);
        rect.setAttribute('y', data.y1);
        rect.setAttribute('width', data.x2 - data.x1);
        rect.setAttribute('height', 40);
    
        // Set the fill color for the rectangle based on the subnet color
        if (seriesIndex !== series.length - 1) {
        rect.setAttribute('style', 'fill: ' + colors[seriesIndex].toString() + '; stroke: none;');
        }
        // Apply diagonal stripes to the last bar in the series
        else if (seriesIndex === series.length - 1) {
            rect.setAttribute('style', 'fill: url(#diagonal-stripes); stroke: none;');
        }
    
        // Append the custom rectangle to the SVG group
        data.group._node.appendChild(rect);
    }
  }