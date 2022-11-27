import React from 'react';
import {
    BarChart,
    LineChart,
    CartesianGrid,
    Line,
    XAxis,
    YAxis,
    ResponsiveContainer,
    Tooltip,
    Legend,
    Bar,
    PieChart,
    Pie,
    AreaChart,
    Area,
} from "recharts";
import {getMessagesCountByDateByCategory, transformObjectToArray} from "./helpers/DataTransformers";
import visualizationCss from "./ReportsVisualization.module.css"
import {ECONOMICAL_CATEGORY, HUMANITARIAN_CATEGORY, POLITICAL_CATEGORY, SHELLING_CATEGORY} from "../../../../config";

const SuccessReport = (props) => {
    const messagesByHourCount = transformObjectToArray(props.report.messagesCountByDayHour, "hour", "messagesCount");
    const messagesByChannelCount = transformObjectToArray(props.report.messagesCountByChannel, "channel", "messagesCount");
    const messagesCountByCategory = transformObjectToArray(props.report.messagesCountByCategory, "category", "messagesCount");
    const messagesCountBySentimentType = transformObjectToArray(props.report.messagesCountBySentimentType, "sentiment", "messagesCount");
    const messagesCountByDate = transformObjectToArray(props.report.messagesCountByDate, "date", "messagesCount");
    const messagesCountByDateByCategory = transformObjectToArray(props.report.messagesCountByDateByCategory, "date", "categories");

    return (
        <div className={visualizationCss.visualizationContainer}>
            <h1>{props.report.name}</h1>

            <div className={visualizationCss.chartContainer}>
                <h2>Number of messages distributed by hours</h2>

                <BarChart
                    width={600}
                    height={300}
                    data={messagesByHourCount}
                >
                    <XAxis dataKey="hour" />
                    <YAxis />
                    <Tooltip />
                    <Legend />
                    <Bar dataKey="messagesCount" fill="#5C5972" name={"Number of messages"} />
                </BarChart>
            </div>

            <div className={visualizationCss.chartContainer}>
                <h2>Number of messages distributed by channels</h2>

                <BarChart
                    width={550}
                    height={300}
                    data={messagesByChannelCount}>
                    <XAxis dataKey="channel" />
                    <YAxis />
                    <Tooltip />
                    <Legend />
                    <Bar dataKey="messagesCount" fill="#BA97B4" name={"Number of messages"} />
                </BarChart>
            </div>

            <div className={visualizationCss.chartContainer}>
                <h2>Dependence of news number on dates</h2>


                <AreaChart
                    width={1210}
                    height={400}
                    data={messagesCountByDate}
                >
                    <XAxis dataKey="date" />
                    <YAxis />
                    <Tooltip />
                    <Legend />
                    <Area type="monotone" dataKey="messagesCount" stroke="#8884d8" fill="#8884d8" />
                </AreaChart>
            </div>
            <div className={visualizationCss.chartContainer}>
                <h2>Dependence of news number on dates by categories</h2>

                <LineChart
                    width={1210}
                    height={300}
                    data={messagesCountByDateByCategory}
                >
                    <XAxis dataKey="date" />
                    <YAxis />
                    <Tooltip />
                    <Legend />
                    <Line type="monotone" dataKey={"categories.Shelling"} stroke="#DD261B" name={"Shelling"} dot={false} />
                    <Line type="monotone" dataKey={"categories.Political"} stroke="#009BF9" name={"Political"} dot={false} />
                    <Line type="monotone" dataKey={"categories.Humanitarian"} stroke="#F9F871" name={"Humanitarian"} dot={false} />
                    <Line type="monotone" dataKey={"categories.Economical"} stroke="#25B382" name={"Economical"} dot={false} />
                </LineChart>
            </div>


        </div>
    );
};

export default SuccessReport;