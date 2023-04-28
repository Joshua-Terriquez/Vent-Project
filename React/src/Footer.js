import React, {useState} from "react";
import NaviBar from "./NaviBar.js";
import PostForm from "./PostForm.js";
import NaviBarIcon from "./assets/NaviBarIcon.png";
import PostFormIcon from "./assets/PostFormIcon.png";

function Footer(){
    const [showNaviBar, setShowNaviBar] = useState(false);
    const [showPostForm, setshowPostForm] = useState(false);
    const handleNaviBarClick = () => {
        setShowNaviBar(!showNaviBar);
    };
    const handlePostFormClick = () => {
        setshowPostForm(!showPostForm);
    };

    return (
        <div className="footer">
            <button className="navibar-toggle" onclick={handleNaviBarClick}>
            <img id="NaviBarIcon" src={NaviBarIcon} alt="NaviBar" width="50" height="50"/>
            </button>
            <button className="PostForm-toggle" onclick={handlePostFormClick}>
            <img id="PostFormIcon" src={PostFormIcon} alt="PostForm" width="50" height="50"/>
            </button>
            {showNaviBar && <NaviBar />}
            {showPostForm && <PostForm />}
        </div>
    );
}
export default Footer;