var functions = require('../src/claiming-functions.js');

var chai = require('chai');
var expect = chai.expect;

describe( 'numToMoney...', function() {
  it( '...turn 5 into $5', function() {
    expect( functions.numToMoney( 5 )).to.equal( '$5' );
  });

  it( '...should turn -5 into -$5', function() {
    expect( functions.numToMoney( -5 )).to.equal( '-$5' );
  });

  it( '...should turn _undefined_ into $0', function() {
    expect( functions.numToMoney( undefined )).to.equal( '$0' );
  });

  it( '...should turn _undefined_ into $0', function() {
    expect( functions.numToMoney( undefined )).to.equal( '$0' );
  });

  it( '...should turn OBJECT into $0', function() {
    expect( functions.numToMoney( { 'testObject': true } )).to.equal( '$0' );
  });

});

describe( 'calculateAge...', function() {
  var now = new Date('January 1, 2015 01:23:00');

  it( '...should return 65 if birthday is 1/1/1950 and today is 1/1/2015', function() {
    expect( functions.calculateAge( 1, 1, 1950, now ) ).to.equal( 65 );
  });

  it( '...should return 64 if birthday is 1/2/1950 and today is 1/1/2015', function() {
    expect( functions.calculateAge( 1, 2, 1950, now ) ).to.equal( 64 );
  });

  it( '...should return false on any NaN age result', function() {
    expect( functions.calculateAge( 'a', 2, 1950, now ) ).to.equal( false );
    expect( functions.calculateAge( 1, 2, [ 3, 4, 5 ], now ) ).to.equal( false );
    expect( functions.calculateAge( 1, 2, 999999, now ) ).to.equal( false );
  });

});

describe( 'enforceRange...', function() {
  it( '...should enforce maximums', function() {
    expect( functions.enforceRange( 15, 1, 10 ) ).to.equal( 10 );
    expect( functions.enforceRange( 150, 1, 100 ) ).to.equal( 100 );
    expect( functions.enforceRange( 4, 2, 3 ) ).to.equal( 3 );
  });

  it( '...should enforce minimums', function() {
    expect( functions.enforceRange( 5, 10, 15 ) ).to.equal( 10 );
    expect( functions.enforceRange( 3, 5, 100 ) ).to.equal( 5 );
    expect( functions.enforceRange( 1, 2, 3 ) ).to.equal( 2 );
  });

  it( '...should allow numbers within the range', function() {
    expect( functions.enforceRange( 5, 1, 10 ) ).to.equal( 5 );
    expect( functions.enforceRange( 155, 100, 1000 ) ).to.equal( 155 );
    expect( functions.enforceRange( 1, 1, 10 ) ).to.equal( 1 );
    expect( functions.enforceRange( 10, 1, 10 ) ).to.equal( 10 );
  });

  it( '...should return false if min is greater than max', function() {
    expect( functions.enforceRange( 15, 20, 10 ) ).to.equal( false );
  });

  it( '...should return false if types are mixed', function() {
    expect( functions.enforceRange( 1, 'a', 'c' ) ).to.equal( false );
  });

  it( '...should work on strings', function() {
    expect( functions.enforceRange( 'd', 'a', 'c' ) ).to.equal( 'c' );
    expect( functions.enforceRange( 'cat', 'bar', 'foo' ) ).to.equal( 'cat' );
    expect( functions.enforceRange( 'lion', 'bar', 'foo' ) ).to.equal( 'foo' );
  });
});

describe( 'validDates...', function() {
  it( '...should enforce date range by month', function() {
    expect( functions.validDates( 10, 36, 2015 )['concat'] ).to.equal( '10-31-2015' );
    expect( functions.validDates( 10, 0, 2015 )['concat'] ).to.equal( '10-1-2015' );
    expect( functions.validDates( 2, 31, 2015 )['concat'] ).to.equal( '2-28-2015' );
    expect( functions.validDates( 4, 31, 2015 )['concat'] ).to.equal( '4-30-2015' );
    expect( functions.validDates( 6, 31, 2015 )['concat'] ).to.equal( '6-30-2015' );
    expect( functions.validDates( 9, 31, 2015 )['concat'] ).to.equal( '9-30-2015' );
  });

  it( '...should enforce months between 1 and 12', function() {
    expect( functions.validDates( 13, 31, 2015 )['concat'] ).to.equal( '12-31-2015' );
    expect( functions.validDates( 0, 31, 2015 )['concat'] ).to.equal( '1-31-2015' );
  });

  it( '...should change two-digit years to be 19XX', function() {
    expect( functions.validDates( 13, 31, 55 )['concat'] ).to.equal( '12-31-1955' );
    expect( functions.validDates( 0, 31, 00 )['concat'] ).to.equal( '1-31-1900' );
  });

  it( '...should understand leap years', function() {
    expect( functions.validDates( 2, 29, 2004 )['concat'] ).to.equal( '2-29-2004' );
    expect( functions.validDates( 2, 29, 2003 )['concat'] ).to.equal( '2-28-2003' );
  });
});