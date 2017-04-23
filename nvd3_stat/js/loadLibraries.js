function(d3_version, nvd3_version, printSuccess, printError) {
  
  // Zeppelin tends to execute some calls twice ...
  if (typeof nvd3_stat.session.loadTime == "undefined") {
    var now = (new Date()).getTime();
    nvd3_stat.session.loadTime = now;
  } else {
    var now = (new Date()).getTime();
    if (now - nvd3_stat.session.loadTime < 1000) {
      console.log("loadLibraries already initiated")
      return
    }
  }

  window.nvd3_stat.promise = new Promise(function(resolve, reject) {

    // d3.js has to be mininimized: https://github.com/novus/nvd3/issues/1520
    var d3_js = "https://cdnjs.cloudflare.com/ajax/libs/d3/" + d3_version + "/d3.min.js";           
    var nvd3_css = "https://cdnjs.cloudflare.com/ajax/libs/nvd3/" + nvd3_version + "/nv.d3.min.css";
    var nvd3_js = "https://cdnjs.cloudflare.com/ajax/libs/nvd3/" + nvd3_version + "/nv.d3.min.js";
    var saveAsPng    = "https://rawgit.com/bernhard-42/saveSvgAsPng/gh-pages/saveSvgAsPng";
    var saveAsPng_js = saveAsPng + ".js";

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
      }).on("error", function() {
        printError("Could not load nv.d3.css");
        console.error("Could not load nv.d3.css");
        reject();
      }).on("load", function() {
        if (cssLoaded(href)) {
          printSuccess("successfully loaded nvd3 css");
          callback();
        }
      }).appendTo('head');
    }

    var loadJs = function() {
      $.getScript(d3_js)
        .done(function( script, textStatus ) {
          printSuccess("successfully loaded d3.js " + d3.version);
          $.getScript(nvd3_js)
            .done(function( script, textStatus ) {
              printSuccess("successfully loaded nv.d3.js " + nv.version);
              resolve();
              if (typeof requirejs === "function" ) {
                console.log("requirejs")
                requirejs.onError = function (err) {
                  if (err.requireType != "mismatch"){ // ignore first attempt
                    printError("Could not load " + saveAsPng_js + "</div>");
                    console.error("Could not load " + saveAsPng_js + "</div>");
                  }
                }
                require.config({ paths: {saveSvg: saveAsPng} });
                require(["saveSvg"], function(saveSvgAsPng) {
                  window.saveSvgAsPng = saveSvgAsPng.saveSvgAsPng;
                  window.saveSvg = saveSvgAsPng.saveSvg;
                  printSuccess("successfully loaded saveSvgAsPng");
                })
              } else {
                $.getScript(saveAsPng_js)
                  .done(function( script, textStatus ) {
                    printSuccess("successfully loaded saveSvgAsPng");
                  }).fail(function(jqxhr, settings, exception) { 
                    printError("Could not load " + saveAsPng_js + "</div>");
                    console.error("Could not load " + saveAsPng_js + "</div>");
                  }
                );
              }
            }).fail(function(jqxhr, settings, exception) { 
              printError("Could not load " + nvd3_js + "</div>"); 
              console.error("Could not load " + nvd3_js + "</div>"); 
              reject();
            }
          );
        }).fail(function(jqxhr, settings, exception) { 
          printError("Could not load " + d3_js + "</div>"); 
          console.error("Could not load " + d3_js + "</div>"); 
          reject();
        }
      );
    }

    if (cssLoaded(nvd3_css)) {
        loadJs();
    } else {
        loadCss(nvd3_css, loadJs);
    } 
  });
};

