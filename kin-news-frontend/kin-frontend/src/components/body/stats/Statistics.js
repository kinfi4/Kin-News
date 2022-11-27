import mainPageCss from "../MainPage.module.css";
import statisticsCss from "./Statistics.module.css"
import React from "react";

import 'react-date-range/dist/styles.css'; // main style file
import 'react-date-range/dist/theme/default.css'; // theme css file
import "./GenerateReportMenu/DateRangePickerStyles.css"
import {Link, Route, Switch} from "react-router-dom";
import {useRouteMatch} from "react-router-dom/cjs/react-router-dom";
import GenerateReportMenu from "./GenerateReportMenu/GenerateReportMenu";
import SelectReportMenu from "./SelectReport/SelectReportMenu";
import ReportVisualization from "./ReportVisualization/ReportVisualization";


const Statistics = (props) => {
    let {path, url} = useRouteMatch();

    return (
        <>
            <div className={mainPageCss.container}>
                <div className={mainPageCss.sideBar}>
                    <div className={mainPageCss.sideBarContent}>
                        <Switch>
                            <Route exact path={path} render={() => <SelectReportMenu />} />
                            <Route exact path={`${path}/generate`} render={() => <GenerateReportMenu />} />
                        </Switch>
                    </div>
                </div>
                <div className={statisticsCss.statsContainer}>
                    <ReportVisualization />
                </div>
            </div>
        </>
    )
}

export default Statistics;
