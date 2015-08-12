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

describe( 'enforceRange...', function() {
  it( '...should turn 15 into 10 if the upper limit is 10', function() {
    expect( functions.enforceRange( 15, 1, 10 )).to.equal( 10 );
  });


});