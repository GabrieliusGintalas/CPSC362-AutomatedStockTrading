import React, { useState, useEffect } from 'react';
import './App.css';
import { Line } from 'react-chartjs-2';
import { Chart as ChartJS } from 'chart.js/auto';
import StockChart from './StockChart';

function App() {
  const today = new Date();
  const defaultMonth = String(today.getMonth() + 1).padStart(2, '0');
  const defaultDay = String(today.getDate()).padStart(2, '0');
  const defaultYear = today.getFullYear();

  const [selectedSymbol, setSelectedSymbol] = useState('FNGU');
  const [month, setMonth] = useState(defaultMonth);
  const [day, setDay] = useState(defaultDay);
  const [year, setYear] = useState(defaultYear);
  const [marketData, setMarketData] = useState([]); // State to store market data
  const [chartData, setChartData] = useState(null);

  // Helper function to ensure valid input and proper date format
  const handleInputChange = (e, setter, maxLength) => {
    const value = e.target.value;
    if (/^\d*$/.test(value) && value.length <= maxLength) {
      setter(value);
    }
  };

  const validateDate = () => {
    let m = parseInt(month, 10);
    let d = parseInt(day, 10);
    let y = parseInt(year, 10);

    if (isNaN(m) || m < 1) m = 1;
    if (m > 12) m = 12;

    if (isNaN(y) || y < 2024) y = 2024;
    if (y > defaultYear) y = defaultYear;

    const daysInMonth = new Date(y, m, 0).getDate();
    if (isNaN(d) || d < 1) d = 1;
    if (d > daysInMonth) d = daysInMonth;

    setMonth(String(m).padStart(2, '0'));
    setDay(String(d).padStart(2, '0'));
    setYear(String(y));
  };

  // Fetch market data from the backend when the symbol or date changes
  useEffect(() => {
    const fetchData = async () => {
      try {
        const endDate = `${year}-${month}-${day}`;
        const response = await fetch('http://localhost:5000/fetch_market_data', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            symbol: selectedSymbol,
            end_date: endDate,
          }),
        });

        const data = await response.json();
        if (response.ok) {
          console.log('Market Data:', data); // Print the data in the console
          setMarketData(data.data); // Store the data in the state
        } else {
          console.error('Error fetching market data:', data.error);
        }
      } catch (error) {
        console.error('Error fetching market data:', error);
      }
    };

    fetchData();
  }, [selectedSymbol, month, day, year]); // Trigger fetch when symbol or date changes

  return (
    <div>
      <h1 className="title">Automated Stock Trading</h1>
      <p className="default-text">Please select a symbol that you would like to analyze:</p>
      <div className="button-container">
        <button className="symbol-button" onClick={() => setSelectedSymbol('FNGU')}>
          FNGU
        </button>
        <button className="symbol-button" onClick={() => setSelectedSymbol('FNGD')}>
          FNGD
        </button>
      </div>

      <p className="default-text">
        Showing market data for symbol: {selectedSymbol} from 01/01/2021 to{' '}
        <input
          className="date-input-inline"
          type="text"
          value={month}
          onChange={(e) => handleInputChange(e, setMonth, 2)}
          onBlur={validateDate}
          maxLength="2"
        />
        /
        <input
          className="date-input-inline"
          type="text"
          value={day}
          onChange={(e) => handleInputChange(e, setDay, 2)}
          onBlur={validateDate}
          maxLength="2"
        />
        /
        <input
          className="date-input-inline year-input"
          type="text"
          value={year}
          onChange={(e) => handleInputChange(e, setYear, 4)}
          onBlur={validateDate}
          maxLength="4"
        />
      </p>

      <div>
    <h2>Market Data Chart</h2>
      <StockChart marketData={marketData} selectedSymbol={selectedSymbol} />
    </div>

    </div>
  );
}

export default App;








