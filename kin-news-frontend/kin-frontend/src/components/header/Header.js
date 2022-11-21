import {NavLink} from "react-router-dom";
import {logout} from "../../redux/reducers/authReducer";
import {connect} from "react-redux";

import headerCss from "./Header.module.css"

function Header(props) {
    return (
        <>
            <header className={headerCss.header}>
                <h3><NavLink to={'/tape'}>TAPE</NavLink></h3>
                <h3><NavLink to={'/statistics'}>STATISTICS</NavLink></h3>

                <h3
                    onClick={(e) => props.logout()}
                >
                    LOG OUT
                </h3>
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
