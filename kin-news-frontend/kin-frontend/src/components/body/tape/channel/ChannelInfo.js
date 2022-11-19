import React from 'react';
import channelCss from './Channel.module.css'
import {showModalWindow} from "../../../../redux/reducers/modalWindowReducer";
import {connect} from "react-redux";
import {NEWS_SERVICE_URL} from "../../../../config";
import {truncate} from "../../../../utils/utils";


const ChannelInfo = (props) => {
    return (
        <div className={channelCss.channelInfoContainer}>
            <div>
                <img src={NEWS_SERVICE_URL + props.channel.profilePhotoUrl} alt={truncate(props.channel.title, 14)}/>
                <div>
                    STAR STAR STAR STAR
                </div>
            </div>
            <div>
                <h1>
                    {props.channel.title}
                </h1>
                <span className={channelCss.subsribersCount}>{props.channel.subscribersNumber} subscribers</span>
                <p>{props.channel.description}</p>
            </div>
        </div>
    );
};


let mapStateToProps = (state) => {
    return {}
}

let mapDispatchToProps = (dispatch) => {
    return {

    }
}

export default connect(mapStateToProps, mapDispatchToProps)(ChannelInfo);