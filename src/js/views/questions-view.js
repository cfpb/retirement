'use strict';

var questionsView = {

  init: function() {
    var $buttons = $( '.step-two .question .lifestyle-btn' );

    $buttons.click(function() {
      var $container = $(this).closest( '.question' );
      var respTo = $(this).val();
      $container.find( '.lifestyle-btn' ).removeClass( 'lifestyle-btn__active' );
      $(this).addClass( 'lifestyle-btn__active' );

      $container.find( '.lifestyle-img' ).slideUp();
      $container.find( '.lifestyle-response' ).not( '[data-responds-to="' + respTo + '"]' ).slideUp();
      $container.find( '.lifestyle-response[data-responds-to="' + respTo + '"]' ).slideDown();

      $container.attr( 'data-answered', 'yes' );

    } );
  },

  /*
   * This function updates the text in the "questions" in Part 2
   * based on the user's current age
   * @param {number} currentAge   The user's current age
   */
  update: function( currentAge ) {
    var $ageSplits = $( '.lifestyle-btn.age-split' );
    if ( currentAge < 50 ) {
      $ageSplits.each( function() {
        $(this).val( $(this).attr( 'data-base-value' ) + '-under50' );
      });
    } else {
      $ageSplits.each( function() {
        $(this).val( $(this).attr( 'data-base-value' ) + '-over50' );
      });
    }
  }

};

module.exports = questionsView;
