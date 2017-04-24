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
from .nvd3_chart import Nvd3Chart

from .charts.boxPlotChart             import BoxPlotChart
from .charts.discreteBarChart         import DiscreteBarChart
from .charts.multiBarChart            import MultiBarChart
from .charts.multiBarHorizontalChart  import MultiBarHorizontalChart
from .charts.lineChart                import LineChart
from .charts.linePlusBarChart         import LinePlusBarChart
from .charts.scatterPlusLineChart     import ScatterPlusLineChart
from .charts.stackedAreaChart         import StackedAreaChart
from .charts.pieChart                 import PieChart
from .charts.sunBurstChart            import SunBurstChart
from .charts.parallelCoordinatesChart import ParallelCoordinatesChart
from .charts.historicalBarChart       import HistoricalBarChart
from .charts.candlestickBarChart      import CandlestickBarChart
from .charts.ohlcBarChart             import OhlcBarChart
from .charts.bulletChart              import BulletChart


class Nvd3(object):
    
    def __init__(self, downloadAsPng=True):
        self.nvd3Functions = Nvd3Functions()


    def reloadNVD3(self, nvd3version="1.8.5", d3version="3.5.17"):
        self.nvd3Functions.reloadNVD3(nvd3version, d3version)
   
    def enableStreaming(self):
        self.nvd3Functions.enableStreaming()
        
    def traceJs(self, on=True):
        self.nvd3Functions.traceJs(on)
        

    def createDataConfig(self, data, config={}):
        return ({"data":data, "config":config})


    def boxPlotChart(self):
        return BoxPlotChart(self.nvd3Functions)

    def discreteBarChart(self):
        return DiscreteBarChart(self.nvd3Functions)

    def multiBarChart(self):
        return MultiBarChart(self.nvd3Functions)

    def multiBarHorizontalChart(self):
        return MultiBarHorizontalChart(self.nvd3Functions)

    def lineChart(self):
        return LineChart(self.nvd3Functions)

    def linePlusBarChart(self):
        return LinePlusBarChart(self.nvd3Functions)

    def scatterPlusLineChart(self):
        return ScatterPlusLineChart(self.nvd3Functions)

    def stackedAreaChart(self):
        return StackedAreaChart(self.nvd3Functions)

    def pieChart(self):
        return PieChart(self.nvd3Functions)

    def sunBurstChart(self):
        return SunBurstChart(self.nvd3Functions)

    def parallelCoordinatesChart(self):
        return ParallelCoordinatesChart(self.nvd3Functions)

    def ohlcBarChart(self):
        return OhlcBarChart(self.nvd3Functions)

    def candlestickBarChart(self):
        return CandlestickBarChart(self.nvd3Functions)

    def historicalBarChart(self):
        return HistoricalBarChart(self.nvd3Functions)

    def bulletChart(self):
        return BulletChart(self.nvd3Functions)


    def _slice(self, colors, args):
        if len(args) == 0:
            return colors
        else:
            return [colors[i%len(colors)] for i in args]
        
    # Source: http://d3js.org
    def c10(self, *args):
        colors = ["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd", "#8c564b", "#e377c2", "#7f7f7f", "#bcbd22", "#17becf"]
        return self._slice(colors, args)

    # Source: http://d3js.org
    def c20(self, *args):
        colors = ["#1f77b4", "#aec7e8", "#ff7f0e", "#ffbb78", "#2ca02c", "#98df8a", "#d62728", "#ff9896", "#9467bd", "#c5b0d5", 
                "#8c564b", "#c49c94", "#e377c2", "#f7b6d2", "#7f7f7f", "#c7c7c7", "#bcbd22", "#dbdb8d", "#17becf", "#9edae5"]
        return self._slice(colors, args)

    # Source: http://d3js.org
    def c20b(self, *args):
        colors = ["#393b79", "#5254a3", "#6b6ecf", "#9c9ede", "#637939", "#8ca252", "#b5cf6b", "#cedb9c", "#8c6d31", "#bd9e39", 
                "#e7ba52", "#e7cb94", "#843c39", "#ad494a", "#d6616b", "#e7969c", "#7b4173", "#a55194", "#ce6dbd", "#de9ed6"]
        return self._slice(colors, args)

    # Source: http://d3js.org
    def c20c(self, *args):
        colors = ["#3182bd", "#6baed6", "#9ecae1", "#c6dbef", "#e6550d", "#fd8d3c", "#fdae6b", "#fdd0a2", "#31a354", "#74c476", 
                "#a1d99b", "#c7e9c0", "#756bb1", "#9e9ac8", "#bcbddc", "#dadaeb", "#636363", "#969696", "#bdbdbd", "#d9d9d9"]
        return self._slice(colors, args)

    def grey(self):
        digits = ["0","1","2","3","4","5","6","7","8","9","a","b","c","d","e","f"]
        colors = ["#%s" % (d*3) for d in digits]
        return self._slice(colors, args)
