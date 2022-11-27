import React from 'react';
import {connect} from "react-redux";

const ReportVisualization = (props) => {
    if(props.report === null) {
        return <div></div>
    }

    return (
        <div>

        </div>
    );
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