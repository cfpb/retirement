'use strict';

var benefitsModel = require( '../models/benefits-model' );

var getModel = {
  benefits: function() {
    return benefitsModel.values;
  }
};

module.exports = getModel;
