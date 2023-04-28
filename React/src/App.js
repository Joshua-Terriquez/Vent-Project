import Login from "./Login.js";
import React, { useState } from 'react';
import MyFeed from "./MyFeed.js";
import Footer from "./Footer.js";
import NaviBar from "./NaviBar.js"

import './App.css';

function App() {
  const [count, setCount] = useState(0);

  return (
    <div className="App">
      <MyFeed />
    </div>
  );
}

export default App;
