'use strict';

/***-- delay(): Delay a function ---**/
var delay = (function(){
  var t = 0;
  return function(callback, delay) {
    clearTimeout(t);
    t = setTimeout(callback, delay);
  };
})(); // end delay()

module.exports = delay;