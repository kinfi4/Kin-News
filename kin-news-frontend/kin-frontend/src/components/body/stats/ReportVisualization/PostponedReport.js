import React from 'react';
import reportsVisualizationCss from "./ReportsVisualization.module.css"
import processingImageFailedIcon from "../../../../images/processing-failed-icon.jpg"

const PostponedReport = (props) => {
    return (
        <div className={reportsVisualizationCss.postponedContainer}>
            <h1>REPORT: {props.report.name}</h1>
            <div>
                <img src={processingImageFailedIcon} alt="Processing Failed"/>
                <div>
                    We are sorry for this! But your report processing failed with error: <br/> <br/>
                    {props.report.reportFailedReason}
                </div>
            </div>
        </div>
    );
};

export default PostponedReport;