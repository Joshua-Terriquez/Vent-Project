import React, { useState } from "react";
import "./NaviBarIcon.css"

const NaviBar = () => {
  const [menuOpen, setMenuOpen] = useState(false);

  const toggleMenu = () => {
    setMenuOpen(!menuOpen);
  };

  return (
    <>
      <button className={`menu-button ${menuOpen ? "menu-open" : ""}`} onClick={toggleMenu}>
        <div className="strip"></div>
        <div className="strip"></div>
        <div className="strip"></div>
      </button>
      <div className={`sidebar ${menuOpen ? "menu-open" : ""}`}></div>
    </>
  );
};

export default NaviBar;