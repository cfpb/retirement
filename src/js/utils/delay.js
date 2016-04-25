'use strict';

/**
 * This function can be used to call another function with a delay.
 */
var delay = ( function() {
  var t = 0;
  return function( callback, time ) {
    clearTimeout( t );
    t = setTimeout( callback, time );
  };
} )();

module.exports = delay;
