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

  const getLivePrice = async () => {
    try {
      const response = await fetch('/get_live_price', {
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
      console.error('Error fetching live price:', error);
    }
  };

  useEffect(() => {
    const updatePrice = async () => {
      const marketOpen = checkMarketHours();
      setIsMarketHours(marketOpen);
      
      if (marketOpen) {
        await getLivePrice();
      } else if (price !== null) {
        price = 100
        const changePercent = (Math.random() - 0.5) * 0.002;
        setPrice(price * (1 + changePercent));
      } 
    };

    updatePrice();
    const interval = setInterval(updatePrice, 10000);
    return () => clearInterval(interval);
  }, [symbol, price]);

  const priceStyle = {
    backgroundColor: 'var(--White)',
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
          ({isMarketHours ? 'Live Market Price' : 'Simulated Price'})
        </span>
      </div>
    </div>
  );
}

export default LivePrice;