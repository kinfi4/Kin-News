import authCss from './auth.module.css'
import {connect} from "react-redux";
import {login} from "../../redux/reducers/authReducer";

function Login() {
    return (
        <>

        </>
    );
}


let mapStateToProps = (state) => {
    return {}
}

let mapDispatchToProps = (dispatch) => {
    return {
        login: (username, password) => dispatch(login(username, password))
    }
}


export default connect(mapStateToProps, mapDispatchToProps)(Login);
