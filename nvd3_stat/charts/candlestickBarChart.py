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


class CandlestickBarChart(Nvd3Chart):

    funcName = "candlestickBarChart"
    funcBody = """
        function(session, object) {

            var chart = nv.models.candlestickBarChart()
                 .x(function(d) { return d['date'] })
                 .y(function(d) { return d['close'] })
                 .useInteractiveGuideline(true)
                 .showLegend(false)
                      
            chart.xAxis.showMaxMin(false)
                       .tickFormat(function(d) { console.log(d); return d3.time.format("%x")(new Date(d)) })

            chart.yAxis.showMaxMin(true)
                       .tickFormat(d3.format(',.1f'))

            session.__functions.makeChart(session, object, chart);
        }        
    """
    
    def __init__(self, nvd3Functions):
        super(self.__class__, self).__init__(nvd3Functions)

    def convert(self, data, key, value, ohlcAttributes={}):
        """
        Convert data to CandlestickBarChart format

        Example:
            >>> df.head(1)
                    Date  Adj_Close  Close   High     Low   Open Symbol    Volume      Timestamp
            0 2016-03-18      11.01  11.01  11.37  10.715  11.13    HDP  811100.0  1458259200000
            
            >>> cs = nv.candlestickBarChart()
            >>> ohlcAttributes = {"open":"Open" ,"high":"High" ,"low":"Low" ,"volume":"Volume" ,"adjusted":"Adj_Close"}
            >>> data = cs.convert(df, "Timestamp", "Close", ohlcAttributes)

            >>> config = {"color":nv.c20(), width":1400, "height":800,
                          "xAxis":{"tickFormat":"%d/%m/%Y", "axisLabel":"Date (d/m/y)"},
                          "yAxis":{"axisLabel": Close (USD)"}}

            >>> cs.plot({"data":data, "config":config})
            
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
        value : string
            Column name or dict key for values to used for the y axis
        ohlcAttributes : dict
            A dict of attributes: {"open":"Open" ,"high":"High" ,"low":"Low" ,"volume":"Volume" ,"adjusted":"Adj_Close"}
            The keys represent the value attribute for the plot, the value reprents the dict key or dataframe column to be used
            
        Returns
        -------
        dict
            The input data converted to the specific nvd3 chart format
        
        """
        df = data if isinstance(data, pd.DataFrame) else pd.DataFrame(data)

        ohlcAttributes["date"] = key
        ohlcAttributes["close"] = value       
        nvd3Data = df.rename(str, {v:k for k,v in ohlcAttributes.items()})[list(ohlcAttributes.keys())].to_dict("records")
        
        return [{"values": nvd3Data}]
