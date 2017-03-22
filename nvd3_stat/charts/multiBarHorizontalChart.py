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


class MultiBarHorizontalChart(Nvd3Chart):

    funcName = "multiBarHorizontalChart"
    funcBody = """
        function(session, object) {

            var chart = nv.models.multiBarHorizontalChart()
                .margin({bottom: 50, left: 50})
                .stacked(false);
                
            chart.xAxis.showMaxMin(false)
                       .tickFormat(d3.format(',.1f'))

            chart.yAxis.showMaxMin(false)
                       .tickFormat(d3.format(',.1f'))
              
           session.__functions.makeChart(session, object, chart);
        }        
    """
    
    def __init__(self, nvd3Functions):
        super(self.__class__, self).__init__(nvd3Functions)

    def convert(self, data, key, values):
        """
        Convert data to MultiBarHorizontalChart format
        Example:
            >>> x = np.linspace(0, 4*np.pi, 10)
                df = pd.DataFrame({"X":x*100, "Sin":np.sin(x), "Cos":np.cos(x), "ArcTan":np.arctan(x-2*np.pi)/3})
            
            >>> mbh = nv.multiBarHorizontalChart()

            >>> data = mbh.convert(l1_df, "X", ["Sin", "Cos", "ArcTan"], keyAttributes)
                
            >>> config={"height":400, "width": 1000,
                        "focusEnable": False, "color":nv.c10()[::2], 
                        "yAxis": {"axisLabel":"F(X)", "tickFormat":",.1f"}, 
                        "xAxis":{"axisLabel":"X", "tickFormat":",.1f"}}
                        
            >>> mbh.plot({"data":data, "config":config})
            
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
            Column names or dict keys for values to be used for the bars

        Returns
        -------
        dict
            The input data converted to the specific nvd3 chart format
        """

        df = data if isinstance(data, pd.DataFrame) else pd.DataFrame(data)

        nvd3Data = []
        for i in range(len(values)):
            nvd3Data.append({"key":values[i], "values":df.loc[:,[key, values[i]]].rename(str,{key:"x", values[i]:"y"}).to_dict("records")})

        return nvd3Data 
