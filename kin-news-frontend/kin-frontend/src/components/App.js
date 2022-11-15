import Header from "./header/Header";
import ModalWindow from "./common/modal/ModalWindow";
import {Route} from "react-router-dom";
import Login from "./auth/login";
import Register from "./auth/register";
import Footer from "./footer/Footer";
import Statistics from "./body/stats/Statistics";
import Tape from "./body/tape/Tape";
import {useEffect} from "react";
import store from "../redux/store";
import {loadUser} from "../redux/reducers/authReducer";


function App() {
    useEffect(() => {
        store.dispatch(loadUser())
    })

    return (
      <>
          {/*<ReactNotifications />*/}
          <ModalWindow />

          <Route exact path={'/sign-in'} render={() => <Login />} />
          <Route exact path={'/sign-up'} render={() => <Register />} />

          <Header />
              <Route exact path={'/statistics'} render={() => <Statistics />} />
              <Route path={'/'} render={() => <Tape />} />
          <Footer />
      </>
  );
}

export default App;
