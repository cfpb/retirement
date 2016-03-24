'use strict';


/***-- numToMoney(n): Convert from number to money string ---**/
function numToMoney(n) {
  var money;
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

module.exports = numToMoney;