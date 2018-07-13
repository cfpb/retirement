
const chai = require('chai');
const expect = require('chai').expect;

const numToMoney = require( '../src/js/utils/num-to-money' );
const enforceRange = require( '../src/js/utils/enforce-range' );
const validDates = require( '../src/js/utils/valid-dates' );
const handleStringInput = require( '../src/js/utils/handle-string-input' );


describe( 'numToMoney...', function() {
  it( '...turn 5000000 into $5,000,000', function() {
    expect( numToMoney( 5000000 )).to.equal( '$5,000,000' );
  });

  it( '...should turn -5000000 into -$5,000,000', function() {
    expect( numToMoney( -5000000 )).to.equal( '-$5,000,000' );
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
    expect( validDates( 0, 31, 0 )['concat'] ).to.equal( '1-31-1900' );
  });

  it( '...should understand leap years', function() {
    expect( validDates( 2, 29, 2004 )['concat'] ).to.equal( '2-29-2004' );
    expect( validDates( 2, 29, 2003 )['concat'] ).to.equal( '2-28-2003' );
  });
});


describe( 'handleStringInput...', function() {

  it( '...will parse number strings with non-numeric characters', function() {
    expect( handleStringInput( '9a99' ) ).to.equal( 999 );
    expect( handleStringInput( 'u123456' ) ).to.equal( 123456 );
    expect( handleStringInput( '01234' ) ).to.equal( 1234 );
    expect( handleStringInput( '$1,234,567' ) ).to.equal( 1234567 );
    expect( handleStringInput( 'Ilikethenumber5' ) ).to.equal( 5 );
    expect( handleStringInput( 'function somefunction() { do badstuff; }' ) ).to.equal( 0 );
  });

  it( '...will parse the first period as a decimal point', function() {
    expect( handleStringInput( '4.22' ) ).to.equal( 4.22 );
    expect( handleStringInput( 'I.like.the.number.5' ) ).to.equal( 0.5 );
    expect( handleStringInput( '1.2.3.4.5.6.7' ) ).to.equal( 1.234567 );
  });

});
