import React, {useEffect, useState} from "react";
import statsCss from "../Statistics.module.css";
import mainPageCss from "../../MainPage.module.css";
import {DateRangePicker} from "react-date-range";
import {connect} from "react-redux";
import {Link} from "react-router-dom";
import {showModalWindow} from "../../../../redux/reducers/modalWindowReducer";
import SelectChannelsWindow from "./SelectChannels";
import {generateReport, setChannelsListForGeneration} from "../../../../redux/reducers/reportsReducer";
import {fetchChannels} from "../../../../redux/reducers/channelsReducer";


const GenerateReportMenu = (props) => {
    useEffect(() => {
        props.fetchChannels();
    }, []);
    useEffect(() => {
        props.setChannels(props.initialChannels.map(el => el.link));
    }, [props.initialChannels]);

    const [data, setData] = useState({startDate: new Date(), endDate: new Date()});

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
                        <SelectChannelsWindow />,
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
                onClick={() => props.sendGenerationRequest(data.startDate, data.endDate, props.channels)}
                style={{marginTop: "100px", padding: "30px"}}
            >
                GENERATE
            </div>
        </>
    )
}


let mapStateToProps = (state) => {
    return {
        initialChannels: state.channels.channels,
        channels: state.reportsReducer.channelListForGeneration,
    }
}

let mapDispatchToProps = (dispatch) => {
    return {
        showModal: (content, width, height) => dispatch(showModalWindow(content, width, height)),
        sendGenerationRequest: (startDate, endDate, channels) => dispatch(generateReport(startDate, endDate, channels)),
        setChannels: (channels) => dispatch(setChannelsListForGeneration(channels)),
        fetchChannels: () => dispatch(fetchChannels()),
    }
}

export default connect(mapStateToProps, mapDispatchToProps)(GenerateReportMenu);