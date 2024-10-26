import React, { useEffect, useState } from 'react';
import { Line } from 'react-chartjs-2';
import { Chart as ChartJS } from 'chart.js/auto';

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
            backgroundColor: 'rgb(75, 192, 192)',
            borderColor: 'rgba(75, 192, 192, 0.2)',
          },
        ],
      };

      setChartData(data);
    } else {
      setChartData(null);
    }
  }, [marketData, selectedSymbol]);

  return chartData ? (
    <Line data={chartData} />
  ) : (
    <p>No data available to display the chart.</p>
  );
}

export default StockChart;








