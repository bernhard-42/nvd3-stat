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


class DiscreteBarChart(Nvd3Chart):
    
    funcName = "discreteBarChart"
    funcBody = """
        function(session, object) {
            var chart = nv.models.discreteBarChart()
                .staggerLabels(true)
                .showValues(true)
                .showLegend(false)
                .margin({top:30})

            session.__functions.makeChart(session, object, chart);
        }        
    """

    def __init__(self, nvd3Functions):
        super(self.__class__, self).__init__(nvd3Functions)

    def convert(self, data, key, value):
        """
        Convert data to DiscreteBarChart format
        
        Example:
            >>> df.head(3)
                     Series       Mean
                0  Series A  10.709464
                1  Series B   5.073523
                2  Series C   2.852349
                
            >>> db = nv.discreteBarChart()

            >>> config={"height": 350, "width": 500, "color": nv.c20(), "yDomain":[0,12]}
            >>> data = db.convert(df, key="Series", value="Mean")
                
            >>> db.plot({"data":data, "config":config})

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
            Name of column holding value names
        value : string
            Name of column holding the values

        Returns
        -------
        dict
            The input data converted to the specific nvd3 chart format        
        """
        
        df = data if isinstance(data, pd.DataFrame) else pd.DataFrame(data)
        
        nvd3Data = df.loc[:,[key, value]].rename(str, {key:"x", value:"y"}).to_dict("records")

        return [{"key":key, "values":nvd3Data}] 

