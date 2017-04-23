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


class HistoricalBarChart(Nvd3Chart):
    funcName = "historicalBarChart"
    funcBody = """
        function(session, object) {

            var chart = nv.models.historicalBarChart();
            chart.useInteractiveGuideline(true)
                 .showLegend(false)
                      
            chart.xAxis.showMaxMin(false)
                       .tickFormat(function(d) { return d3.time.format("%d.%m.%Y")(new Date(d)) })

            chart.yAxis.showMaxMin(true)
                       .tickFormat(d3.format(',.1f'))

            session.__functions.makeChart(session, object, chart);
        }        
    """

    def __init__(self, nvd3Functions):
        super(self.__class__, self).__init__(nvd3Functions)
        self.key = []
        self.value = []


    def plot(self, data, key, value, config={}):
        """
        Create a HistoricalBarChart
        
        Example:
            >>> df.head(1)
                    Date  Adj_Close  Close   High     Low   Open Symbol    Volume      Timestamp
            0 2016-03-18      11.01  11.01  11.37  10.715  11.13    HDP  811100.0  1458259200000
            
            >>> hb = nv.historicalBarChart()
            >>> hb = HistoricalBarChart(nv.nvd3Functions)

            >>> config = {"color":nv.c20()[4:]}
            >>> hb.plot(hdp, "Timestamp", "Volume", config=config)

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
        config : dict
            dict of nvd3 options 
            (use as keywork argument in the form config=myconfig)

        Returns
        -------
            None
        
        """        
        dataConfig = self.chart(data, key=key, value=value, config=config)    
        self._plot(dataConfig)
       
       
    def convert(self, data, key, value):
        self.key.append(key)
        self.value.append(key)

        df = data if isinstance(data, pd.DataFrame) else pd.DataFrame(data)
        
        nvd3Data = df.loc[:,[key, value]].rename(str, {key:"x", value:"y"}).to_dict("records")
        
        return {"data": [{"key": key, "values":nvd3Data}]}


    def append(self, data, chart=0): 
        dataConfig = self.chart(data, key=self.key[chart], value=self.value[chart], config=self.config[chart], chart=chart) 
        self._append(dataConfig, chart=chart)
