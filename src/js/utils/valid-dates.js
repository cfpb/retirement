'use strict';

var enforceRange = require( './enforce-range' );

/***-- validDates(month, day, year): makes sure the date given is valid, and changes it to
  something valid if it's not (guessing at user intent, a bit).
  parameters: month is numeric month (1-12), day is numeric day (1-31), year is numeric year
  ---**/
function validDates( month, day, year ) {
  // get parts of birthday and salary, strip non-numeric strings
  var monthMaxes = { '1': 31, '2': 28, '3': 31, '4': 30, '5': 31, '6': 30,
      '7': 31, '8': 31, '9': 30, '10': 31, '11': 30, '12': 31 };
  if ( new Date(year, 1, 29).getMonth() === 1 ) {
    monthMaxes['2'] = 29;
  }
  month = enforceRange( Number( month.toString().replace( /\D/g, '' ) ), 1, 12 );
  day = enforceRange( Number( day.toString().replace( /\D/g,'' ) ), 1, monthMaxes[ month.toString() ] );
  if ( Number(year) < 100 ) {
    year = Number(year) + 1900;
  }
  year = enforceRange( Number( year.toString().replace(/\D/g,'') ), 1900, new Date().getFullYear() );
  return { 'month': month, 'day': day, 'year': year, 'concat': month + '-' + day + '-' + year };
}

module.exports = validDates;