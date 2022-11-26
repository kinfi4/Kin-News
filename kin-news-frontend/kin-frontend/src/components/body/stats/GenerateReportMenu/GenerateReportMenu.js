import React, {useEffect, useState} from "react";
import statsCss from "../Statistics.module.css";
import mainPageCss from "../../MainPage.module.css";
import {DateRangePicker} from "react-date-range";
import {connect} from "react-redux";
import {Link} from "react-router-dom";
import {AiFillDelete, AiFillEdit} from "react-icons/ai";
import TapeCss from "../../tape/Tape.module.css";
import Input from "../../../common/input/Input";
import Button from "../../../common/button/Button";
import {showModalWindow} from "../../../../redux/reducers/modalWindowReducer";
import generateReportCss from "./GenerateReport.module.css"
import {fetchChannels} from "../../../../redux/reducers/channelsReducer";


const SelectChannelsWindow = (props) => {
    let [data, setData] = useState({channelLink: ""});


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
                onClick={(event) => props.addChannelLink(data.channelLink)}
            />

            <>
                {
                    props.channels.map((el, idx) => {
                        return (
                            <div
                                key={idx}
                                className={generateReportCss.reportBlock}
                            >
                                {el.link}
                                <span onClick={() => props.removeChannelFromList(el.channelLink)}><AiFillDelete /></span>
                            </div>
                        )
                    })
                }
            </>
        </div>
    )
}


const GenerateReportMenu = (props) => {
    useEffect(() => {
        props.fetchChannels();
    }, []);

    const [data, setData] = useState({startDate: new Date(), endDate: new Date(), channels: []});

    const addChannelToTheList = (channelLink) => {
        const newChannels = [...data.channels, channelLink];
        setData({channels: newChannels});
    }
    const removeChannelFromList = (channelLink) => {
        const newChannels = data.channels.filter(el => el.channelLink !== channelLink);
        setData({channels: newChannels});
    }

    return (
        <>
            <div className={statsCss.controls}>
                <Link to={`/statistics`}>
                    <div
                        className={mainPageCss.controlButton}
                        onClick={() => null}
                    >
                        CHOSE EXISTING REPORT
                    </div>
                </Link>

                <div
                    className={mainPageCss.controlButton}
                    onClick={() => props.showModal(
                        <SelectChannelsWindow
                            channels={props.channels}
                            addChannelLink={addChannelToTheList}
                            removeChannelFromList={removeChannelFromList}
                        />,
                        500,
                        800,
                    )}
                >
                    SELECT CHANNELS
                </div>
            </div>
            <DateRangePicker
                className={"bg-dark"}
                rangeColors={["#2CA884"]}
                ranges={[{
                    startDate: data.startDate,
                    endDate: data.endDate,
                    key: 'selection',
                }]}
                onChange={
                    (range) => setData({
                        startDate: range.selection.startDate,
                        endDate: range.selection.endDate,
                    })
                }
            />

            <div
                className={mainPageCss.controlButton}
                onClick={() => null}
                style={{marginTop: "100px", padding: "30px"}}
            >
                GENERATE
            </div>
        </>
    )
}


let mapStateToProps = (state) => {
    return {
        channels: state.channels.channels,
    }
}

let mapDispatchToProps = (dispatch) => {
    return {
        showModal: (content, width, height) => dispatch(showModalWindow(content, width, height)),
        fetchChannels: () => dispatch(fetchChannels()),
    }
}

export default connect(mapStateToProps, mapDispatchToProps)(GenerateReportMenu);