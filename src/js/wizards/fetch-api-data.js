'use strict';

var update = require( './update-model' );

var fetch = {
  apiData: function( birthdate, salary, dataLang ) {
    var url;
    if ( dataLang === 'es' ) {
      url = '/retirement/retirement-api/estimator/' + birthdate + '/' + Number(salary) + '/es/';
    } else {
      url = '/retirement/retirement-api/estimator/' + birthdate + '/' + Number(salary) + '/';
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
