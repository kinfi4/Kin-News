import {NavLink} from "react-router-dom";

function Header() {
    return (
        <>
            <header>
                <nav className={s.navigation}>
                    <NavLink to={'/'}>
                        <h3>Tape</h3>
                    </NavLink>

                    <NavLink to={'/'}>
                        <h3>Analytics</h3>
                    </NavLink>

                    <NavLink to={'/'}>
                        <h3>Log out</h3>
                    </NavLink>
                </nav>
            </header>
        </>
    )
}


export default Header;
