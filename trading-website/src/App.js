import React, { useState, useEffect } from 'react';
import './App.css';
import StockChart from './StockChart';
import TradeLogTable from './TradeLog';
import LivePrice from './LivePrice';

function App() {
  const today = new Date();
  const defaultMonth = String(today.getMonth() + 1).padStart(2, '0');
  const defaultDay = String(today.getDate()).padStart(2, '0');
  const defaultYear = today.getFullYear();

  const [selectedSymbol, setSelectedSymbol] = useState('FNGU');
  const [month, setMonth] = useState(defaultMonth);
  const [day, setDay] = useState(defaultDay);
  const [year, setYear] = useState(defaultYear);
  const [marketData, setMarketData] = useState([]);
  const [tradeLog, setTradeLog] = useState([]);
  const [finalBalance, setFinalBalance] = useState(0);
  const [totalGainLoss, setTotalGainLoss] = useState(0);
  const [annualReturn, setAnnualReturn] = useState(0);
  const [totalReturn, setTotalReturn] = useState(0);

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

    if (isNaN(y) || y < 2021) y = 2024;
    if (y > defaultYear) y = defaultYear;

    const daysInMonth = new Date(y, m, 0).getDate();
    if (isNaN(d) || d < 1) d = 1;
    if (d > daysInMonth) d = daysInMonth;

    setMonth(String(m).padStart(2, '0'));
    setDay(String(d).padStart(2, '0'));
    setYear(String(y));
  };

  const downloadTradeLog = () => {
    const csvContent = [
      ["Date", "Symbol", "Action", "Price", "Shares", "Transaction Amount", "Gain/Loss", "Balance"],
      ...tradeLog.map(trade => [
        trade.date, trade.symbol, trade.action, trade.price, trade.shares, trade.transaction_amount, trade["gain/loss"], trade.balance
      ]),
      [],
      ["Summary"],
      ["Final Balance", finalBalance],
      ["Total Gain/Loss", totalGainLoss],
      ["Annual Return (%)", annualReturn],
      ["Total Return (%)", totalReturn]
    ]
    .map(row => row.join(","))
    .join("\n");
  
    const blob = new Blob([csvContent], { type: "text/csv;charset=utf-8;" });
    const link = document.createElement("a");
    link.href = URL.createObjectURL(blob);
    link.download = "trade_log.csv";
    link.style.display = "none";
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  useEffect(() => {
    const fetchData = async () => {
      try {
        const endDate = `${year}-${month}-${day}`;
        const response = await fetch('/fetch_market_data', {
          method: 'POST',
          headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            symbol: selectedSymbol,
            end_date: endDate,
          }),
        });

        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();
        if (response.ok) {
          console.log('Market Data:', data); 
          setMarketData(data.data); 
          setTradeLog(data.trade_log)
          setFinalBalance(data.final_balance)
        } else {
          console.error('Error fetching market data:', data.error);
        }
      } catch (error) {
        console.error('Error fetching market data:', error);
      }
    };

    fetchData();
  }, [selectedSymbol, month, day, year]); // Trigger fetch when symbol or date changes

  // Function to run backtest and fetch the results
  const runBacktest = async (algorithm) => {
    try {
      const endDate = `${year}-${month}-${day}`;
      const response = await fetch('/run_backtest', {
        method: 'POST',
        headers: {
          'Accept': 'application/json',
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          symbol: selectedSymbol,
          end_date: endDate,
          algorithm: algorithm,  
        }),
      });

      const data = await response.json();
      if (response.ok) {
        console.log('Backtest Data:', data);
        setTradeLog(data.trade_log); 
        setFinalBalance(data.final_balance); 
        setTotalGainLoss(data.total_gain_loss);
        setAnnualReturn(data.annual_return);
        setTotalReturn(data.total_return)
      } else {
        console.error('Error running backtest:', data.error);
      }
    } catch (error) {
      console.error('Error running backtest:', error);
    }
  };


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
      <LivePrice symbol={selectedSymbol} />

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
        <StockChart marketData={marketData} selectedSymbol={selectedSymbol} tradeLog={tradeLog} />
      </div>

      <p className="default-text">Please select a trading algorithm that you would like to use</p>
      <div className="button-container">
        <button className="symbol-button" onClick={() => runBacktest('SMA')}>
          SMA
        </button>
        <button className="symbol-button" onClick={() => runBacktest('BollingerBands')}>
          BB
        </button>
        <button className="symbol-button" onClick={() => runBacktest('MACD')}>
          MACD
        </button>
      </div>

      <div>
        <TradeLogTable
          trades={tradeLog}
          finalBalance={finalBalance}
          totalGainLoss={totalGainLoss}
          annualReturn={annualReturn}
          totalReturn={totalReturn}
        />
      </div>
      <div style={{ textAlign: 'center' }}>
        {tradeLog?.length > 0 && (
          <p
            className="download-link"
            onClick={downloadTradeLog}
            style={{
              cursor: 'pointer',
              color: 'blue',
              fontWeight: 'bold',
              textDecoration: 'underline',
              background: 'white',
              display: 'inline-block'
            }}
          >
            Download Trade Log as CSV
          </p>
        )}
      </div>
    </div>
  );
}

export default App;








