import React, {useState} from "react";
import TapeCss from "../../tape/Tape.module.css";
import Input from "../../../common/input/Input";
import Button from "../../../common/button/Button";
import generateReportCss from "./GenerateReport.module.css";
import {AiFillDelete} from "react-icons/ai";
import {connect} from "react-redux";
import {setChannelsListForGeneration} from "../../../../redux/reducers/reportsReducer";
import {showMessage} from "../../../../utils/messages";


const SelectChannelsWindow = (props) => {
    let [data, setData] = useState({channelLink: ""});

    const addNewChannel = (channelLink) => {
        if(!channelLink) {
            showMessage([{message: "Sorry, but you have to specify the link.", type: "danger"}])
            return
        }
        const newList = [...props.channels, channelLink];
        props.setChannels(newList);
    }

    const removeChannelFromList = (channelLink) => {
        const newList = props.channels.filter(link => link !== channelLink);
        props.setChannels(newList);
    }

    return (
        <div className={TapeCss.enterLinkContainer}>
            <h4 style={{marginBottom: "40px"}}>REPORT WILL BE GENERATED FOR ALL THE CHANNELS BELOW</h4>
            <Input
                value={data.channelLink}
                onChange={(event) => setData({channelLink: event.target.value})}
                placeholder={"Channel Link"}
            />

            <Button
                text={"Add channel"}
                onClick={() => addNewChannel(data.channelLink)}
            />

            <>
                {
                    props.channels.map((link, idx) => {
                        return (
                            <div
                                key={idx}
                                className={`${generateReportCss.reportBlock}`}
                            >
                                {link}
                                <span onClick={() => removeChannelFromList(link)}><AiFillDelete /></span>
                            </div>
                        )
                    })
                }
            </>
        </div>
    )
}


let mapStateToProps = (state) => {
    return {
        channels: state.reportsReducer.channelListForGeneration,
    }
}

let mapDispatchToProps = (dispatch) => {
    return {
        setChannels: (channels) => dispatch(setChannelsListForGeneration(channels))
    }
}

export default connect(mapStateToProps, mapDispatchToProps)(SelectChannelsWindow);