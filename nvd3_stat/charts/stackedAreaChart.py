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


class StackedAreaChart(Nvd3Chart):

    funcName = "stackedAreaChart"
    funcBody = """
        function(session, object) {

            var chart = nv.models.stackedAreaChart()
                .useInteractiveGuideline(true)
                .controlLabels({stacked: "Stacked"})

            chart.xAxis.showMaxMin(false)
                       .tickFormat(d3.format(',.1f'));
            chart.yAxis.showMaxMin(false)
                       .tickFormat(d3.format(',.1f'));

           session.__functions.makeChart(session, object, chart);
        }        
    """
    
    def __init__(self, nvd3Functions):
        super(self.__class__, self).__init__(nvd3Functions)
        self.key = []
        self.values = []

    def plot(self, data, key, values, config={}):
        """
        Create a StackedAreaChart

        Example:
            >>> x= np.linspace(0, 4*np.pi, 100)
                df = pd.DataFrame({"X":x*100, "Sin":np.sin(x), "Cos":np.cos(x), "ArcTan":np.arctan(x-2*np.pi)/3})
            
            >>> sa = nv.stackedAreaChart()
            >>> data = {"Series %d" % g: randomList(100, 4, 1) for g in range(5)}
            >>> seriesNames = list(data.keys())
            >>> data["Date"] = lastDays(count, ms=False)
            >>> sa_df = pd.DataFrame(data)
                
            >>> config={"xAxis":{"tickFormat":"%d/%m/%Y"},
                        "color": nv.c20(), "height":300}
                
            >>> data = sa.plot(sa_df, "Date", seriesNames, config=config)
            
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
            Column name or dict key for values to be used for the x axis
        values : list of strings
            Column names or dict keys for values to be used for the stacked areas
        config : dict
            dict of nvd3 options 
            (use as keywork argument in the form config=myconfig)

        Returns
        -------
            None
        """

        dataConfig = self.chart(data, key=key, values=values, config=config)    
        self._plot(dataConfig)


    def convert(self, data, key, values):
        self.key.append(key)
        self.values.append(values)

        df = data if isinstance(data, pd.DataFrame) else pd.DataFrame(data)
        
        nvd3Data = []
        for i in range(len(values)):
            line = {"key":values[i], "values":df.loc[:,[key, values[i]]].rename(str,{key:"x", values[i]:"y"}).to_dict("records")}
            nvd3Data.append(line)

        return {"data":nvd3Data}


    def append(self, data, chart=0): 
        dataConfig = self.chart(data, key=self.key[chart], values=self.values[chart], config=self.config[chart], chart=chart) 
        self._append(dataConfig, chart=chart)


