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


class LinePlusBarChart(Nvd3Chart):

    funcName = "linePlusBarChart"
    funcBody = """
        function(session, object) {
    
            var chart = nv.models.linePlusBarChart()
                      .margin({bottom: 50, left: 70, right:50})
      
            chart.xAxis.showMaxMin(false)
                       .tickFormat(d3.format(',.1f'))
    
            chart.x2Axis.showMaxMin(false)
                       .tickFormat(d3.format(',.1f'))
    
            chart.y1Axis.showMaxMin(false)
                       .tickFormat(d3.format(',.1f'))
    
            chart.y2Axis.showMaxMin(false)
                       .tickFormat(d3.format(',.1f'))
            
           session.makeChart(session, object, chart);
        }
    """
    
    def __init__(self, nvd3Functions):
        super(self.__class__, self).__init__(nvd3Functions)
        self.key = []
        self.lineValue = []
        self.barValue = []
    
    def plot(self, data, key, lineValue, barValue, config={}):
        """
        Create a LinePlusBarChart

        Example:
            >>> df.head(1)
                             Date    Price   Quantity
                0   1136005200000   71.890  1271000.0            
            >>> lpb = nv.linePlusBarChart()

            >>> config={"color":nv.c10(), "height":400,
                        "xAxis":{"axisLabel":"x", "tickFormat":"%d-%m-%Y"},
                        "x2Axis":{"axisLabel":"x", "tickFormat":"%d-%m-%Y"}
                }
                
            >>> lpb.plot(df, "Date", lineValue="Price", barValue="Quantity", config=config)
            
        Parameters
        ----------
        data : dict of lists or Pandas DataFrame 
            If the paramter is a dict, each keys represent the name of the dataset in the list
              { 'A': ( 1,   2,   3),
                'B': ('C', 'T', 'D' }
            or a pandas DataFrame, each column representing a dataset
                 A  B
              0  1  C
              1  2  T
              2  3  D
        key : string
            Column name or dict key for values to used for the x axis
        lineValue : string
            Column name or dict key for values to used for line
        barValue : String
            Column name or dict key for values to used for bar
        config : dict
            dict of nvd3 options 
            (use as keywork argument in the form config=myconfig)

        Returns
        -------
            None        
        """

        dataConfig = self.chart(data, key=key, lineValue=lineValue, barValue=barValue, config=config)  
        self._plot(dataConfig)


    def convert(self, data, key, lineValue, barValue):
        self.key.append(key)
        self.lineValue.append(lineValue)
        self.barValue.append(barValue)

        df = data if isinstance(data, pd.DataFrame) else pd.DataFrame(data)
        
        lineData = {"key":lineValue, "values":df.loc[:,[key, lineValue]].rename(str, {key:"x", lineValue:"y"}).to_dict("records")}
        barData =  {"key":barValue, "values":df.loc[:,[key, barValue ]].rename(str, {key:"x", barValue:"y"}).to_dict("records"), "bar": True}
        
        return {"data": [lineData, barData]}


    def append(self, data, chart=0): 
        dataConfig = self.chart(data, key=self.key[chart], lineValue=self.lineValue[chart], barValue=self.barValue[chart], config=self.config[chart], chart=chart) 
        self._append(dataConfig, chart=chart)


