import React, { useState, useEffect } from 'react';

function LivePrice({ symbol }) {
  const [price, setPrice] = useState(null);
  const [isMarketHours, setIsMarketHours] = useState(false);

  const getLastClosingPrice = async () => {
    try {
      const response = await fetch('/get_last_closing_price', {
        method: 'POST',
        headers: {
          'Accept': 'application/json',
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          symbol: symbol
        }),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      setPrice(data.price);
    } catch (error) {
      console.error('Error fetching last closing price:', error);
    }
  };

  useEffect(() => {
    // Reset price when symbol changes
    setPrice(null);
    
    // Initial fetch of last closing price
    getLastClosingPrice();

    // Set up polling interval to get updated prices
    const interval = setInterval(getLastClosingPrice, 1000);
    return () => clearInterval(interval);
  }, [symbol]);

  const priceStyle = {
    backgroundColor: 'var(--LightGray)',
    padding: '10px 20px',
    borderRadius: '5px',
    margin: '10px 0',
    display: 'inline-block',
    fontWeight: 'bold',
    fontSize: '18px',
    color: 'var(--Black)',
  };

  return (
    <div style={{ textAlign: 'center', margin: '20px 0' }}>
      <div style={priceStyle}>
        Current Price: ${price ? price.toFixed(2) : 'Loading...'}
        <span style={{ fontSize: '14px', marginLeft: '10px' }}>
          (Simulated Price)
        </span>
      </div>
    </div>
  );
}

export default LivePrice;