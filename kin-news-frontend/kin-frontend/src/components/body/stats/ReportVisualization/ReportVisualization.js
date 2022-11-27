import React from 'react';
import {connect} from "react-redux";
import {REPORT_STATUS_POSTPONED, REPORT_STATUS_PROCESSING} from "../../../../config";
import PostponedReport from "./PostponedReport";
import SuccessReport from "./SuccessReport";
import ProcessingReport from "./ProcessingReport";

const ReportVisualization = (props) => {
    if(props.report === null || props.report === undefined) {
        return <div></div>
    }

    if (props.report.processingStatus === REPORT_STATUS_POSTPONED) {
        return <PostponedReport report={props.report} />
    }
    if (props.report.processingStatus === REPORT_STATUS_PROCESSING) {
        return <ProcessingReport report={props.report} />
    }

    return <SuccessReport report={props.report} />;
};

let mapStateToProps = (state) => {
    return {
        report: state.reportsReducer.detailedReport,
    }
}

let mapDispatchToProps = (dispatch) => {
    return {}
}

export default connect(mapStateToProps, mapDispatchToProps)(ReportVisualization);