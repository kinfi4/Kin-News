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
    Cell,
} from "recharts";
import {
    generateColorsList, getDataPercentage,
    makePercentage,
    renderCustomizedLabel,
    renderTooltipContent,
    toPercent,
    transformObjectToArray
} from "./helpers/DataTransformers";
import visualizationCss from "./ReportsVisualization.module.css"

const SuccessReport = (props) => {
    const messagesByHourCount = transformObjectToArray(props.report.messagesCountByDayHour, "hour", "messagesCount");
    const messagesByChannelCount = transformObjectToArray(props.report.messagesCountByChannel, "channel", "messagesCount");
    const messagesCountByCategory = transformObjectToArray(props.report.messagesCountByCategory, "category", "messagesCount");
    const messagesCountBySentimentType = transformObjectToArray(props.report.messagesCountBySentimentType, "sentiment", "messagesCount");
    const messagesCountByDate = transformObjectToArray(props.report.messagesCountByDate, "date", "messagesCount");
    const messagesCountByDateByCategory = transformObjectToArray(props.report.messagesCountByDateByCategory, "date", "categories");
    const messagesCountByDateBySentimentType = transformObjectToArray(props.report.messagesCountByDateBySentimentType, "date", "sentiment");
    const messagesCountByChannelBySentimentType = transformObjectToArray(props.report.messagesCountByChannelBySentimentType, "channel", "sentiment");
    const messagesCountByChannelByCategory = transformObjectToArray(props.report.messagesCountByChannelByCategory, "channel", "category");

    console.log(messagesCountByDateByCategory)

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
                <h2>Sentiment distribution by channels</h2>

                <BarChart
                    width={850}
                    height={400}
                    data={messagesCountByChannelBySentimentType}
                    stackOffset="expand"
                >
                    <XAxis dataKey="channel" />
                    <YAxis tickFormatter={toPercent} />
                    <Tooltip />
                    <Legend />
                        <Bar dataKey="sentiment.negative" name="Negative" fill="#dc4444" type="monotone" stackId="1" />
                        <Bar dataKey="sentiment.positive" name="Positive" fill="#79FAC5" type="monotone" stackId="1" />
                        <Bar dataKey="sentiment.neutral" name="Neutral" fill="#BA97B4" type="monotone" stackId="1" />
                </BarChart>
            </div>

            <div className={visualizationCss.chartContainer}>
                <h2>Sentiment Distribution</h2>

                <PieChart width={300} height={400}>
                    <Pie
                        data={messagesCountBySentimentType}
                        labelLine={false}
                        outerRadius={150}
                        dataKey="messagesCount"
                    >

                        {
                            messagesCountBySentimentType.map((entry, index) => {
                                return <Cell fill={["#00C6B5", "#F9F871", "#90cf95"][index]} name={entry.sentiment} />
                            })
                        }
                    </Pie>
                    <Tooltip />
                    <Legend />
                </PieChart>
            </div>

            <div className={visualizationCss.chartContainer}>
                <h2>Dependence sentiment color by date</h2>

                <AreaChart
                    width={1210}
                    height={400}
                    data={messagesCountByDateBySentimentType}
                    stackOffset="expand"
                >

                    <XAxis dataKey="date" />
                    <YAxis tickFormatter={toPercent} />
                    <Legend />
                    <Tooltip content={renderTooltipContent} />
                    <Area type="monotone" dataKey="sentiment.positive" stackId="1" stroke="#8884d8" fill="#8884d8" name={"Positive"} />
                    <Area type="monotone" dataKey="sentiment.negative" stackId="1" stroke="#82ca9d" fill="#82ca9d" name={"Negative"} />
                    <Area type="monotone" dataKey="sentiment.neutral" stackId="1" stroke="#ffc658" fill="#ffc658" name={"Neutral"} />
                </AreaChart>
            </div>
            <div className={visualizationCss.chartContainer}>
                <h2>Negative news during time</h2>

                <AreaChart
                    width={1210}
                    height={400}
                    data={messagesCountByDateBySentimentType}
                >

                    <XAxis dataKey="date" />
                    <YAxis />
                    <Tooltip />
                    <Legend />
                    <Area type="monotone" dataKey="sentiment.negative" stroke="#82ca9d" fill="#82ca9d" name={"Negative"} />
                </AreaChart>
            </div>
            <div className={visualizationCss.chartContainer}>
                <h2>Negative news percentage during time</h2>

                <AreaChart
                    width={1210}
                    height={400}
                    data={getDataPercentage(messagesCountByDateBySentimentType, "date", "sentiment", "negative")}
                >

                    <XAxis dataKey="date" />
                    <YAxis />
                    <Tooltip />
                    <Legend />
                    <Area type="monotone" dataKey="negative" stroke="#82ca9d" fill="#82ca9d" name={"Negative"} />
                </AreaChart>
            </div>
            <div className={visualizationCss.chartContainer}>
                <h2>Message categories distribution by channels</h2>

                <BarChart
                    width={590}
                    height={700}
                    data={messagesCountByChannelByCategory}
                    stackOffset="expand"
                    layout="vertical"
                >
                    <XAxis type="number" />
                    <YAxis dataKey="channel" type="category" />
                    <Tooltip />
                    <Legend />

                    <Bar dataKey="category.Shelling" name="Shelling" fill="#dc4444" stackId={'a'} />
                    <Bar dataKey="category.Political" name="Political" fill="#79FAC5" stackId={'a'}/>
                    <Bar dataKey="category.Humanitarian" name="Humanitarian" fill="#7db244" stackId={'a'} />
                    <Bar dataKey="category.Economical" name="Economical" fill="#4499b2" stackId={'a'} />
                </BarChart>
            </div>

            <div className={visualizationCss.chartContainer} style={{height: "775px"}}>
                <h2>News Categories</h2>

                <div className={visualizationCss.categoriesCounters}>
                    <div>
                        Shelling news total:  {props.report.messagesCountByCategory.Shelling}
                    </div>
                    <div>
                        Political news total:  {props.report.messagesCountByCategory.Political}
                    </div>
                    <div>
                        Economical news total:  {props.report.messagesCountByCategory.Economical}
                    </div>
                    <div>
                        Humanitarian news total:  {props.report.messagesCountByCategory.Humanitarian}
                    </div>
                </div>

                <PieChart width={550} height={400}>
                    <Pie
                        data={messagesCountByCategory}
                        labelLine={false}
                        outerRadius={160}
                        dataKey="messagesCount"
                        fill={"#8884d8"}
                    >

                        {
                            messagesCountByCategory.map((entry, index) => {
                                return <Cell fill={["#2CA884", "#F9F871", "#90AECF", "#EDB7D1"][index]} name={entry.category} />
                            })
                        }
                    </Pie>
                    <Tooltip />
                    <Legend />
                </PieChart>
            </div>

            <div className={visualizationCss.chartContainer}>
                <h2>Dependence of news number on dates by categories</h2>

                <LineChart
                    width={1210}
                    height={400}
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

            <div className={visualizationCss.chartContainer}>
                <h2>Shelling news during time</h2>

                <AreaChart
                    width={1210}
                    height={400}
                    data={messagesCountByDateByCategory}
                >

                    <XAxis dataKey="date" />
                    <YAxis />
                    <Tooltip />
                    <Legend />
                    <Area type="monotone" dataKey="categories.Shelling" stroke="#D0261B" fill="#DD261B" name={"Shelling"} />
                </AreaChart>
            </div>
            <div className={visualizationCss.chartContainer}>
                <h2>Shelling news percentage during time</h2>

                <AreaChart
                    width={1210}
                    height={400}
                    data={getDataPercentage(messagesCountByDateByCategory, "date", "categories", "Shelling")}
                >

                    <XAxis dataKey="date" />
                    <YAxis />
                    <Tooltip />
                    <Legend />
                    <Area type="monotone" dataKey="Shelling" stroke="#D0261B" fill="#DD261B" name={"Shelling"} />
                </AreaChart>
            </div>

        </div>
    );
};

export default SuccessReport;