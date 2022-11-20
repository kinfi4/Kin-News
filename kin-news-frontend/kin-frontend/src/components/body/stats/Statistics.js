import mainPageCss from "../MainPage.module.css";
import React, {useState} from "react";
import { DateRangePicker } from 'react-date-range';
import 'react-date-range/dist/styles.css'; // main style file
import 'react-date-range/dist/theme/default.css'; // theme css file


const Statistics = (props) => {
    const [data, setData] = useState({startDate: new Date(), endDate: new Date()});

    return (
        <>
            <div className={mainPageCss.container}>
                <div className={mainPageCss.sideBar}>
                    <div className={mainPageCss.sideBarContent}>
                        <div
                            className={mainPageCss.controlButton}
                            onClick={() => null}
                        >
                            CHOSE EXISTING REPORT
                        </div>

                        <div
                            className={mainPageCss.controlButton}
                            onClick={() => null}
                        >
                            GENERATE REPORT
                        </div>

                        <DateRangePicker
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

                    </div>
                </div>
                <div className={'statisticsCss.tape'}>
                </div>
            </div>
        </>
    )
}

export default Statistics;
