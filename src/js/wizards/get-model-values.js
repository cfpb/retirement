'use strict';

var benefitsModel = require( '../models/benefits-model' );
var lifetimeModel = require( '../models/lifetime-model' );

var getModel = {
  benefits: function() {
    return benefitsModel.values;
  },
  lifetime: function() {
    return lifetimeModel.values;
  }
};

module.exports = getModel;
