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



def loadNVD3(nvd3version="1.8.2", d3version="3.5.17"):

    js = """
    var d3_js = "https://cdnjs.cloudflare.com/ajax/libs/d3/%s/d3";
    var nvd3_css = "https://cdnjs.cloudflare.com/ajax/libs/nvd3/%s/nv.d3.css";
    var nvd3_js = "https://cdnjs.cloudflare.com/ajax/libs/nvd3/%s/nv.d3.js";
    var saveAsPng_js = "https://rawgit.com/bernhard-42/saveSvgAsPng/gh-pages/saveSvgAsPng";

    var cssLoaded = function(href) {
        var found = false;
        for (var i in document.styleSheets) {
            if (document.styleSheets[i].href == href ) {
                found = true;
                break;
            }
        }   
        return found;
    }

    var loadCss = function(href, callback) {
       $('<link/>', {
            rel: 'stylesheet',
            type: 'text/css',
            crossOrigin: 'anonymous',
            href: href
        }).error(function() {
            element.html("<div style='color:red'>Error: loading nv.d3.css</div>");
        }).load(function() {
            if (cssLoaded(href)) {
                element.append("<div>loaded nvd3 css</div>");
                loadJs();
            }
        }).appendTo('head');
    }

    var loadJs = function() {
        require.config({ paths: {d3: d3_js, saveSvg: saveAsPng_js} });
        require(["d3"], function(d3) {
            window.d3 = d3;
            element.append("<div>loaded d3 js " + d3.version + "</div>", window.d3)
            $.getScript(nvd3_js)
             .done(function( script, textStatus ) {
                element.append("<div>loaded nvd3.js " + nv.version + "</div>", window.nv)
                require(["saveSvg"], function(saveSvgAsPng) {
                    window.saveSvgAsPng = saveSvgAsPng.saveSvgAsPng
                    window.saveSvg = saveSvgAsPng.saveSvg
                    window.__saveSvgAsPng = saveSvgAsPng;
                    element.append("<div>loaded saveSvgAsPng</div>");
                })
             }).fail(function(jqxhr, settings, exception){
                element.html("<div style='color:red'>Error: loading nv.d3.js</div>");
             })
        });
    }

    if (cssLoaded(nvd3_css)) {
        loadJs();
    } else {
        loadCss(nvd3_css, loadJs);
    } 
    """ % (d3version, nvd3version, nvd3version)
    
    display_javascript(Javascript(js))
