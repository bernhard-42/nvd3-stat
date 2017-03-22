# Copyright 2017 Bernhard Walter
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from IPython import get_ipython

if get_ipython() is None:
    from zeppelin_session import ZeppelinSession
    isZeppelin = True
else:
    from IPython.display import Javascript, display_javascript
    from IPython.display import HTML, display_html    
    import json
    isZeppelin = False


class Nvd3Functions(object):
    
    makeChart = """
        
makeChart = function(session, object, chart) {
    console.log("makeChart called")
    var cacheId = "__nv__chart_cache_" + object.plotId;

    if(typeof(window.__zeppelin_session_debug) == "undefined") {
        window.__zeppelin_session_debug = 0;  // no debug output
    }
    
    var Logger = function(name) {
        this.name = name;
    }
    Logger.prototype.info = function(msg) {
        if (window.__zeppelin_session_debug > 0) {
            console.info(this.name + " [INFO] " + msg)
        }
    }
    Logger.prototype.debug = function(msg, obj) {
        if (window.__zeppelin_session_debug > 1) {
            if (typeof(obj) === "undefined") {
                console.log(this.name + " [DEBUG] " + msg)
            } else {
                console.log(this.name + " [DEBUG] " + msg, obj)
            }
        }
    }
    var logger = new Logger("NVD3-Stat");
    
    d3.selectAll('.nvtooltip').style('opacity', '0');  // remove all "zombie" tooltips

    nv.utils.windowResize = function(chart) { console.info("windowResize not supported") } // avoid d3 translate(Nan,5) errors
    var duration = 350;


    var identifyData = function(data) {
        if ((typeof(data[0].values) != "undefined") && (typeof(data[0].key) != "undefined")) {
            return "kv"
        } else if ((typeof(data[0].x) != "undefined") && (typeof(data[0].y) != "undefined")) {
            return "xy"
        } else {
            console.error('Unknown data type')
        }
    }


    var configure = function(chartModel, config) {
        for (var c in config) {
            console.log("CONFIG", c, config[c]);
            if (c == "margin" || c == "arcRadius") {
                chart[c](config[c]);                
            } else if ((typeof(config[c]) === "object") && ! Array.isArray(config[c])) {       // sub config, 1 level
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

    
    if (object.event == "plot") {
        logger.debug("plot " + object.plotId, object.data)

        var data = object.data.data;
        var config = object.data.config;

        var divId = "#" + object.plotId + " svg";
        session[cacheId] = {"data": data};

        nv.addGraph(function() {
            try {
                chart = configure(chart, config);
                chartData = d3.select(divId).datum(JSON.parse(JSON.stringify(data)));
                chartData.transition().duration(500).call(chart);
            } catch(err) {
                console.error(err.message);
            }

            
            session[cacheId].chart = chart;
            session[cacheId].chartData = chartData;

            return chart;
        })

                           
    } else if (object.event == "saveAsPng") {
        logger.debug("Save " + object.plotId + " as PNG")
        
        saveSvgAsPng(document.getElementById(object.plotId).children[0], object.data.filename + ".png");

    } else if (object.event == "replace") {

        var data = JSON.parse(JSON.stringify(object.data));  // clone data

        session[cacheId].data = data;
        var chart = session[cacheId].chart;
        var chartData = session[cacheId].chartData;
        console.log("replace: " + chart.container.parentNode.id)

        chartData.datum(data).transition().duration(duration).call(chart);

    } else if (object.event == "append") {

        var newData = JSON.parse(JSON.stringify(object.data));  // clone data

        var data = session[cacheId].data;

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

        var chart = session[cacheId].chart;
        var chartData = session[cacheId].chartData;
        logger.debug("append: " + chart.container.parentNode.id, newData)
        
        chartData.datum(data).transition().duration(duration).call(chart);

    } else if (object.event == "update") {

        var changedData = JSON.parse(JSON.stringify(object.data.changedData));  // clone data
        var rowIndices = object.data.rowIndices;
        
        var data = session[cacheId].data;
        
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
        
        var chart = session[cacheId].chart;
        var chartData = session[cacheId].chartData;
        logger.debug("update: " + chart.container.parentNode.id, changedData)

        chartData.datum(data).transition().duration(duration).call(chart);
        
    } else if (object.event == "delete") {

        var sortedIndices = object.data.rowIndices;

        var data = session[cacheId].data;

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
        
        var chart = session[cacheId].chart;
        var chartData = session[cacheId].chartData;
        logger.debug("delete: " + chart.container.parentNode.id, sortedIndices)

        chartData.datum(data).transition().duration(duration).call(chart);
        chart.update()
    }}
"""

    def __init__(self):
        if isZeppelin:
            self.session = ZeppelinSession()
            self.session.registerFunction("makeChart", Nvd3Functions.makeChart)
        else:
            JS1 = """
            window.Nvd3py = function() {
                this.session = {}
                console.log("nvd3py is initialized");
            }
            """
            JS2 = "window.Nvd3py.prototype." + Nvd3Functions.makeChart.lstrip() + "\n"
            JS3 = """
            window.nvd3py = new window.Nvd3py();
            window.nvd3py.session = {};
            window.nvd3py.session.__functions = {};
            window.nvd3py.session.__functions.makeChart = window.nvd3py.makeChart;
            """
            self.display_javascript(JS1 + JS2 + JS3)
            
 
    def display_html(self, html):
        if isZeppelin:
            print("%html")
            print(html)
        else:
            display_html(HTML(html))

 
    def display_javascript(self, js):
        if isZeppelin:
            print("%html")
            print("<script>%s</script>" % js)
        else:
            display_javascript(Javascript(js))


    def register(self, funcName, funcCode):
        if isZeppelin:
            self.session.registerFunction(funcName, "%s = %s" % (funcName, funcBody)) 
        else:
            js = "window.Nvd3py.prototype." + funcName.lstrip() + " = " + funcCode
            self.display_javascript(js)

 
    def send(self, funcName, event, data, divId, delay=200):
        if isZeppelin:
            self.session.call(funcName, {"event":event, "data": data, "plotId":"%s" % divId}, delay)
        else:
            payload = json.dumps({"event":event, "data": data, "plotId":"%s" % divId})
            self.display_javascript("window.nvd3py." + funcName + "(window.nvd3py.session, " + payload + ")")


    def reloadNVD3(self, nvd3version="1.8.5", d3version="3.5.17"):
        if isZeppelin:
            html = """
                <link href="https://cdnjs.cloudflare.com/ajax/libs/nvd3/%s/nv.d3.min.css" rel="stylesheet">
                <script src="https://cdnjs.cloudflare.com/ajax/libs/nvd3/%s/nv.d3.js"></script>
                <link href="https://cdnjs.cloudflare.com/ajax/libs/nvd3/%s/nv.d3.min.css" rel="stylesheet">
                <script src="http://cdn.rawgit.com/exupero/saveSvgAsPng/gh-pages/saveSvgAsPng.js" type="text/javascript"></script>
            """ % (d3version, nvd3version, nvd3version)
            self.display_html(html)
        else:
            js = """
            require.config({ paths: {d3:      "http://d3js.org/d3.v3.min",
                                     saveSvg: "http://cdn.rawgit.com/exupero/saveSvgAsPng/gh-pages/saveSvgAsPng"} });
            require(["d3"], function(d3) {
                window.d3 = d3;
                console.log("loaded d3", window.d3)

                require(["saveSvg"], function(saveSvgAsPng) {
                    window.saveSvgAsPng = saveSvgAsPng
                    console.log("loaded saveSvgAsPng", window.saveSvgAsPng);

                    $.getScript("https://cdnjs.cloudflare.com/ajax/libs/nvd3/1.8.5/nv.d3.js", function() {
                        $('<link/>', {
                           rel: 'stylesheet',
                           type: 'text/css',
                           href: 'https://cdnjs.cloudflare.com/ajax/libs/nvd3/1.8.5/nv.d3.css'
                        }).appendTo('head');
                        console.log("loaded nvd3", window.nv)
                    })
                })
            });
            """

            self.display_javascript(js)

