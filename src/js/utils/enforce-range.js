'use strict';

/***-- enforceRange(n, min, max): ensures ( min <= n <= max ) is true
  NOTE: If min or max is 'false' then that min or max is not enforced
  ---**/
function enforceRange(n, min, max) {
  if ( max < min || typeof n !== typeof min ) {
    return false;
  }
  if ( n > max && max !== false ) {
    n = max;
  }
  if ( n < min && min !== false ) {
    n = min;
  }
  return n;
}

module.exports = enforceRange;