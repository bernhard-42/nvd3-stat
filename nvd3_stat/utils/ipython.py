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

from IPython.display import Javascript, display_javascript, HTML, display_html
import json


class IPythonSession(object):

    def __init__(self):
        js = """
            window.Nvd3py = function() {};
            window.nvd3py = new window.Nvd3py();
            window.nvd3py.session = {};
            window.nvd3py.session.__functions = {};
            """
        display_javascript(Javascript(js))

        css = """
        <style>
        div.output_area img, div.output_area svg {
            max-width: 100%;
            height: 100%;
        }
        </style>
        """
        display_html(HTML(css))
            

    def registerFunction(self, funcName, func):
        js = """
        window.Nvd3py.prototype.%s;
        window.nvd3py.session.__functions.%s = window.nvd3py.%s;
        """ % (func, funcName, funcName)
        display_javascript(Javascript(js))


    def call(aself, funcName, args, delay):
        payload = json.dumps(args)
        display_javascript(Javascript("window.nvd3py." + funcName + "(window.nvd3py.session, " + payload + ")"))



def loadNVD3(nvd3version="1.8.5", d3version="3.5.17"):

    js = """
    require.config({ paths: {d3:      "http://d3js.org/d3.v3.min",
                             saveSvg: "http://cdn.rawgit.com/exupero/saveSvgAsPng/gh-pages/saveSvgAsPng"} });
    require(["d3"], function(d3) {
        window.d3 = d3;
        console.log("loaded d3", window.d3)

        require(["saveSvg"], function(saveSvgAsPng) {
            window.saveSvgAsPng = saveSvgAsPng.saveSvgAsPng
            console.log("loaded saveSvgAsPng", window.saveSvgAsPng);

            $.getScript("https://cdnjs.cloudflare.com/ajax/libs/nvd3/1.8.5/nv.d3.js", function() {
                $('<link/>', {
                   rel: 'stylesheet',
                   type: 'text/css',
                   href: 'https://cdnjs.cloudflare.com/ajax/libs/nvd3/1.8.5/nv.d3.css'
                }).appendTo('head');
                console.log("loaded nvd3", window.nv)
            })
        })
    });
    """

    display_javascript(Javascript(js))
