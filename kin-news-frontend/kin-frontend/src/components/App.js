import Header from "./header/Header";
import ModalWindow from "./common/modal/ModalWindow";
import {Route, Switch, Redirect} from "react-router-dom";
import Login from "./auth/login";
import Register from "./auth/register";
import Footer from "./footer/Footer";
import Statistics from "./body/stats/Statistics";
import Tape from "./body/tape/Tape";
import {useEffect} from "react";
import store from "../redux/store";
import {loadUser} from "../redux/reducers/authReducer";
import {ReactNotifications} from "react-notifications-component";
import 'react-notifications-component/dist/theme.css'


export function Main() {
    return (
        <>
            <Header/>

            <Switch>
                <Route path={'/statistics'} render={() => <Statistics />} />
                <Route exact path={'/tape'} render={() => <Tape />} />
                <Route path={'/'} render={() => <Redirect to={'/tape'}/>} />
            </Switch>

            <Footer />
        </>
    )
}

function App() {
    useEffect(() => {
        store.dispatch(loadUser())
    })

    return (
      <>
          <ReactNotifications />
          <ModalWindow />

          <Switch>
              <Route exact path={'/sign-in'} render={() => <Login />} />
              <Route exact path={'/sign-up'} render={() => <Register />} />
              <Route path={'/'} render={() => <Main />} />
          </Switch>
      </>
  );
}

export default App;
