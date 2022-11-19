import axios from "axios";
import {NEWS_SERVICE_URL} from "../../config";

axios.defaults.xsrfHeaderName = "X-CSRFTOKEN";
axios.defaults.xsrfCookieName = "csrftoken";

let initialState = {
    channels: [],
    activeChannel: {},
    loading: false,

}


const GOT_CHANNELS = 'GOT_CHANNELS'
const CHANNEL_ADDED = 'CHANNEL_ADDED'
const CLEAR_STATE = 'CLEAR_STATE'
const SET_LOADING = 'SET_LOADING'

export const FETCH_ERROR = 'FETCH_ERROR'


export let addChannel = (link) => (dispatch) => {
    const token = localStorage.getItem("token")

    axios.post(NEWS_SERVICE_URL + '/api/v1/channels', {link: link}, {
        headers: {
            'Authorization': `Token ${token}`,
            'Content-Type': 'application/json',
        }
    }).then(res => {
        dispatch({type: CHANNEL_ADDED})
    }).catch(err => {
        console.log(err.response.data.errors)
        dispatch({type: FETCH_ERROR, errors: err.response.data.errors})
    })
}

export let fetchChannels = (link) => (dispatch) => {
    const token = localStorage.getItem("token")

    axios.get(NEWS_SERVICE_URL + '/api/v1/channels', {
        headers: {
            'Authorization': `Token ${token}`,
        }
    }).then(res => {
        dispatch({type: GOT_CHANNELS, channels: res.data})
    }).catch(err => {
        dispatch({type: FETCH_ERROR, errors: err.data.errors})
    })
}

export let channelsReducer = (state=initialState, action) => {
    switch (action.type){
        case GOT_CHANNELS:
            return {
                ...state,
                channels: action.channels,
                loading: false,
            }
        case SET_LOADING:
            return {
                ...state,
                loading: true,
            }
        case CLEAR_STATE:
            return initialState
        case CHANNEL_ADDED:
            return window.location.replace('/')
        default:
            return state
    }
}
