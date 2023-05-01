import React, {useState} from "react";
function LogOutButton(){
    const [loggedOut, setLoggedOut] = useState(false);
    
    const handleLogout = () => {
        fetch("logout")
            .then((res) => res.json())
            .then((data) => {
                if(data.success) {
                    setLoggedOut(true)
                    window.location.href = "/Login";
                }
            })
            .catch((error) => console.log(error));
    };
    return(
        <button conClick="handleLogout">
            {loggedOut ? "Logged out!" : "Log out"}
        </button>
    )
}
export default LogOutButton;