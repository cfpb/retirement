'use strict';

var questionsView = {

  init: function() {
    var $buttons = $( '.step-two .question .lifestyle-btn' );

    $buttons.click( function() {
      var $container = $( this ).closest( '.question' ),
          respTo = $( this ).val(),
          selector;
      $container.find( '.lifestyle-btn' )
        .removeClass( 'lifestyle-btn__active' );
      $( this ).addClass( 'lifestyle-btn__active' );

      $container.find( '.lifestyle-img' ).slideUp();
      $container.find( '.lifestyle-response' )
        .not( '[data-responds-to="' + respTo + '"]' ).slideUp();
      selector = '.lifestyle-response[data-responds-to="' + respTo + '"]';
      $container.find( selector ).slideDown();

      $container.attr( 'data-answered', 'yes' );

    } );
  },

  /*
   * This function updates the text in the "questions" in Step 2
   * based on the user's current age
   * @param {number} currentAge   The user's current age
   */
  update: function( currentAge ) {
    var $ageSplits = $( '.lifestyle-btn.age-split' );
    if ( currentAge < 50 ) {
      $ageSplits.each( function() {
        $( this ).val(
          $( this ).attr( 'data-base-value' ) + '-under50'
        );
      } );
    } else {
      $ageSplits.each( function() {
        $( this ).val(
          $( this ).attr( 'data-base-value' ) + '-over50'
        );
      } );
    }
    this.limitAgeSelector( currentAge );
  },

  /*
   * This function limits the age selector in Step 3 to
   * the user's current age or higher
   * @param {number} currentAge   The user's current age
   */
  limitAgeSelector: function( currentAge ) {
    var $select = $( '#retirement-age-selector' ),
        firstOption = $select.find( 'option' )[0],
        retirementAge = 62;

    $select.empty();
    // We save and append the first OPTION, "Choose age"
    $select.append( firstOption );
    if ( retirementAge < currentAge ) {
      retirementAge = currentAge;
    }

    for ( var x = retirementAge; x <= 70; x++ ) {
      var elem = '<option value="' + x;
      elem += '">' + x + '</option>';
      $select.append( elem );
    }
  }

};

module.exports = questionsView;
