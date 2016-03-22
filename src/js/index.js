'use strict';

require( './utils/nemo' );
require( './utils/nemo-shim' );
var claimingPage = require( './claiming-graph');

var app = {
  init: function() {
    claimingPage.init();

  }
};

$( document ).ready( function() {
  app.init();
} );
