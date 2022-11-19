import channelCss from './Channel.module.css'
import {NEWS_SERVICE_URL} from "../../../../config";
import {showModalWindow} from "../../../../redux/reducers/modalWindowReducer";
import {addChannel, fetchChannels} from "../../../../redux/reducers/channelsReducer";
import {connect} from "react-redux";
import ChannelInfo from "./ChannelInfo";

const ChannelBlock = (props) => {
    function truncate(str, n){
        return (str.length > n) ? str.slice(0, n-1) + '...' : str;
    }

    return (
        <div
            className={channelCss.channelBlockContainer}
            onClick={(event) => {
                props.showModal(<ChannelInfo channel={props.channel} />, 800, 600)
            }}
        >
            {
                props.channelsLoading ? "LOADING" : <img src={NEWS_SERVICE_URL + props.channel.profilePhotoUrl} alt={truncate(props.channel.title, 14)}/>
            }
        </div>
    );
};

let mapStateToProps = (state) => {
    return {
        channelsLoading: state.channels.loading,
    }
}

let mapDispatchToProps = (dispatch) => {
    return {
        showModal: (content, width, height) => dispatch(showModalWindow(content, width, height)),
    }
}


export default connect(mapStateToProps, mapDispatchToProps)(ChannelBlock);