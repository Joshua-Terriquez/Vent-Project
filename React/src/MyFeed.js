import React, { useState } from 'react';
import './MyFeed.css';
function MainPage() {
    const [showText, setShowText] = useState(false);
    const [h2Text, setH2Text] = useState('');

    function handleClick() {
      setShowText(true);
      setTimeout(() => {
        setShowText(false);
      }, 2000);
    }
  
    return (
        <div className="FeedForm">
          <button onClick={fetchData} className='rating'>
            <span className="Arrow">&#8593;</span>
          </button>
          <button onClick={fetchData} className='rating'>
          <span className="Arrow">&#8595;</span>
          </button>
        {showText && (
          <h2 className="h2-transition">{h2Text}</h2>
        )}
      </div>
    );
}

export default MainPage;