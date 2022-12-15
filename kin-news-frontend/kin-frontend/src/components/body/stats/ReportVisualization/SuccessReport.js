import React, {useState} from 'react';
import {
    BarChart,
    LineChart,
    Line,
    XAxis,
    YAxis,
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
    getDataPercentage,
    renderTooltipContent,
    toPercent,
    transformObjectToArray
} from "./helpers/DataTransformers";
import visualizationCss from "./ReportsVisualization.module.css"
import {STATISTICS_SERVICE_URL} from "../../../../config";
import {capitalizeFirstLetter, downloadFile, transformLargeNumberToReadable} from "../../../../utils/utils";
import FilteringBlock from "./helpers/FilteringBlock";
import {FaFileCsv} from "react-icons/fa";
import {VscJson} from "react-icons/vsc";
import {getColor} from "./helpers/Colors";


const SuccessReport = (props) => {
    const [filteringState, setFilteringState] = useState({currentCategory: "Shelling", currentSentiment: "negative"});
    const [exportOptions, setExportOptions] = useState({activeExportOptions: false});
    function renderExportOptions() {
        if(exportOptions.activeExportOptions) {
            return (
                <div
                    className={visualizationCss.exportOptions}
                >
                    <div
                        onClick={() => {
                            downloadFile(STATISTICS_SERVICE_URL + `/api/v1/data/${props.report.reportId}?type=csv`, 'csv')
                        }}
                    >
                       <FaFileCsv style={{marginRight: "5px"}}/> CSV
                    </div>
                    <div
                        onClick={() => {
                            downloadFile(STATISTICS_SERVICE_URL + `/api/v1/data/${props.report.reportId}?type=json`, 'json')
                        }}
                    >
                       <VscJson style={{marginRight: "5px"}} /> <span style={{fontSize: "15px"}}>JSON</span>
                    </div>
                </div>
            )
        }

        return <></>
    }

    const messagesByHourCount = transformObjectToArray(props.report.messagesCountByDayHour, "hour", "messagesCount");
    const messagesByChannelCount = transformObjectToArray(props.report.messagesCountByChannel, "channel", "messagesCount");
    const messagesCountByCategory = transformObjectToArray(props.report.messagesCountByCategory, "category", "messagesCount");
    const messagesCountBySentimentType = transformObjectToArray(props.report.messagesCountBySentimentType, "sentiment", "messagesCount");
    const messagesCountByDate = transformObjectToArray(props.report.messagesCountByDate, "date", "messagesCount");
    const messagesCountByDateByCategory = transformObjectToArray(props.report.messagesCountByDateByCategory, "date", "categories");
    const messagesCountByDateBySentimentType = transformObjectToArray(props.report.messagesCountByDateBySentimentType, "date", "sentiment");
    const messagesCountByChannelBySentimentType = transformObjectToArray(props.report.messagesCountByChannelBySentimentType, "channel", "sentiment");
    const messagesCountByChannelByCategory = transformObjectToArray(props.report.messagesCountByChannelByCategory, "channel", "category");

    return (
        <div className={visualizationCss.visualizationContainer}>
            <div className={visualizationCss.header}>
                <span>
                    {props.report.name}
                    <span
                        style={{
                            fontSize: "20px",
                            marginLeft: "20px",
                            color: "#7b6991",
                        }}
                    >
                        [{transformLargeNumberToReadable(props.report.totalMessagesCount)} messages processed]
                    </span>
                </span>
                <div
                    className={visualizationCss.exportButton}
                    onMouseEnter={() => setExportOptions({activeExportOptions: true})}
                    onMouseLeave={() => setExportOptions({activeExportOptions: false})}
                >
                    EXPORT

                    {renderExportOptions()}
                </div>
            </div>

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
                    <Bar dataKey="messagesCount" fill={getColor("count")} name={"Number of messages"} />
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
                    <Bar dataKey="messagesCount" fill={getColor("count")} name={"Number of messages"} />
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
                    <Area type="monotone" dataKey="messagesCount" stroke={"#fff"} fill={getColor("count")} name={"Number of messages"} />
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
                        <Bar dataKey="sentiment.negative" name="Negative" fill={getColor("negative")} type="monotone" stackId="1" />
                        <Bar dataKey="sentiment.positive" name="Positive" fill={getColor("Positive")} type="monotone" stackId="1" />
                        <Bar dataKey="sentiment.neutral" name="Neutral" fill={getColor("Neutral")} type="monotone" stackId="1" />
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
                                return <Cell fill={getColor(entry.sentiment)} name={entry.sentiment} />
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
                    <Area type="monotone" dataKey="sentiment.positive" stackId="1" stroke={getColor("Positive")} fill={getColor("Positive")} name={"Positive"} />
                    <Area type="monotone" dataKey="sentiment.negative" stackId="1" stroke={getColor("Negative")} fill={getColor("Negative")} name={"Negative"} />
                    <Area type="monotone" dataKey="sentiment.neutral" stackId="1" stroke={getColor("Neutral")} fill={getColor("Neutral")} name={"Neutral"} />
                </AreaChart>
            </div>
            <div className={visualizationCss.chartContainer}>
                <FilteringBlock
                    currentOption={filteringState.currentSentiment}
                    options={[
                        {label: "Negative", onClick: () => setFilteringState({...filteringState, currentSentiment: "negative"})},
                        {label: "Positive", onClick: () => setFilteringState({...filteringState, currentSentiment: "positive"})},
                        {label: "Neutral", onClick: () => setFilteringState({...filteringState, currentSentiment: "neutral"})},
                    ]}
                />
                <h2>{capitalizeFirstLetter(filteringState.currentSentiment)} news during time</h2>

                <AreaChart
                    width={1210}
                    height={400}
                    data={messagesCountByDateBySentimentType}
                >

                    <XAxis dataKey="date" />
                    <YAxis />
                    <Tooltip />
                    <Legend />
                    <Area
                        type="monotone"
                        dataKey={`sentiment.${filteringState.currentSentiment}`}
                        stroke={getColor(filteringState.currentSentiment)}
                        fill={getColor(filteringState.currentSentiment)}
                        name={capitalizeFirstLetter(filteringState.currentSentiment)}
                    />
                </AreaChart>
            </div>
            <div className={visualizationCss.chartContainer}>
                <h2>{capitalizeFirstLetter(filteringState.currentSentiment)} news percentage during time</h2>

                <AreaChart
                    width={1210}
                    height={400}
                    data={getDataPercentage(messagesCountByDateBySentimentType, "date", "sentiment", filteringState.currentSentiment)}
                >

                    <XAxis dataKey="date" />
                    <YAxis />
                    <Tooltip />
                    <Legend />
                    <Area
                        type="monotone"
                        dataKey={filteringState.currentSentiment}
                        stroke={getColor(filteringState.currentSentiment)}
                        fill={getColor(filteringState.currentSentiment)}
                        name={capitalizeFirstLetter(filteringState.currentSentiment)}
                    />
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

                    <Bar dataKey="category.Shelling" name="Shelling" fill={getColor("Shelling")} stackId={'a'} />
                    <Bar dataKey="category.Political" name="Political" fill={getColor("Political")} stackId={'a'}/>
                    <Bar dataKey="category.Humanitarian" name="Humanitarian" fill={getColor("Humanitarian")} stackId={'a'} />
                    <Bar dataKey="category.Economical" name="Economical" fill={getColor("Economical")} stackId={'a'} />
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
                        fill={getColor("count")}
                    >

                        {
                            messagesCountByCategory.map((entry, index) => {
                                return <Cell fill={getColor(entry.category)} name={entry.category} />
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
                    <Line type="monotone" dataKey={"categories.Shelling"} stroke={getColor("shelling")} name={"Shelling"} dot={false} />
                    <Line type="monotone" dataKey={"categories.Political"} stroke={getColor("Political")} name={"Political"} dot={false} />
                    <Line type="monotone" dataKey={"categories.Humanitarian"} stroke={getColor("Humanitarian")} name={"Humanitarian"} dot={false} />
                    <Line type="monotone" dataKey={"categories.Economical"} stroke={getColor("Economical")} name={"Economical"} dot={false} />
                </LineChart>
            </div>

            <div className={visualizationCss.chartContainer}>
                <h2>{filteringState.currentCategory} news during time</h2>

                <FilteringBlock
                    currentOption={filteringState.currentCategory}
                    options={[
                        {label: "Shelling", onClick: () => setFilteringState({...filteringState, currentCategory: "Shelling"})},
                        {label: "Economical", onClick: () => setFilteringState({...filteringState, currentCategory: "Economical"})},
                        {label: "Humanitarian", onClick: () => setFilteringState({...filteringState, currentCategory: "Humanitarian"})},
                        {label: "Political", onClick: () => setFilteringState({...filteringState, currentCategory: "Political"})},
                    ]}
                />

                <AreaChart
                    width={1210}
                    height={400}
                    data={messagesCountByDateByCategory}
                >

                    <XAxis dataKey="date" />
                    <YAxis />
                    <Tooltip />
                    <Legend />
                    <Area
                        type="monotone"
                        dataKey={`categories.${filteringState.currentCategory}`}
                        stroke={getColor(filteringState.currentCategory)}
                        fill={getColor(filteringState.currentCategory)}
                        name={filteringState.currentCategory}
                    />
                </AreaChart>
            </div>
            <div className={visualizationCss.chartContainer}>
                <h2>{filteringState.currentCategory} news percentage during time</h2>

                <AreaChart
                    width={1210}
                    height={400}
                    data={getDataPercentage(messagesCountByDateByCategory, "date", "categories", filteringState.currentCategory)}
                >

                    <XAxis dataKey="date" />
                    <YAxis />
                    <Tooltip />
                    <Legend />
                    <Area
                        type="monotone"
                        dataKey={filteringState.currentCategory}
                        stroke={getColor(filteringState.currentCategory)}
                        fill={getColor(filteringState.currentCategory)}
                        name={filteringState.currentCategory}
                    />
                </AreaChart>
            </div>

        </div>
    );
};

export default SuccessReport;