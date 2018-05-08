/* bundleLogger
   ------------
   Provides gulp style logs to the bundle method in browserify.js
*/

const ansiColors = require( 'ansi-colors' );
const fancyLog = require( 'fancy-log' );
const prettyHrtime = require( 'pretty-hrtime' );

let startTime;

module.exports = {
  start: function( filepath ) {
    startTime = process.hrtime();
    fancyLog(
      'Bundling',
      ansiColors.green( filepath ) + '...'
    );
  },
  watch: function( bundleName ) {
    fancyLog(
      'Watching files required by',
      ansiColors.yellow( bundleName )
    );
  },
  end: function( filepath ) {
    const taskTime = process.hrtime( startTime );
    const prettyTime = prettyHrtime( taskTime );
    fancyLog(
      'Bundled',
      ansiColors.green( filepath ),
      'in', ansiColors.magenta( prettyTime )
    );
  }
};
