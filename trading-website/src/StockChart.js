import React, { useState, useEffect } from 'react';
import { Line } from 'react-chartjs-2';
import 'chart.js/auto';
import 'chartjs-adapter-date-fns'; // Adapter for handling dates

function StockChart({ selectedEndDate }) {
  const [chartData, setChartData] = useState({
    labels: [], // Dates
    datasets: [
      {
        label: 'Closing Costs ($)',
        data: [], // Closing prices
        borderColor: 'rgba(75,192,192,1)',
        backgroundColor: 'rgba(75,192,192,0.2)',
        borderWidth: 1,
        fill: true,
      },
    ],
  });

  useEffect(() => {
    fetch('/FNGU_data.json')  // Fetch the CSV-like data stored in JSON
      .then((response) => response.text()) // Parse the data as text
      .then((textData) => {
        const rows = textData.trim().split('\n');  // Split the text by newlines
  
        // Log the raw rows to verify the text split into rows correctly
        console.log('Raw rows:', rows);
  
        const filteredData = [];
        const startDate = '2024-01-01';  // Hardcoded start date
  
        // Loop through the rows (ignore the header row)
        rows.slice(1).forEach((row, index) => {
          console.log(`Row ${index + 1}:`, row);  // Log each row to ensure it contains data
  
          const columns = row.trim().split(/\s+/);  // Split by spaces (handles multiple spaces)
          
          // Log the columns to check if they are being split correctly
          console.log(`Columns for Row ${index + 1}:`, columns);
  
          // Extract the date (first column) and close price (5th column)
          const date = columns[0]; 
          const closePrice = parseFloat(columns[4]);  // Closing price is the 5th column
  
          if (date && closePrice && date !== 'Date') {
            const dateObj = new Date(date);  // Convert date to Date object
  
            // Filter out dates after the selected end date
            if (dateObj >= new Date(startDate) && dateObj <= new Date(selectedEndDate)) {
              filteredData.push({ date: dateObj, closePrice });
            }
          }
        });
  
        // After filtering, print the final array of filtered data
        console.log('Filtered data:', filteredData);
  
        // Prepare data for the chart
        const dates = filteredData.map((entry) => entry.date);  // Dates for the x-axis
        const closingPrices = filteredData.map((entry) => entry.closePrice);  // Closing prices for the y-axis
  
        // Update chart data
        setChartData({
          labels: dates,  // x-axis labels
          datasets: [
            {
              label: 'Closing Costs ($)',
              data: closingPrices,  // y-axis data
              borderColor: 'rgba(75,192,192,1)',
              backgroundColor: 'rgba(75,192,192,0.2)',
              borderWidth: 1,
              fill: true,
            },
          ],
        });
  
        // Print final chart data to confirm if it was set correctly
        console.log('Chart data:', { dates, closingPrices });
      })
      .catch((error) => {
        console.error('Error fetching data:', error);
      });
  }, [selectedEndDate]);
  
  
  

  const chartOptions = {
    scales: {
      x: {
        type: 'time',  // Use time scale for x-axis
        time: {
          unit: 'month',  // Show one tick per month
          tooltipFormat: 'MMM yyyy',  // Tooltip format for date
          displayFormats: {
            month: 'MMM yyyy',  // Format for the month labels
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
          text: 'Closing Cost ($)',
        },
        ticks: {
          callback: function (value) {
            return `$${value}`;  // Format y-axis as dollar amounts
          },
        },
      },
    },
  };

  return (
    <div className="chart-container">
      <h2>FNGU Stock Closing Prices</h2>
      <Line data={chartData} options={chartOptions} />
    </div>
  );
}

export default StockChart;





