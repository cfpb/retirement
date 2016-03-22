'use strict';

/***-- calculateAge(month, day, year): Calculates an age based on inputs
  parameters: month is numeric month (1-12), day is numeric day (1-31), year is numeric year,
              currentDate is an optional Date
  ---**/
function calculateAge( month, day, year, currentDate ) {
  var now = currentDate;
  if ( currentDate instanceof Date !== true  ) {
    now = new Date();
  }
  var birthdate = new Date(year, Number(month) - 1, day);
  var age = now.getFullYear() - birthdate.getFullYear();
  var m = now.getMonth() - birthdate.getMonth();
  if ( m < 0 || ( m === 0 && now.getDate() < birthdate.getDate() ) ) {
    age--;
  }
  if ( isNaN( age ) ) {
    return false;
  }
  return age;
}

module.exports = calculateAge;