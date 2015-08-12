

/***-- delay(): Delay a function ---**/
var delay = (function(){
  var t = 0;
  return function(callback, delay) {
    clearTimeout(t);
    t = setTimeout(callback, delay);
  };
})(); // end delay()

/***-- numToMoney(n): Convert from number to money string ---**/
function numToMoney(n) {
  // When n is a string, we should, ironically, strip its numbers first.
  if (typeof n === 'string') {
      n =  Number(n.replace(/[^0-9\.]+/g,""));
  }
  if ( typeof n === 'object' ) {
    n = 0;
  }
  var t = ",";
  if (n < 0) {
    var s = "-";
  }
  else {
    var s = "";
  }
  var i = parseInt(n = Math.abs(+n || 0).toFixed(0)) + "";
  var j = 0;
  if (i.length > 3) {
    j = ((i.length) % 3);
  }
  money = s + "$";
  if (j > 0) {
    money += i.substr(0,j) + t;
  }
  money += i.substr(j).replace(/(\d{3})(?=\d)/g, "$1" + t);
  return money;
}

/***-- calculateAge(month, day, year): Calculates an age based on inputs
  parameters: month is numeric month (1-12), day is numeric day (1-31), year is numeric year
  ---**/
function calculateAge( month, day, year ) {
  var now = new Date();
  var birthdate = new Date(year, Number(month) - 1, day);
  var age = now.getFullYear() - birthdate.getFullYear();
  var m = now.getMonth() - birthdate.getMonth();
  if ( m < 0 || ( m === 0 && now.getDate() < birthdate.getDate() ) ) {
    age--;
  }
  return age;
}

/***-- enforceRange(n, min, max): ensures ( min <= n <= max ) is true
  NOTE: If min or max is 'false' then that min or max is not enforced
  ---**/
function enforceRange(n, min, max) {
  if ( n > max && max !== false ) {
    n = max;
  }
  if ( n < min && min !== false ) {
    n = min;
  }
  return n;
}

/***-- validDates(month, day, year): makes sure the date given is valid, and changes it to
  something valid if it's not (guessing at user intent, a bit).
  parameters: month is numeric month (1-12), day is numeric day (1-31), year is numeric year
  ---**/
function validDates( month, day, year ) {
  // get parts of birthday and salary, strip non-numeric strings
  var monthMaxes = { '1': 31, '2': 29, '3': 31, '4': 30, '5': 31, '6': 30,
      '7': 31, '8': 31, '9': 30, '10': 31, '11': 30, '12': 31 };
  month = enforceRange( Number( month.toString().replace(/\D/g,'') ), 1, 12 );
  day = enforceRange( Number( day.toString().replace(/\D/g,'') ), 1, monthMaxes[ month.toString() ] );
  if ( Number(year) < 100 ) {
    year = Number(year) + 1900;
  }
  year = enforceRange( Number( year.toString().replace(/\D/g,'') ), 1900, new Date().getFullYear() );
  return { 'month': month, 'day': day, 'year': year, 'concat': month + '-' + day + '-' + year };
}

if ( typeof module === "object" ) {
  var functions = {
    numToMoney: numToMoney,
    calculateAge: calculateAge,
    enforceRange: enforceRange,
    validDates: validDates
  };
  
  module.exports = functions;  
}
