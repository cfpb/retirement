'use strict';

var validDates = require( '../utils/valid-dates' );
var update = require( './update-model' );

var fetch = {
  apiData: function( birthdate, salary, dataLang ) {
    if ( dataLang === 'es' ) {
      var url = '/retirement/retirement-api/estimator/' + birthdate + '/' + Number(salary) + '/es/';
    } else {
      var url = '/retirement/retirement-api/estimator/' + birthdate + '/' + Number(salary) + '/';
    }

    var apiDataRequest = $.ajax( {
      url: url,
      dataType: 'json',
      success: function( resp ) {
        if ( resp.error === '' ) {
          update.processApiData( resp );
        }
        return resp;
      },
      error: function( req, status, err ) {

      }

    } );

    return apiDataRequest;
  }
};

module.exports = fetch;