import "./Header.css"
import SearchIcon from "@mui/icons-material/Search";
import LanguageIcon from "@mui/icons-material/Language";
import ExpandMoreIcon from "@mui/icons-material/ExpandMore";
import { Avatar } from "@mui/material";
import { Link } from "react-router-dom";
import logo from "./Logo.png";

const Header =()=> (
    <div className="header">
        <img 
            className="header__icon"
            src={logo}
            alt=""
        />

        <div className="header__center">
            <input type="text"/>
            <SearchIcon />
        </div>

        <div className="header__right">
            <p>Become a host</p>
            <LanguageIcon />
            <ExpandMoreIcon />
            <Avatar />
        </div>
    </div>
)

export default Header;