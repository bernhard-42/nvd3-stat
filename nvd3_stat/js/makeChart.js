window.nvd3_stat = { 
    session: {
        charts: {}
    } 
};

if(typeof(window.__nvd3_stat_debug) == "undefined") {
    window.__nvd3_stat_debug = 0;  // no debug output
}

window.nvd3_stat.session.makeChart = function(session, object, chart) {

    //
    // Generic Logger
    //

    var Logger = function(name) {
        this.name = name;
    }
    Logger.prototype.info = function(msg) {
        if (window.__nvd3_stat_debug > 0) {
            console.info(this.name + " [INFO] " + msg)
        }
    }
    Logger.prototype.debug = function(msg, obj) {
        if (window.__nvd3_stat_debug > 1) {
            if (typeof(obj) === "undefined") {
                console.log(this.name + " [DEBUG] " + msg)
            } else {
                console.log(this.name + " [DEBUG] " + msg, obj)
            }
        }
    }

    //
    // Determine type of data provided
    //

    var identifyData = function(data) {
        if ((typeof(data[0].values) != "undefined") && (typeof(data[0].key) != "undefined")) {
            return "kv"
        } else if ((typeof(data[0].x) != "undefined") && (typeof(data[0].y) != "undefined")) {
            return "xy"
        } else {
            console.error('Unknown data type')
        }
    }

    //
    // Apply configurations provided to chart
    //

    var configure = function(chartModel, config) {
        for (var c in config) {
            if (c == "margin" || c == "arcRadius") {
                chart[c](config[c]);                
            } else if ((typeof(config[c]) === "object") && ! Array.isArray(config[c])) { // sub config, 1 level
                for (var c2 in config[c]) {
                    if (c2 == "tickFormat") {
                        var format = config[c][c2];
                        if (format[0] == "%") {
                            chart[c][c2](function(d) { return d3.time.format(format)(new Date(d)) });
                        } else {
                            chart[c][c2](d3.format(format));
                        }
                    } else {
                        chart[c][c2](config[c][c2]);
                    }
                }
            } else {                                                                     // direct config
                if (c === "halfPie" && config[c]) {
                    chart.pie.startAngle(function(d) { return d.startAngle/2 - Math.PI/2 })
                             .endAngle(function(d)   { return d.endAngle/2   - Math.PI/2 });
                } else {
                    chart[c](config[c]);
                }
            }
        }
        return chart;
    }

    //
    // Initialization
    //

    var logger = new Logger("NVD3-Stat");
    
    logger.debug("makeChart called");

    d3.selectAll('.nvtooltip').style('opacity', '0');  // remove all "zombie" tooltips

    nv.utils.windowResize = function(chart) { console.info("windowResize not supported") } // avoid d3 translate(Nan,5) errors
    var duration = 350;

    var cache = window.nvd3_stat.session.charts;
    
    if (object.event == "plot") {

        //
        // Plotting data
        //

        logger.debug("plot " + object.plotId, object.data)

        var data = object.data.data;
        var config = object.data.config;
        var duration = 200;
        if (typeof config.duration != "undefined") {
            duration = config.duration
        }

        var divId = "#" + object.plotId + " svg";
        cache[object.plotId] = {"data": data, "config": config};

        nv.addGraph(function() {
            try {
                chart = configure(chart, config);
                chartData = d3.select(divId).datum(JSON.parse(JSON.stringify(data)));
                if (duration == 0) {
                    chartData.call(chart);
                } else {
                    chartData.transition().duration(duration).call(chart);
                }
            } catch(err) {
                console.error(err.message);
            }

            
            cache[object.plotId].chart = chart;
            cache[object.plotId].chartData = chartData;

            return chart;
        })

                           
    } else if (object.event == "append") {

        //
        // Append data
        //

        var newData = JSON.parse(JSON.stringify(object.data));  // clone data

        var data = cache[object.plotId].data;
        var config = cache[object.plotId].config;

        var _append = function(dataType, dold, dnew) {
            if (dataType == "kv") {
                dold.values = dold.values.concat(dnew.values);
                for (var attr in dnew) {
                    if (attr !== "key" && attr !== "values") {
                        dold[attr] = dnew[attr];
                    }
                }
            } else {
                dold = dold.concat(dnew);
            }
            return dold
        }
        
        var dataType = identifyData(data);
        if (dataType == "kv") {
            for (var i in data) {
                data[i] = _append("kv", data[i], newData[i])
            }
        } else if (dataType == "xy") {
            data = _append(dataType, data, newData)
        } else {
            console.error("Unknown data type");
        }
        
        var chart = cache[object.plotId].chart;
        var chartData = cache[object.plotId].chartData;
        logger.debug("append: " + chart.container.parentNode.id, newData)
        
        chartData.datum(data).transition().duration(duration).call(chart);

    } else if (object.event == "saveAsPng") {

        //
        // Save plot and download as PNG
        //

        logger.debug("Save " + object.plotId + " as PNG")
        window.saveSvgAsPng(document.getElementById(object.plotId).children[0], object.data.filename + ".png", {backgroundColor: object.data.backgroundColor});

    } else if (object.event == "replace") {

        //
        // Replace data (CURRENTLY UNUSED AND ONLY slightly tested)
        //

        var data = JSON.parse(JSON.stringify(object.data));  // clone data


        cache[object.plotId].data = data;
        var chart = cache[object.plotId].chart;
        var chartData = cache[object.plotId].chartData;
        console.log("replace: " + chart.container.parentNode.id)

        chartData.datum(data).transition().duration(duration).call(chart);

    } else if (object.event == "update") {

        //
        // Updqate data (CURRENTLY UNUSED AND ONLY slightly tested)
        //

        var changedData = JSON.parse(JSON.stringify(object.data.changedData));  // clone data
        var rowIndices = object.data.rowIndices;
        
        var data = cache[object.plotId].data;
        
        var _update = function(dold, dnew, rowIndices) {
            for (var i in rowIndices) {
                dold.values[rowIndices[i]] = dnew.values[i];
            }
            for (attr in dnew) {
                if (attr !== "key" && attr !== "values") {
                    dold[attr] = dnew[attr];
                }
            }
        }

        if (data instanceof Array && changedData instanceof Array) {
            for (i in data) { _update(data[i], changedData[i], rowIndices) }
        } else {
            _update(data, changedData, rowIndices)
        }
        
        var chart = cache[object.plotId].chart;
        var chartData = cache[object.plotId].chartData;
        logger.debug("update: " + chart.container.parentNode.id, changedData)

        chartData.datum(data).transition().duration(duration).call(chart);
        
    } else if (object.event == "delete") {

        //
        // Delete data (CURRENTLY UNUSED AND ONLY slightly tested)
        //

        var sortedIndices = object.data.rowIndices;

        var data = cache[object.plotId].data;

        var _delete = function(dold, rowIndices) {
            for (var i in sortedIndices) {
                dold.values.splice(sortedIndices[i], 1);
            }
        }

        if (data instanceof Array) {
            for (var i in data) { _delete(data[i], sortedIndices) }
        } else {
            _delete(data, sortedIndices)
        }
        
        var chart = cache[object.plotId].chart;
        var chartData = cache[object.plotId].chartData;
        logger.debug("delete: " + chart.container.parentNode.id, sortedIndices)

        chartData.datum(data).transition().duration(duration).call(chart);
        chart.update()
    }
}

console.info("nvd3_stat is initialized");
