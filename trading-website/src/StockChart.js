import React, { useEffect, useState } from 'react';
import { Line } from 'react-chartjs-2';
import { Chart as ChartJS } from 'chart.js/auto';
import './Colors.css';
import 'chartjs-adapter-date-fns';


function StockChart({ marketData, selectedSymbol }) {
  const [chartData, setChartData] = useState(null);

  useEffect(() => {
    if (Array.isArray(marketData) && marketData.length > 0) {
      const labels = marketData.map(entry => entry.Date);
      const dataValues = marketData.map(entry => entry.Close);

      const data = {
        labels: labels,
        datasets: [
          {
            label: `Closing Price of ${selectedSymbol}`,
            data: dataValues,
            fill: false,
            backgroundColor: 'rgb(125, 125, 125)',
            borderColor: 'rgba(0, 0, 0, 1)',
            pointRadius: 0, // No points on the line
            pointHoverRadius: 0,
          },
        ],
      };

      const options = {
        plugins: {
          legend: {
            onClick: null,
          },
        },
        interaction: {
          mode: 'index',
          intersect: false,
        },
        hover: {
          mode: null,
        },
        scales: {
          x: {
            type: 'time', // Set the x-axis to display time-based data
            time: {
              unit: 'month', // Set the tick marks to increment by month
              tooltipFormat: 'MM/yyyy', // Tooltip format for hovering
              displayFormats: {
                month: 'MM/yyyy', // Format the tick labels to show MM/YYYY
              },
            },
            title: {
              display: true,
              text: 'Date',
            },
          },
          y: {
            title: {
              display: true,
              text: 'Closing Price ($)',
            },
            ticks: {
              callback: function(value) {
                return `$${value}`; // Add a $ symbol before the y-axis values
              },
            },
          },
        },
        maintainAspectRatio: false, // Ensures resizing works properly
      };

      setChartData({ data, options });
    } else {
      setChartData(null);
    }
  }, [marketData, selectedSymbol]);

  const marketDataChartStyle = {
    display: 'flex',           
    flexDirection: 'column',    
    justifyContent: 'center',    
    alignItems: 'center',   
    margin: '0 auto',                                     
  };

  const chartTitleStyle = {
    color: 'var(--LightBlue)',
  }
  
  const chartContainerStyle = {
    textAlign: 'center',
    padding: '10px',
    backgroundColor: '#f5f5f5',
    borderRadius: '10px',
    width: '50%',               
    height: '365px',  
    justifyContent: 'center',    
    alignItems: 'center',    
  };
  
  const noDataTextStyle = {
    color: 'red',
    fontWeight: 'bold',
  };
  
  return chartData ? (
    <div style={marketDataChartStyle}>
      <h2 style={chartTitleStyle}>Market Data Chart</h2>
      <div style={chartContainerStyle}>
        <Line data={chartData.data} options={chartData.options} />
      </div>
    </div>
  ) : (
    <p style={noDataTextStyle}>No data available to display the chart.</p>
  );
   
}

export default StockChart;








