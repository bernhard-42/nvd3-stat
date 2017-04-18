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

import time

def HTML(text):
    return "%%html\n%s" % text

def Javascript(script):
    return "%%html\n<script>%s</script>" % script

def display_html(html):
    print(html)

def display_javascript(js):
    print(js)

def loadNVD3(nvd3version="1.8.5", d3version="3.5.17"):
    html = """
        <link href="https://cdnjs.cloudflare.com/ajax/libs/nvd3/%s/nv.d3.min.css" rel="stylesheet" crossOrigin:"anonymous">
    """ % (d3version, nvd3version, nvd3version)
    display_html(HTML(html))

    time.sleep(0.5)
    
    js = """
      console.log("successfully loaded nv.d3.css %s");
      jQuery.getScript("https://cdnjs.cloudflare.com/ajax/libs/d3/%s/d3.min.js", function( data, textStatus, jqxhr ) {
        if (textStatus == "success") {
          console.log("successfully loaded d3.js %s");
          jQuery.getScript("https://cdnjs.cloudflare.com/ajax/libs/nvd3/%s/nv.d3.min.js", function( data, textStatus, jqxhr ) {
            if (textStatus == "success") {
              console.log("successfully loaded nv.d3,js %s");
              jQuery.getScript("http://cdn.rawgit.com/exupero/saveSvgAsPng/gh-pages/saveSvgAsPng.js", function( data, textStatus, jqxhr ) {
                if (textStatus == "success") {
                  console.log("successfully loaded saveSvgAsPng");
                }
              })
            }
          })
        }
      })                    
    """
    display_javascript(Javascript(js))
