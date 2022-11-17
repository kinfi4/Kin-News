import Header from "./header/Header";
import ModalWindow from "./common/modal/ModalWindow";
import {Route, Routes} from "react-router-dom";
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


function Main() {
    return (
        <>
            <Header />
            <Routes>
                <Route path={'/statistics'} element={<Statistics />} />
                <Route path={'/*'} element={<Tape />} />
            </Routes>
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

          <Routes>
              <Route exact path={'/sign-in'} element={<Login />} />
              <Route exact path={'/sign-up'} element={<Register />} />
              <Route path={''} element={<Main />} />
          </Routes>
      </>
  );
}

export default App;
