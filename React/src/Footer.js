import React, {useState} from "react";
import NaviBar from "./NaviBar.js";
import PostForm from "./PostForm.js";
import NaviBarIcon from "./assets/NaviBarIcon.png";
import PostFormIcon from "./assets/PostFormIcon.png";
import MyFeed from './MyFeed';
import MyProfile from './MyProfile';
import Setting from './Setting';
import LogOutButton from "./LogOutButton.js";

function Footer(){
    const [isNaviBarOpen, setIsNaviBarOpen] = useState(false);
    const [activeElement, setActiveElement] = useState(null);
    const toggleNaviBar = () => {
        setIsNaviBarOpen(!isNaviBarOpen);
    }
    const handleNaviBarClick = (element) => {
        setActiveElement(element);
        setIsNaviBarOpen(false);
    }
    return(
        <footer>
        <button onClick={toggleNaviBar}>Toggle Navigation</button>
        {isNaviBarOpen && (
          <Nav handleClick={handleNaviBarClick} />
        )}
        {activeElement === 'MyFeed' && (
          <MyFeed />
        )}
        {activeElement === 'MyProfile' && (
          <MyProfile />
        )}
        {activeElement === 'Setting' && (
          <Setting />
        )}
        <LogOutButton />
      </footer>
    );
}
function Nav(props) {
    const { handleClick } = props;
    return (
      <nav>
        <ul>
          <li><a href="#"  onClick={() => handleClick('MyFeed')}>Feed</a></li>
          <li><a href="#" onClick={() => handleClick('MyProfile')}>Profile</a></li>
          <li><a href="#" onClick={() => handleClick('Setting')}>Setting</a></li>
        </ul>
      </nav>
    );
  }
export default Footer;