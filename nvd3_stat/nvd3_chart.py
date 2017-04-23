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

from .nvd3_functions import Nvd3Functions
import numpy as np
import json

class Nvd3Chart(object):
    _plotId = 0

    def __init__(self, nvd3Functions):
        self.id = 0

        self.data = []
        self.config = []

        self.divIds = []
        self.nvd3Functions = nvd3Functions

        self.width = 1024
        self.height = 400
        self.delay = 200
        self.horizontal = False
        self.vertical = False
        self.gap = 15

    def _divId(self):
        return "%s_%03d" % (self.funcName, Nvd3Chart._plotId) 
        

    def _call(self, event, delay, divId, data):
        self.nvd3Functions.call(event, data, divId, delay)


    def _identifyData(self, data):
        if data[0].get("values") and data[0].get("key"):
            return "kv"
        elif data[0].get("y") and data[0].get("x"):
            return "xy"
        else:
            raise(ValueError('Unknown data type'))


    def _deNumpy(self, data):
        if isinstance(data, (list, tuple)):
            return [self._deNumpy(o) for o in data]
        elif isinstance(data, dict):
            return {k:self._deNumpy(v) for k,v in data.items()}
        else:
            return np.asscalar(data) if isinstance(data, np.generic) else data
   

    def deNumpy(self, dataConfig):
        return {k:(self._deNumpy(v) if k=="data" else v) for k,v in dataConfig.items()}
        

    def _plotAll(self, dataConfigs):

        # Define widths and heights

        _height = 0
        _widths = [] 
        _data = []
        _divIds = []

        for dataConfig in dataConfigs:
            Nvd3Chart._plotId = Nvd3Chart._plotId + 1
            self.divIds.append(self._divId())
            
            config = dataConfig["config"]
            if config.get("width"):
                _widths.append(config.get("width"))
            else:
                _widths.append(self.width)
    
            if config.get("height"):
                _height = max(_height, config.get("height"))

        if _height > 0:
            self.height = _height

        overallHeight = self.height
        if self.vertical:
            self.height = self.height + self.gap
            style = "margin-bottom: %dpx;" % self.gap
            overallHeight = len(dataConfigs) * self.height

        self.width = sum(_widths)
        
        style = ""
        # Print the divs as float:left
        if self.horizontal:
            style = "float:left;"

        html = """<div style="height:%dpx; width:%dpx">""" %  (overallHeight, self.width)

        for dataConfig, divId, width in zip(dataConfigs, self.divIds, _widths):
            html = html + """
            <div id="%s" class="with-3d-shadow with-transitions" style="%s height:%dpx; width:%dpx">
                <svg></svg>
                <script class="nvd3_data">
                    var data_%s = %s;
                </script>
                <script>
                    (function() {
                        var plot = %s
                        var synch = function(session, object) {
                            // in case of reload wait until libraries are loaded
                            window.nvd3_stat.promise.then(function() {
                                // window.nvd3_stat.session..charts["%s"] = plot;
                                plot(session, object);
                            })
                        }
                        document.getElementById("%s")
                                .addEventListener("load", synch(window.nvd3_stat.session, 
                                                  {"event":"plot", "data": data_%s, "plotId":"%s"}))
                    })();
                </script>
            </div>
            """ % (divId, style, self.height, width, divId, json.dumps(self.deNumpy(dataConfig)), 
                   self.funcBody.strip(), divId, divId, divId, divId)

        
        self.nvd3Functions.display(html=html)

    
    def _plot(self, dataConfig):
        if isinstance(dataConfig, list):
            self._plotAll(dataConfig)
        else:
            self._plotAll([dataConfig])


    def chart(self, *args, **kwargs):
        config = kwargs.get("config", {})
        chart = kwargs.get("chart")

        kw = {k:v for k,v in kwargs.items() if k not in ["config", "chart"]}
        data = self.convert(*args, **kw)
        if chart is None:
            self.data.append(data["data"])
            self.config.append(config)

        return dict(config=config, **data)


    def hplot(self, dataConfigs):
        self.horizontal = True
        self._plot(dataConfigs)


    def vplot(self, dataConfigs):
        self.vertical = True
        self._plot(dataConfigs)


    def _replace(self, dataConfig, chart=0):
        data = dataConfig["data"]
        self.data[chart] = data
        self._call("replace", 0, self.divIds[chart], data)
    
        
    def _append(self, dataConfig, chart=0):                              # needs to do the same as the javascript part
        newData = self._deNumpy(dataConfig["data"])

        def _appendData(dataType, data, newData):
            if dataType == "kv":
                if data["key"] == newData["key"]:
                    data["values"] = data["values"] + newData["values"]
                    for key in newData.keys():
                        if key not in ["key", "values"]:
                            data[key] = newData[key]
            else:
                data = data + newData

            return data

        dataType = self._identifyData(self.data[chart])

        if dataType == "kv":
            for i in range(len(self.data[chart])):
                self.data[chart][i] = _appendData("kv", self.data[chart][i], newData[i])
        elif dataType == "xy":
                self.data[chart] = _appendData("xy", self.data[chart], newData)
        else:
            raise(ValueError('Unknown data type'))

        self._call("append", 0, self.divIds[chart], newData)
    
            
    def update(self, rowIndices, dataConfig, chart=0):              # needs to do the same as the javascript part
        changedData = self._deNumpy(dataConfig["data"])
        
        def _updateData(data, rowIndices, changedData):
            for i in range(len(rowIndices)):
                data["values"][rowIndices[i]] = changedData["values"][i]
    
            for key in changedData.keys():
                if key not in ["key", "values"]:
                    data[key] = changedData[key]

        if type(self.data[chart]) == list and type(changedData) == list:
            for i in range(len(self.data[chart])):
                _updateData(self.data[chart][i], rowIndices, changedData[i])
        else:
            _updateData(self.data[chart], rowIndices, changedData)
            
        self._call("update", 0, self.divIds[chart], {"rowIndices":rowIndices, "changedData":changedData})

        
    def delete(self, rowIndices, chart=0):                          # needs to do the same as the javascript part

        sortedIndices = sorted(rowIndices, reverse=True)
        def _deleteData(data, rowIndices):
            for i in sortedIndices:
                data[chart]["values"].pop(i)
    
        if type(self.data[chart]) == list:
            for i in range(len(self.data[chart])):
                _deleteData(self.data[i], rowIndices)
        else:
            _deleteData(self.data[chart], rowIndices)
            
        self._call("delete", 0, self.divIds[chart], {"rowIndices":sortedIndices})
        

    def saveAsPng(self, filename=None, chart=0, backgroundColor="transparent"):
        if filename is None:
            filename = self.divIds[chart]
        self._call("saveAsPng", 0, self.divIds[chart], {"filename":filename, "backgroundColor":backgroundColor})


    def clone(self):
        dataConfig = [{"data":data, "config":config} for data, config in zip(self.data, self.config)]
        chartClone = self.__class__(self.nvd3Functions)
        chartClone.horizontal = self.horizontal
        chartClone.vertical = self.vertical
        chartClone._plot(dataConfig)
        return chartClone
