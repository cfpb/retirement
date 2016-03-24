
var chai = require('chai');
var expect = require('chai').expect;

var numToMoney = require( '../src/js/utils/num-to-money' );
var calculateAge = require( '../src/js/utils/calculate-age' );
var enforceRange = require( '../src/js/utils/enforce-range' );
var validDates = require( '../src/js/utils/valid-dates' );


describe( 'numToMoney...', function() {
  it( '...turn 5 into $5', function() {
    expect( numToMoney( 5 )).to.equal( '$5' );
  });

  it( '...should turn -5 into -$5', function() {
    expect( numToMoney( -5 )).to.equal( '-$5' );
  });

  it( '...should turn _undefined_ into $0', function() {
    expect( numToMoney( undefined )).to.equal( '$0' );
  });

  it( '...should turn _undefined_ into $0', function() {
    expect( numToMoney( undefined )).to.equal( '$0' );
  });

  it( '...should turn OBJECT into $0', function() {
    expect( numToMoney( { 'testObject': true } )).to.equal( '$0' );
  });

});

describe( 'calculateAge...', function() {
  var now = new Date('January 1, 2015 01:23:00');

  it( '...should return 65 if birthday is 1/1/1950 and today is 1/1/2015', function() {
    expect( calculateAge( 1, 1, 1950, now ) ).to.equal( 65 );
  });

  it( '...should return 64 if birthday is 1/2/1950 and today is 1/1/2015', function() {
    expect( calculateAge( 1, 2, 1950, now ) ).to.equal( 64 );
  });

  it( '...should return false on any NaN age result', function() {
    expect( calculateAge( 'a', 2, 1950, now ) ).to.equal( false );
    expect( calculateAge( 1, 2, [ 3, 4, 5 ], now ) ).to.equal( false );
    expect( calculateAge( 1, 2, 999999, now ) ).to.equal( false );
  });

});

describe( 'enforceRange...', function() {
  it( '...should enforce maximums', function() {
    expect( enforceRange( 15, 1, 10 ) ).to.equal( 10 );
    expect( enforceRange( 150, 1, 100 ) ).to.equal( 100 );
    expect( enforceRange( 4, 2, 3 ) ).to.equal( 3 );
  });

  it( '...should enforce minimums', function() {
    expect( enforceRange( 5, 10, 15 ) ).to.equal( 10 );
    expect( enforceRange( 3, 5, 100 ) ).to.equal( 5 );
    expect( enforceRange( 1, 2, 3 ) ).to.equal( 2 );
  });

  it( '...should allow numbers within the range', function() {
    expect( enforceRange( 5, 1, 10 ) ).to.equal( 5 );
    expect( enforceRange( 155, 100, 1000 ) ).to.equal( 155 );
    expect( enforceRange( 1, 1, 10 ) ).to.equal( 1 );
    expect( enforceRange( 10, 1, 10 ) ).to.equal( 10 );
  });

  it( '...should return false if min is greater than max', function() {
    expect( enforceRange( 15, 20, 10 ) ).to.equal( false );
  });

  it( '...should return false if types are mixed', function() {
    expect( enforceRange( 1, 'a', 'c' ) ).to.equal( false );
  });

  it( '...should work on strings', function() {
    expect( enforceRange( 'd', 'a', 'c' ) ).to.equal( 'c' );
    expect( enforceRange( 'cat', 'bar', 'foo' ) ).to.equal( 'cat' );
    expect( enforceRange( 'lion', 'bar', 'foo' ) ).to.equal( 'foo' );
  });
});

describe( 'validDates...', function() {
  it( '...should enforce date range by month', function() {
    expect( validDates( 10, 36, 2015 )['concat'] ).to.equal( '10-31-2015' );
    expect( validDates( 10, 0, 2015 )['concat'] ).to.equal( '10-1-2015' );
    expect( validDates( 2, 31, 2015 )['concat'] ).to.equal( '2-28-2015' );
    expect( validDates( 4, 31, 2015 )['concat'] ).to.equal( '4-30-2015' );
    expect( validDates( 6, 31, 2015 )['concat'] ).to.equal( '6-30-2015' );
    expect( validDates( 9, 31, 2015 )['concat'] ).to.equal( '9-30-2015' );
  });

  it( '...should enforce months between 1 and 12', function() {
    expect( validDates( 13, 31, 2015 )['concat'] ).to.equal( '12-31-2015' );
    expect( validDates( 0, 31, 2015 )['concat'] ).to.equal( '1-31-2015' );
  });

  it( '...should change two-digit years to be 19XX', function() {
    expect( validDates( 13, 31, 55 )['concat'] ).to.equal( '12-31-1955' );
    expect( validDates( 0, 31, 00 )['concat'] ).to.equal( '1-31-1900' );
  });

  it( '...should understand leap years', function() {
    expect( validDates( 2, 29, 2004 )['concat'] ).to.equal( '2-29-2004' );
    expect( validDates( 2, 29, 2003 )['concat'] ).to.equal( '2-28-2003' );
  });
});


/**
 * Testing functions in claiming-graph.js
 */

// describe( 'moveIndicatorToAge...', function() {
//   it( '...should prevent you from selecting an age less than your current age', function() {
//     expect( graph.moveIndicatorToAge( 63, 64 ) ).to.equal( false );
//     expect( graph.moveIndicatorToAge( 66, 69 ) ).to.equal( false );
//   });
// });
