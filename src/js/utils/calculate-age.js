'use strict';

/**
 * This function calculates an age based on inputs
 * @param {number} month Month (1-12) of birth
 * @param {number} day Day (1-31) of birth
 * @param {number} year Year of birth
 * @param {date} currentDate optional current date to be used instead of
 * the current date
 * @returns {number} age 
 */
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