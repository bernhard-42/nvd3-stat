
// after refresh window wait for max 5 seconds until Jupyter notebook is initialized

var counter = 0;
var timer = setInterval(function(){
  if (typeof Jupyter != "undefined" && 
    typeof Jupyter.notebook != "unfdefined" && 
    typeof Jupyter.notebook.kernel != "undefined" && 
    Jupyter.notebook.kernel.is_connected() &&                    
    typeof Jupyter.notebook.kernel.comm_manager != "undefined") {

    console.log("NVD3-Stat [INFO] registering Jupyter comms target");
    Jupyter.notebook.kernel.comm_manager.register_target("nvd3_stat", 
      function(comm, msg) {
        if (window.__nvd3_stat_debug > 1) {
          console.log("NVD3-Stat [DEBUG] Comm for nvd3_stat opened");
        }

        comm.on_msg(function(msg) {
          var funcName = msg.content.data.funcName;
          var plotId = msg.content.data.args.plotId;
          var args = msg.content.data.args;
          if (window.__nvd3_stat_debug > 1) {
            console.log("NVD3-Stat [DEBUG]", funcName, args)
          }
          window.nvd3_stat.session[funcName](window.nvd3_stat.session, args);
        });

        comm.on_close(function(msg) {
          console.log("NVD3-Stat [INFO] comm for nvd3_stat closed ", msg);         
        });    
      }    
    )

    clearInterval(timer)
  } else {
    counter++;
    if (counter === 50) {
      console.log("Registering comms target failed")
      clearInterval(timer)            
    }
  }
}, 100)
