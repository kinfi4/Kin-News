import {NavLink} from "react-router-dom";
import {login, logout} from "../../redux/reducers/authReducer";
import {connect} from "react-redux";

function Header(props) {
    return (
        <>
            <header>
                <nav>
                    <NavLink to={'/'}>
                        <h3>Tape</h3>
                    </NavLink>

                    <NavLink to={'/'}>
                        <h3>Analytics</h3>
                    </NavLink>

                    <h3
                        onClick={(e) => props.logout()}
                    >
                        Log out
                    </h3>
                </nav>
            </header>
        </>
    )
}

let mapStateToProps = (state) => {
    return {}
}

let mapDispatchToProps = (dispatch) => {
    return {
        logout: () => dispatch(logout)
    }
}


export default connect(mapStateToProps, mapDispatchToProps)(Header);
