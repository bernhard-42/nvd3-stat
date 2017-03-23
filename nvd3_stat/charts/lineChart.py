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

from ..nvd3_chart import Nvd3Chart
import pandas as pd


class LineChart(Nvd3Chart):
    funcName = "lineChart"
    funcBody = """
        function(session, object) {

            var chart = nv.models.lineChart()
                    .focusEnable(false)
                    .useInteractiveGuideline(true)
                    .margin({right:  40})
                    .margin({bottom: 60})

            chart.xAxis.showMaxMin(false)
                       .tickFormat(d3.format(',.1f'))

            chart.yAxis.showMaxMin(false)
                       .tickFormat(d3.format(',.1f'))

            session.__functions.makeChart(session, object, chart);
        }        
    """

    def __init__(self, nvd3Functions):
        super(self.__class__, self).__init__(nvd3Functions)
        style = "<style>.dashed { stroke-dasharray: 7,7; }\n.dotted { stroke-dasharray: 3,3; } </style>"
        nvd3Functions.display(html=style)


    def convert(self, data, key=None, values=None, lineAttributes={}):
        """
        Convert data to LineChart format
        Example:
            >>> x1 = np.linspace(0, 4*np.pi, 100)
            >>> x2 = np.linspace(np.pi, 3*np.pi, 100)
            >>> sin =  {"X":x1, "Sin": np.sin(x1), "Cos": np.cos(x1)}
            >>> sin1 = {"X":x1, "Sin": np.sin(x1)}
            >>> cos1 = {"X":x2, "Cos": np.cos(x2)}
            
            >>> l1 = LineChart(nv.nvd3Functions)
            
            Option 1:
            >>> data = l1.convert([{"data":sin1, "key":"X", "values":"Sin", "lineAttributes":{"area":True, "fillOpacity":0.2, "style":"dashed"}}, 
                                   {"data":cos1, "key":"X", "values":"Cos", "lineAttributes":{"style":"dotted"}}])
            Option 2:
            >>> data = l1.convert(data=sin, key="X", values=["Sin", "Cos"], 
                                  lineAttributes={"area":[True,False], "fillOpacity":[0.2,0], "style":["dashed",None]})
            Option 3:
            >>> data = l1.convert(data=sin, key="X", values="Sin", lineAttributes={"style":"dotted"})
            
            >>> l1.plot({"data":data, "config":{}})
            
        Parameters
        ----------
        data : dict of lists / Pandas DataFrame or a list of dict of lists / Pandas DataFrame
            If the paramter is a dict, each keys represent the name of the dataset in the list
              { 'A': ( 1,   2,   3),
                'B': ('C', 'T', 'D' }
            or a pandas DataFrame, each column representing a dataset
                 A  B
              0  1  C
              1  2  T
              2  3  D
        key : string
            Column name or dict key for values to be used for the x axis
        values : string or list of strings
            Column name(s) or dict key(s) for values to be used for the line(s)
        lineAttributes : dict 
            A dict of attributes, e.g. {"area":[True,False,True], "fillOpacity":[0.2,0,0.4], "style":["dashed","dotted",None]}
            if "values" is list or {"area":True, "fillOpacity":0.2, "style":"dashed"} if "values" is a string
            The keys represent the value attribute for the lines, the value(s) reprentsthe setting.
            len(values) == len(attributes) for each lineAttribute
            
        Returns
        -------
        dict
            The input data converted to the specific nvd3 chart format
        """

        nvd3Data = []
        if isinstance(data, (list, tuple)):
            for d in data:
                line = self.convert(data=d["data"], key=d["key"], values=d["values"],
                                    lineAttributes=d["lineAttributes"])
                nvd3Data.append(line[0])
        else:
            df = data if isinstance(data, pd.DataFrame) else pd.DataFrame(data)

            if not isinstance(values, (list, tuple)):
                values = [values]
                lineAttributes = {k:[v] for k,v in lineAttributes.items()}
                
            for i in range(len(values)):
                line = {"key":values[i], "values":df.loc[:,[key, values[i]]].rename(str,{key:"x", values[i]:"y"}).to_dict("records")}
                for k,v in lineAttributes.items():
                    line["classed" if k == "style" else k] = v[i]
    
                nvd3Data.append(line)

        return nvd3Data 
        