import {createStore, combineReducers, applyMiddleware} from 'redux'
import thunk from 'redux-thunk'
import {auth} from "./reducers/authReducer";
import {modalWindowReducer} from "./reducers/modalWindowReducer";
import {channelsReducer} from "./reducers/channelsReducer";
import {postsReducer} from "./reducers/postsReducer";
import {ratingReducer} from "./reducers/ratingReducer";

let store = createStore(
    combineReducers({
        auth: auth,
        modalWindow: modalWindowReducer,
        channels: channelsReducer,
        postsReducer: postsReducer,
        ratingReducer: ratingReducer,
    }),
    applyMiddleware(thunk)
)

export default store
