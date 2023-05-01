import React from "react";
import "./NaviBarStyle.css"

const NaviBar = ({items, activeItem, onItemClick}) =>{
  return (
    <div className="naviBar">
      <ul>
        {items.map((item, index) => (
          <li key ={index} className={activeItem === index ? 'active' : ''}>
            <a href="#" onClick={() => onItemClick(index)}>{item}</a>
          </li>
        ))}
      </ul>
    </div>
  );
};
export default NaviBar;