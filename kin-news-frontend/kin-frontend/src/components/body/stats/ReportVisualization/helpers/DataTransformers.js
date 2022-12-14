import {shuffle} from "../../../../../utils/utils";

export const transformObjectToArray = (data, xName, yName) => {
    return Object.entries(data).map(el => {
        let obj = {};
        obj[xName] = el[0];
        obj[yName] = el[1];

        return obj;
    });
}

export const renderCustomizedLabel = ({ cx, cy, midAngle, innerRadius, outerRadius, percent, index }) => {
    const RADIAN = Math.PI / 180;

    const radius = innerRadius + (outerRadius - innerRadius) * 0.5;
    const x = cx + radius * Math.cos(-midAngle * RADIAN);
    const y = cy + radius * Math.sin(-midAngle * RADIAN);

    return (
        <text x={x} y={y} fill="#f7fdff" textAnchor={x > cx ? 'start' : 'end'} dominantBaseline="central">
            {`${(percent * 100).toFixed(0)}%`}
        </text>
    );
};


export const generateColorsList = (numberOfColors) => {
    let allColors = [
        "#2CA884",
        "#8DD47A",
        "#F9F871",
        "#EDB7D1",
        "#00C6B5",
        "#90AECF"
    ];

    let res = shuffle(allColors).slice(0, numberOfColors);

    return res;
}

export const toPercent = (decimal, fixed = 0) => {
    // console.log(decimal)
    return `${(decimal * 100).toFixed(0)}%`
};


const getPercent = (value, total) => {
    const ratio = total > 0 ? value / total : 0;

    return toPercent(ratio, 2);
};
export const renderTooltipContent = (o) => {
    const { payload, label } = o;
    const total = payload.reduce((result, entry) => result + entry.value, 0);

    return (
        <div className="customized-tooltip-content">
            <p className="total">{`${label} (Total: ${total})`}</p>
            <ul className="list">
                {payload.map((entry, index) => (
                    <li key={`item-${index}`} style={{ color: entry.color, fontSize: "22px"}}>
                        {`${entry.name}: ${entry.value}(${getPercent(entry.value, total)})`}
                    </li>
                ))}
            </ul>
        </div>
    );
};


const sumValues = obj => Object.values(obj).reduce((a, b) => a + b, 0);

export const makePercentage = (data) => {
    let totalCount = sumValues(data);

    Object.keys(data).forEach(key => {
        data[key] = data[key] / totalCount;
    });

    return data;
}

export const getDataPercentage = (data, key, targetKey, targetCategory) => {
    return data.map(el => {
        const sum = sumValues(el[targetKey]);

        let res = {}
        res[key] = el[key]
        res[targetCategory] = (el[targetKey][targetCategory] / sum).toFixed(2)
        return res
    })
}


export function transformReportToWordsList(report, channelFilter=null, categoryFilter=null, wordsFilters=[]) {
    const all = "All";
    const allChannels = "All Channels";
    let result = [];

    if (channelFilter !== allChannels && categoryFilter !== all) {
        result = report.dataByChannelByCategory[channelFilter][categoryFilter].map(el => {
            return {text: el[0], value: el[1]};
        });
    } else if (channelFilter !== allChannels && categoryFilter === all) {
        result = report.dataByChannel[channelFilter].map(el => {
            return {text: el[0], value: el[1]};
        });
    } else if (channelFilter === allChannels && categoryFilter !== all) {
        result = report.dataByCategory[categoryFilter].map(el => {
            return {text: el[0], value: el[1]};
        });
    } else {
        result = report.totalWordsFrequency.map(el => {
            return {text: el[0], value: el[1]};
        });
    }

    if(wordsFilters !== []) {
        result = result.filter(el => !wordsFilters.includes(el.text));
    }

    return result;
}
