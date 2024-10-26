import React, { useState } from 'react';
import './App.css';

function App() {
  // Get today's date
  const today = new Date();
  const defaultMonth = String(today.getMonth() + 1).padStart(2, '0'); // Ensure it's 2 digits
  const defaultDay = String(today.getDate()).padStart(2, '0'); // Ensure it's 2 digits
  const defaultYear = today.getFullYear();

  const minDate = new Date('2024-01-01'); // Minimum allowed date: January 1, 2024

  // State for the selected symbol
  const [selectedSymbol, setSelectedSymbol] = useState('FNGU');

  // State for date inputs
  const [month, setMonth] = useState(defaultMonth);
  const [day, setDay] = useState(defaultDay);
  const [year, setYear] = useState(defaultYear);

  // Helper function to ensure valid input and proper date format
  const handleInputChange = (e, setter, maxLength) => {
    const value = e.target.value;
    if (/^\d*$/.test(value) && value.length <= maxLength) {
      setter(value); // Don't pad with 0 yet, to avoid issues when typing
    }
  };

  // Corrects the date to fit within valid bounds (month: 1-12, day: depends on month/year, year: min 2024)
  const validateDate = () => {
    let m = parseInt(month, 10);
    let d = parseInt(day, 10);
    let y = parseInt(year, 10);

    // Correct invalid month
    if (isNaN(m) || m < 1) m = 1; // If the month is 00 or invalid, set it to 1
    if (m > 12) m = 12;

    // Correct invalid year
    if (isNaN(y) || y < 2024) y = 2024;
    if (y > defaultYear) y = defaultYear;

    // Adjust day based on the month and whether it's a leap year
    const daysInMonth = new Date(y, m, 0).getDate(); // Get number of days in the given month
    if (isNaN(d) || d < 1) d = 1; // If the day is 00 or invalid, set it to 1
    if (d > daysInMonth) d = daysInMonth;

    // Set corrected values (with padding for month and day)
    setMonth(String(m).padStart(2, '0'));
    setDay(String(d).padStart(2, '0'));
    setYear(String(y));
  };

  return (
    <div>
      <h1 className="title">Automated Stock Trading</h1>
      <p className="default-text">Please select a symbol that you would like to analyze:</p>
      <div className="button-container">
        <button 
          className="symbol-button" 
          onClick={() => setSelectedSymbol('FNGU')}
        >
          FNGU
        </button>
        <button 
          className="symbol-button" 
          onClick={() => setSelectedSymbol('FNGD')}
        >
          FNGD
        </button>
      </div>

      {/* Text and inline date input fields */}
      <p className="default-text">
        Showing market data for symbol: {selectedSymbol} from 01/01/2021 to {' '}
        <input 
          className="date-input-inline" 
          type="text" 
          value={month} 
          onChange={(e) => handleInputChange(e, setMonth, 2)} 
          onBlur={validateDate} // Validate when the input loses focus
          maxLength="2"
        />
        /
        <input 
          className="date-input-inline" 
          type="text" 
          value={day} 
          onChange={(e) => handleInputChange(e, setDay, 2)} 
          onBlur={validateDate} // Validate when the input loses focus
          maxLength="2"
        />
        /
        <input 
          className="date-input-inline year-input" 
          type="text" 
          value={year} 
          onChange={(e) => handleInputChange(e, setYear, 4)} 
          onBlur={validateDate} // Validate when the input loses focus
          maxLength="4"
        />
      </p>
    </div>
  );
}

export default App;







