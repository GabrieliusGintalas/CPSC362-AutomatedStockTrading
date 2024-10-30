import React from 'react';

const TradeLogTable = ({ trades, finalBalance, totalGainLoss, annualReturn, totalReturn }) => {
  // Check if trades is undefined or null, and render a loading message or empty state
  if (!trades || trades.length === 0) {
    return <p>No trade data available.</p>;
  }

  const tradelogHolder = {
    display: 'flex',
    flexDirection: 'column',
    justifyContent: 'center',
    alignItems: 'center',
    margin: '0 auto',
  };

  const tradelogText = {
    color: 'var(--Black)',
    fontWeight: 'bold',
    fontSize: '30px',
    margin: '0',
    padding: '0',
    marginTop: '10px',
  };

  const performanceSummaryGrid = {
    display: 'grid',
    gridTemplateColumns: 'repeat(2, 1fr)', 
    gap: '10px',
    marginTop: '20px',
    width: '50%',
    color: 'var(--Black)',
    fontSize: '18px',
    fontWeight: 'normal',
    textAlign: 'center',
    backgroundColor: 'var(--SkyBlue)',
    padding: '20px',
    border: '1px solid #ddd',
    borderRadius: '5px',
  };

  const performanceItem = {
    padding: '10px 0',
    borderBottom: '1px solid #ddd',
  };

  const performanceValue = {
    fontWeight: 'bold',
  };

  return (
    <div style={tradelogHolder}>
      <p style={tradelogText}>Trade Log</p>
      <div className="trade-log-grid">
        <table className="trade-log-table">
          <thead>
            <tr>
              <th>Date</th>
              <th>Action</th>
              <th>Price</th>
              <th>Shares</th>
              <th>Transaction Amount</th>
              <th>Gain/Loss</th>
              <th>Balance</th>
            </tr>
          </thead>
          <tbody>
            {trades.map((trade, index) => (
              <tr key={index}>
                <td>{trade.date}</td>
                <td>{trade.action}</td>
                <td>{trade.price.toFixed(2)}</td>
                <td>{trade.shares}</td>
                <td>{trade.transaction_amount.toFixed(2)}</td>
                <td>{trade['gain/loss'] !== null ? trade['gain/loss'].toFixed(2) : 'N/A'}</td>
                <td>{trade.balance.toFixed(2)}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      <div style={performanceSummaryGrid}>
        <div style={performanceItem}>Final Balance</div>
        <div style={{...performanceItem, ...performanceValue}}>${finalBalance.toFixed(2)}</div>
        
        <div style={performanceItem}>Gain/Loss for all trades</div>
        <div style={{...performanceItem, ...performanceValue}}>${totalGainLoss.toFixed(2)}</div>
        
        <div style={performanceItem}>Annual % Return</div>
        <div style={{...performanceItem, ...performanceValue}}>{annualReturn.toFixed(2)}%</div>
        
        <div style={performanceItem}>Total % Return</div>
        <div style={{...performanceItem, ...performanceValue}}>{totalReturn.toFixed(2)}%</div>
      </div>

    </div>
  );
};

export default TradeLogTable;

