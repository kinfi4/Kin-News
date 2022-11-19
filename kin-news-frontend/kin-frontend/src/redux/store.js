import {createStore, combineReducers, applyMiddleware} from 'redux'
import thunk from 'redux-thunk'
import {auth} from "./reducers/authReducer";
import {modalWindowReducer} from "./reducers/modalWindowReducer";
import {channelsReducer} from "./reducers/channelsReducer";

let store = createStore(
    combineReducers({
        auth: auth,
        modalWindow: modalWindowReducer,
        channels: channelsReducer,
    }),
    applyMiddleware(thunk)
)

export default store