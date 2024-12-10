import React, { useState, useEffect } from 'react';

function LivePrice({ symbol }) {
  const [price, setPrice] = useState(null);
  const [isMarketHours, setIsMarketHours] = useState(false);

  const checkMarketHours = () => {
    const now = new Date();
    const day = now.getDay();
    const hour = now.getHours();
    const minute = now.getMinutes();
    const currentTime = hour * 100 + minute;

    return day >= 1 && day <= 5 && currentTime >= 930 && currentTime <= 1600;
  };

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

    // Set up interval for price simulation
    const simulatePrice = () => {
      const marketOpen = checkMarketHours();
      setIsMarketHours(marketOpen);
      
      setPrice(prevPrice => {
        if (prevPrice === null) return null;
        const changePercent = (Math.random() - 0.5) * 0.002;
        return prevPrice * (1 + changePercent);
      });
    };

    const interval = setInterval(simulatePrice, 1000);
    return () => clearInterval(interval);
  }, [symbol]); // Include symbol in dependencies

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

  const statusStyle = {
    fontSize: '14px',
    color: isMarketHours ? 'var(--Green)' : 'var(--Red)',
    marginLeft: '10px',
  };

  return (
    <div style={{ textAlign: 'center', margin: '20px 0' }}>
      <div style={priceStyle}>
        Current Price: ${price ? price.toFixed(2) : 'Loading...'}
        <span style={statusStyle}>
          (Simulated Price)
        </span>
      </div>
    </div>
  );
}

export default LivePrice;