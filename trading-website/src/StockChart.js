import React, { useEffect, useState } from 'react';
import { Line } from 'react-chartjs-2';
import { Chart as ChartJS } from 'chart.js/auto';
import './Colors.css';
import 'chartjs-adapter-date-fns';

function getCSSVariable(name) {
  return getComputedStyle(document.documentElement).getPropertyValue(name).trim();
}

function StockChart({ marketData, selectedSymbol, tradeLog }) {
  const [chartData, setChartData] = useState(null);

  useEffect(() => {
    if (Array.isArray(marketData) && marketData.length > 0) {
      // Convert date strings to Date objects
      const dataPoints = marketData.map(entry => ({
        x: new Date(entry.Date),
        y: entry.Close,
      }));

      const buySignals = Array.isArray(tradeLog)
        ? tradeLog
            .filter(trade => trade.action === 'BUY')
            .map(trade => ({
              x: new Date(trade.date),
              y: trade.price,
            }))
        : [];

      const sellSignals = Array.isArray(tradeLog)
        ? tradeLog
            .filter(trade => trade.action === 'SELL')
            .map(trade => ({
              x: new Date(trade.date),
              y: trade.price,
            }))
        : [];

      console.log('Data Points:', dataPoints);
      console.log('Buy Signals:', buySignals);
      console.log('Sell Signals:', sellSignals);

      const data = {
        datasets: [
          {
            type: 'line',
            label: `Closing Price of ${selectedSymbol}`,
            data: dataPoints,
            fill: false,
            backgroundColor: 'rgb(125, 125, 125)',
            borderColor: 'rgba(0, 0, 0, 1)',
            pointRadius: 0,
            pointHoverRadius: 0,
            pointHitRadius: 0,
            order: 1,
          },
          {
            type: 'scatter',
            label: 'Buy Signals',
            data: buySignals,
            backgroundColor: getCSSVariable('--Red'),
            borderColor: 'black',
            borderWidth: 1,
            pointRadius: 7,
            pointHoverRadius: 9,
            pointHitRadius: 0,
            showLine: false,
            order: 2,
          },
          {
            type: 'scatter',
            label: 'Sell Signals',
            data: sellSignals,
            backgroundColor: getCSSVariable('--Green'),
            borderColor: 'black',
            borderWidth: 1,
            pointRadius: 7,
            pointHoverRadius: 9,
            pointHitRadius: 0,
            showLine: false,
            order: 2,
          },
        ],
      };

      const options = {
          plugins: {
            legend: {
              onClick: null,
            },
            tooltip: {
              filter: function (tooltipItem) {
                const datasetLabel = tooltipItem.dataset.label;
                // Suppress tooltips for Buy and Sell Signals
                if (datasetLabel === 'Buy Signals' || datasetLabel === 'Sell Signals') {
                  return false; // Do not display tooltip
                }
                return true; // Display tooltip
              },
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
              type: 'time',
              time: {
                unit: 'day',
                tooltipFormat: 'MM/dd/yyyy',
                displayFormats: {
                  day: 'MM/dd/yyyy',
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
                callback: function (value) {
                  return `$${value}`;
                },
              },
            },
          },
          maintainAspectRatio: false,
        };
      

      // Custom plugin to control drawing order
      const fixDrawingOrderPlugin = {
        id: 'fixDrawingOrder',
        beforeDatasetsDraw(chart) {
          const metasets = chart.getSortedVisibleDatasetMetas();

          // Separate metasets by element type
          const lines = [];
          const others = [];

          metasets.forEach(meta => {
            if (meta.type === 'line') {
              lines.push(meta);
            } else {
              others.push(meta);
            }
          });

          // Draw line datasets first
          lines.forEach(meta => {
            meta.controller.draw();
          });

          // Then draw other datasets (points)
          others.forEach(meta => {
            meta.controller.draw();
          });

          // Prevent default drawing
          return false;
        },
      };

      setChartData({ data, options, plugins: [fixDrawingOrderPlugin] });
    } else {
      setChartData(null);
    }
  }, [marketData, selectedSymbol, tradeLog]);

  const marketDataChartStyle = {
    display: 'flex',
    flexDirection: 'column',
    justifyContent: 'center',
    alignItems: 'center',
    margin: '0 auto',
  };

  const chartTitleStyle = {
    color: 'var(--Black)',
  };

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
        <Line
          data={chartData.data}
          options={chartData.options}
          plugins={chartData.plugins}
        />
      </div>
    </div>
  ) : (
    <p style={noDataTextStyle}>No data available to display the chart.</p>
  );
}

export default StockChart;
