'use strict';

var benefitsModel = require( '../models/benefits-model' );

var update = {

  benefits: function( prop, val ) {
    benefitsModel.values[ prop ] = val;
  },

  processApiData: function( resp ) {
    var data = resp.data,
        fullAge = Number( data['full retirement age'].substr(0,2) );
    if ( resp.currentAge > fullAge ) {
      fullAge = resp.currentAge;
    }
    $.each( resp.data.benefits, function(i, val) {
      if ( i.substr(0,3) === 'age' ) {
        var prop = i.replace( ' ', '' );
        update.benefits( prop, val );
      }
    });
    update.benefits( 'currentAge', resp.current_age );
    update.benefits( 'past_fra', resp.past_fra );
    update.benefits( 'fullRetirementAge', data['full retirement age'] );
    update.benefits( 'earlyRetirementAge', data['early retirement age'] );
    update.benefits( 'fullAge', fullAge );
    update.benefits( 'earlyAge', Number( data['early retirement age'].substr(0,2) ) );
    update.benefits( 'monthsPastBirthday', Number( data['months_past_birthday'] ) );
  }

};

module.exports = update;
