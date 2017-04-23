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


class BulletChart(Nvd3Chart):

    funcName = "bulletChart"
    funcBody = """
        function(session, object) {
            var chart = nv.models.bulletChart()

            session.__functions.makeChart(session, object, chart);
        }      
    """

    def __init__(self, nvd3Functions):
        super(self.__class__, self).__init__(nvd3Functions)
        self.title = []
        self.subtitle = []
        self.ranges = []
        self.measure = []
        self.markers = []
        self.markerLines = []


    def plot(self, title, subtitle, ranges, measure, markers, markerLines, config={}):
        """
        Create a BulletChart
        
        Example:
            >>> b = BulletChart(nv.nvd3Functions)

            >>> data = b.plot(title="Satisfaction", subtitle="out of 5",
                              ranges={'Bad':3.5, 'OK':4.25, 'Good':5},
                              measure={'Current':3.9},
                              markers={'Previous':3.8},
                              markerLines={'Threshold':3.0, 'Target':4.4}
                              config={})

        Parameters
        ----------
        title : string
            title of the bullet chart
        subtitle : string
            subtitle of the bullet chart
        ranges : dict
            Qualitative ranges in the form {"rangeName":maxValueOfRange, ...}
        markers : dict    
            Triangle markers in the form {"markerName":value, ...}
        markerLines : dict    
            Line markers in the form {"markerLineName":value, ...}
        measure : dict
            Actual value in the form {"actualValueName": value}
        config : dict
            dict of nvd3 options 
            (use as keywork argument in the form config=myconfig)

        Returns
        -------
            None
        
        """

        dataConfig = self.chart(title=title, subtitle=subtitle, ranges=ranges, measure=measure, 
                                markers=markers, markerLines=markerLines, config=config)    
        self._plot(dataConfig)


    def convert(self, title, subtitle, ranges, measure, markers, markerLines):
        self.title.append(title)
        self.subtitle.append(subtitle)
        self.ranges.append(ranges)
        self.measure.append(measure)
        self.markers.append(markers)
        self.markerLines.append(markerLines)

        data = {"title":title,
                "subtitle":subtitle,
                "ranges":list(ranges.values()),
                "rangeLabels":list(ranges.keys()),
                "measures":list(measure.values()),
                "measureLabels":list(measure.keys()),
                "markers":list(markers.values()),
                "markerLabels":list(markers.keys()),
                "markerLines":list(markerLines.values()),
                "markerLineLabels":list(markerLines.keys())}

        return {"data":data}
