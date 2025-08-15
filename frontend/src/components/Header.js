import React from 'react';
import { Link } from 'react-router-dom';
import { toast } from 'react-toastify';

const Header = () => {
  return (
    <header className="header">
      <nav>
        <ul className="nav-list">
          <li>
            <Link to="/">Home</Link>
          </li>
          {/* <li>
            <Link to="/videos">My Videos</Link>
          </li> */}
        </ul>
      </nav>
    </header>
  );
};

export default Header;