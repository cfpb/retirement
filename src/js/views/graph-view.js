'use strict';

var numToMoney = require( '../utils/num-to-money' );
var validDates = require( '../utils/valid-dates' );
var strToNum = require( '../utils/handle-string-input' );
var getModelValues = require( '../wizards/get-model-values' );
var questionsView = require( './questions-view' );
var fetch = require( '../wizards/fetch-api-data' );

var graphView = {
  mouseCoords: {},
  indicator: false,
  sliderLine: {},
  graphBackground: {},
  bars: {},
  graphSettings: {
    graphHeight : 0,
    gutterWidth : 0,
    barWidth : 0,
    indicatorSide : 0,
    graphWidth : 0,
    barGut : 0,
    barOffset : 0
  },
  ages: [ 62, 63, 64, 65, 66, 67, 68, 69, 70 ],
  selectedAge: 0,

  init: function() {
    var SSData = getModelValues.benefits();
    var lifetimeData = getModelValues.lifetime();

    $( 'input[name="benefits-display"]' ).click( function() {
      graphView.setTextByAge();
    } );

    $( '#step-one-form' ).submit( function( ev ) {
      ev.preventDefault();
      $( '#salary-input' ).blur();
      graphView.checkEstimateReady();
      graphView.getYourEstimates();
    } );

    $( '#claim-canvas' ).on( 'click', '.age-text', function() {
      graphView.moveIndicatorToAge( $( this ).attr( 'data-age-value' ) );
    } );

    $( '[data-bar_age]' ).click( function() {
      var age = $( this ).attr( 'data-bar_age' );
      graphView.moveIndicatorToAge( age );
    } );

    $( document ).keypress( function( ev ) {
      if ( ev.which === 57 && ev.ctrlKey === true ) {
        $( '#bd-day' ).val( '1' );
        $( '#bd-month' ).val( '1' );
        $( '#bd-year' ).val( '1949' );
        $( '#salary-input' ).val( '40000' );
        $( '#step-one-form' ).submit();
      }
      if ( ev.which === 55 && ev.ctrlKey === true ) {
        $( '#bd-day' ).val( '7' );
        $( '#bd-month' ).val( '7' );
        $( '#bd-year' ).val( '1977' );
        $( '#salary-input' ).val( '70000' );
        $( '#step-one-form' ).submit();
      }
    } );

    // Retirement age selector handler
    $( '#retirement-age-selector' ).change( function() {
      $( '.next-step-description' ).hide();
      $( '.next-step-two .step-two_option' ).hide();
      $( '#age-selector-response' ).show();
      $( '#age-selector-response .age-response-value' ).text( $( this ).find( 'option:selected' ).val() );
      if ( $( this ).find( 'option:selected' ).val() < SSData.fullAge ) {
        $( '.next-step-two_under' ).show();
      } else if ( $( this ).find( 'option:selected' ).val() > SSData.fullAge ) {
        $( '.next-step-two_over' ).show();
      } else {
        $( '.next-step-two_equal' ).show();
      }

      // Scroll response into view if it's not visible
      if ( graphView.isElementInView( '#age-selector-response' ) === false ) {
        $( 'html, body' ).animate( {
          scrollTop: $( '#retirement-age-selector' ).offset().top - 20
        }, 300);
      }

    } );

    // Helpful button
    $( '#age-selector-response .helpful-btn' ).click( function() {
      $( '#age-selector-response .thank-you' ).show();
      $( '#age-selector-response .helpful-btn' ).attr( 'disabled', true).addClass( 'btn__disabled' ).hide();
    } );

    // reformat salary
    $( '#salary-input' ).blur( function() {
      var salaryNumber = strToNum( $( '#salary-input' ).val() ),
          salary = numToMoney( salaryNumber );
      $( '#salary-input' ).val( salary );
    } );

    // reformat date fields
    $( '.birthdate-inputs' ).blur( function() {
      var month = $( '#bd-month' ).val().replace( /\D/g, '' ),
          day = $( '#bd-day' ).val().replace( /\D/g, '' ),
          year = $( '#bd-year' ).val().replace( /\D/g, '' );
    } );

    // Check if the estimate is ready
    $( '.birthdate-inputs, #salary-input' ).keyup( function() {
      graphView.checkEstimateReady();
    } );

    // Initialize the app
    this.redrawGraph();
    this.initIndicator();

    // Window resize handler
    $( window ).resize( function() {
      if ( $( '.step-one-hidden, .step-three .hidden-content' ).is( ':visible') ) {
        graphView.redrawGraph();
      }
    } );

    // Hamburger menu
    $( '.toggle-menu' ).on( 'click', function( ev ) {
      ev.preventDefault();
      $( 'nav.main ul' ).toggleClass( 'vis' );
    } );
  },

  /*
   * This method is the preferred way of changing the graphSettings property
   * @param {string} setting - The property name of the setting to be changed
   * @param {string|number} value - The new value of the setting
   */
  changeGraphSetting: function( setting, value ) {
    this.graphSettings[setting] = value;
  },

  /*
   * This function checks if the page is ready for the Estimate button to be hit.
   * "Ready" means that the inputs have values typed into them
   */
  checkEstimateReady: function() {
    var $button = $( '#get-your-estimates' ),
        m = ( $( '#bd-month' ).val() !== '' ),
        d = ( $( '#bd-day' ).val() !== '' ),
        y = ( $( '#bd-year' ).val() !== '' ),
        s = ( $( '#salary-input' ).val() !== '' );
    if ( m && d && y && s ) {
      $button.attr( 'disabled', false).removeClass( 'btn__disabled' );
    } else {
      $button.attr( 'disabled', true).addClass( 'btn__disabled' );
    }
  },

  /*
   * Initializes the listener on the slider indicator
   */
  initIndicator: function() {
    var $indicator = $( '#graph_slider-input' );
    // Need both onchange and oninput to work in all browsers
    // http://www.impressivewebs.com/onchange-vs-oninput-for-range-sliders/
    $indicator.on( 'change input', function() {
      var indicatorValue = Number( $( this ).val() );
      graphView.setAgeWithIndicator( indicatorValue );
    });
  },

  /*
   * This function toggles the highlighting of the date of birth fields
   * @param {boolean}   Whether the fields should be highlighted (true|false)
   */
  highlightAgeFields: function( bool ) {
    var $ageFields = $( '#bd-day, #bd-month, #bd-year' );
    if ( bool ) {
      $ageFields.addClass( 'notification-input__warning' );
    } else {
      $ageFields.removeClass( 'notification-input__warning' );
    }
  },

  /*
   * This function determins if the element specified is currently in the
   * browser window (i.e. "in view")
   * @param {string} selector   The selector for the element specified
   */
  isElementInView: function( selector ) {
    var $ele = $( selector ),
        target;
    if ( $ele.offset().top > $(window).scrollTop() + $(window).height() - 150 ) {
      return false;
    }
    return true;
  },

  /*
   * This function validates the numbers in the date of birth fields as
   * valid dates
   */
  validateBirthdayFields: function() {
    var day = $( '#bd-day' ).val(),
        month = $( '#bd-month' ).val(),
        year = $( '#bd-year' ).val(),
        dates = validDates( month, day, year );
    $( '#bd-day' ).val( dates.day );
    $( '#bd-month' ).val( dates.month );
    $( '#bd-year' ).val( dates.year );
    return dates;
  },

  /*
   * This is the main function in the graph view. It hits the API with the birth
   * date and salary values, then updates the graph view with the returned data
   * using a variety of view-updating functions
   */
  getYourEstimates: function() {
    var dataLang = $( 'body' ).attr('data-lang'),
        dates = this.validateBirthdayFields(),
        salary = strToNum( $( '#salary-input' ).val() ),
        lifetimeData,
        SSData;

    // Hide warnings, show loading indicator
    $( '.cf-notification' ).slideUp();
    this.highlightAgeFields( false );
    $( '#api-data-loading-indicator' ).css( 'display', 'inline-block' );
    $.when( fetch.apiData( dates.concat, salary, dataLang ) ).done( function( resp ) {
      if ( resp.error === '' ) {
        SSData = getModelValues.benefits();
        lifetimeData = getModelValues.lifetime();

        $( '.step-two .question' ).css( 'display', 'inline-block' );
        $( '.step-one-hidden, .before-step-two, .step-two, .before-step-three, .step-three, .step-three .hidden-content' ).show();

        questionsView.update( SSData.currentAge );
        graphView.redrawGraph();
        graphView.resetView();

        // Scroll graph into view if it's not visible
        if ( graphView.isElementInView( '#claim-canvas' ) === false ) {
          $( 'html, body' ).animate({
            scrollTop: $( '#estimated-benefits-description' ).offset().top - 20
          }, 300);
        }
        graphView.selectedAge = SSData.fullAge;
      } else {
        $( '.cf-notification' ).slideDown();
        $( '.cf-notification .cf-notification_text' ).html( resp.note );
        if ( resp.current_age >= 71 || resp.current_age < 21 ) {
          graphView.highlightAgeFields( true );
        }
      }
      $( '#api-data-loading-indicator' ).css( 'display', 'none' );
    } );
  },

  /*
   * This function toggles the graph text between monthly view and annual view.
   * It has no parameters, but it uses the selector to determine which values to
   * show
   */
  toggleMonthlyAnnual: function () {
    var SSData = getModelValues.benefits(),
        benefitsValue = SSData['age' + this.selectedAge];
    if ( $( 'input[name="benefits-display"]:checked' ).val() === 'annual' ) {
      benefitsValue *= 12;
      $( '#graph-container .monthly-view' ).hide();
      $( '#graph-container .annual-view' ).show();
    } else {
      $( '#graph-container .monthly-view' ).show();
      $( '#graph-container .annual-view' ).hide();
    }
  },

  /*
   * This function changes the text of benefits elements based on selectedAge
   */
  setTextByAge: function() {
    var gset = this.graphSettings,
        SSData = getModelValues.benefits(),
        lifetimeData = getModelValues.lifetime(),
        lifetimeBenefits = numToMoney( lifetimeData['age' + this.selectedAge] ),
        fullAgeBenefitsValue = SSData['age' + SSData.fullAge],
        benefitsValue = SSData['age' + this.selectedAge],
        $selectedBar,
        benefitsTop,
        benefitsLeft,
        $fullAgeBar,
        fullAgeLeft,
        fullAgeTop,
        percent;

    if ( $( '#estimated-benefits-input [name="benefits-display"]:checked' ).val() === 'annual' ) {
      benefitsValue *= 12;
      fullAgeBenefitsValue *= 12;
    }
    this.toggleMonthlyAnnual();

    $( '#claim-canvas .age-text' ).removeClass( 'selected-age' );
    // Set selected-age
    $( '[data-age-value="' + graphView.selectedAge + '"]' ).addClass( 'selected-age' );

    // set text and position for #benefits-text div
    $( '#benefits-text' ).text( numToMoney( benefitsValue ) );
    $selectedBar = $( '[data-bar_age="' + graphView.selectedAge + '"]' );
    benefitsTop = parseInt( $selectedBar.css( 'top' ), 10 );
    benefitsTop -= $( '#benefits-text' ).height() + 10;
    benefitsLeft = parseInt( $selectedBar.css( 'left' ), 10 );
    benefitsLeft -= $( '#benefits-text' ).width() / 2 - gset.barWidth / 2;
    $( '#benefits-text' ).css( 'top', benefitsTop );
    $( '#benefits-text' ).css( 'left', benefitsLeft );

    // set text, position and visibility of #full-age-benefits-text
    $( '#full-age-benefits-text' ).text( numToMoney( fullAgeBenefitsValue ) );
    $fullAgeBar = $( '[data-bar_age="' + SSData.fullAge + '"]' );
    fullAgeTop = parseInt( $fullAgeBar.css( 'top' ), 10 );
    fullAgeTop -= $( '#full-age-benefits-text' ).height() + 10;
    fullAgeLeft = parseInt( $fullAgeBar.css( 'left' ), 10 );
    fullAgeLeft -= $( '#full-age-benefits-text' ).width() / 2 - gset.barWidth / 2;
    $( '#full-age-benefits-text' ).css( 'top', fullAgeTop );
    $( '#full-age-benefits-text' ).css( 'left', fullAgeLeft );
    if ( this.selectedAge === SSData.fullAge || SSData.currentAge > SSData.fullAge ) {
      $( '#full-age-benefits-text' ).hide();
    } else {
      $( '#full-age-benefits-text' ).show();
    }

    // set lifetime benefits text
    $( '#lifetime-benefits-value' ).text( lifetimeBenefits );

    // Set extra text for early and full retirement ages
    if ( this.selectedAge === 70 ) {
      $( '#selected-retirement-age-value' ).text( window.gettext('70') );
    } else if ( this.selectedAge === SSData.earlyAge ) {
      $( '#selected-retirement-age-value' ).text( window.gettext( SSData.earlyRetirementAge ) );
    } else if ( this.selectedAge === SSData.fullAge && SSData.currentAge < SSData.fullAge ) {
      $( '#selected-retirement-age-value' ).text( window.gettext( SSData.fullRetirementAge ) );
    } else {
      $( '#selected-retirement-age-value' ).text( window.gettext( this.selectedAge ) );
    }

    // Graph content
    $( '.graph-content .content-container' ).hide();
    if ( this.selectedAge === 70 ) {
      $( '.graph-content .content-container.max-retirement' ).show();
    } else if ( this.selectedAge < SSData.fullAge ) {
      $( '.graph-content .content-container.early-retirement' ).show();
    } else {
      $( '.graph-content .content-container.full-retirement' ).show();
    }
    if ( this.selectedAge === SSData.fullAge || ( this.selectedAge === SSData.currentAge && SSData.past_fra ) ) {
      if ( SSData.past_fra ) {
        if ( SSData.currentAge === 70 ) {
          $( '.benefit-modification-text' ).html( window.gettext('is your maximum benefit claiming age.') );
          $( '.compared-to-full' ).hide();
        } else {
          $( '.benefit-modification-text' ).html( window.gettext('is past your full benefit claiming age.') );
          $( '.compared-to-full' ).hide();
        }
      } else {
        $( '.benefit-modification-text' ).html( window.gettext('is your full benefit claiming age.') );
        $( '.compared-to-full' ).hide();
      }
    } else if ( this.selectedAge < SSData.fullAge ) {
      percent = ( SSData['age' + SSData.fullAge] - SSData['age' + this.selectedAge] ) / SSData['age' + SSData.fullAge];
      percent = Math.abs( Math.round( percent * 100 ) );
      $( '.benefit-modification-text' ).html( window.gettext('<strong>reduces</strong> your monthly benefit by&nbsp;<strong>') + percent + '</strong>%' );
      $( '.compared-to-full' ).html( window.gettext( 'Compared to claiming at your full benefit claiming age.' ) );
      $( '.compared-to-full' ).show();
    } else if ( this.selectedAge > SSData.fullAge ) {
      percent = ( SSData['age' + SSData.fullAge] - SSData['age' + this.selectedAge] ) / SSData['age' + SSData.fullAge];
      if ( SSData.past_fra ) {
        percent = ( SSData['age' + SSData.currentAge] - SSData['age' + this.selectedAge] ) / SSData['age' + SSData.currentAge];
        var comparedToClaimingFullEs = window.gettext( 'Compared to claiming at' );
        var comparedToClaimingEsSplit = comparedToClaimingFullEs.split( 'XXX' );
        if ( typeof comparedToClaimingEsSplit !== 'undefined' ) {
          if ( comparedToClaimingEsSplit.length === 2 ) {
            $( '.compared-to-full' ).html( comparedToClaimingEsSplit[0] + ' ' + SSData.currentAge + ' ' + comparedToClaimingEsSplit[1] );
          } else {
            $( '.compared-to-full' ).html( comparedToClaimingEsSplit[0] + ' ' + SSData.currentAge + '.' );
          }
        }
      } else {
        $( '.compared-to-full' ).html( window.gettext( 'Compared to claiming at your full benefit claiming age.' ) );
      }
      percent = Math.abs( Math.round( percent * 100 ) );
      $( '.benefit-modification-text' ).html( window.gettext('<strong>increases</strong> your benefit by&nbsp;<strong>') +
        percent + '</strong>%' );
      $( '.compared-to-full' ).show();
    }
  },

  /*
   * Sets an age on the graph when the indicator is moved
   * @param {number} indicatorValue Value of the range slider
   */
  setAgeWithIndicator: function ( indicatorValue ) {
    var SSData = getModelValues.benefits(),
        $indicator = $( '#graph_slider-input' );
    graphView.selectedAge = indicatorValue;
    // Don't let the user select an age younger than they are now
    if ( graphView.selectedAge < SSData.currentAge ) {
      graphView.selectedAge = SSData.currentAge;
      $indicator.val( graphView.selectedAge );
    }
    graphView.drawBars();
    graphView.setTextByAge();
  },

  /*
   * Uses setAgeWithIndicator to move the indicator to age
   * NOTE: This function is all that's require to change the chart to a different age
   * @param {number} age  The age for the indicator to be set to
   */
  moveIndicatorToAge: function( age ) {
    var gset = this.graphSettings,
        SSData = getModelValues.benefits(),
        $indicator = $( '#graph_slider-input' );
    if ( age < SSData.currentAge ) {
      age = SSData.currentAge;
    }
    age = Number( age );
    $indicator.val( age );
    this.setAgeWithIndicator( age );
  },

  /**
    * This function updates the  graphSettings object based on window size
    * and the position of various elements
    */
  setGraphDimensions: function() {
    var canvasLeft,
        graphWidth,
        graphHeight,
        barWidth,
        barOffset,
        gutterWidth,
        heightRatio,
        SSData = getModelValues.benefits();

    // Update width settings
    canvasLeft = Number( $( '#claim-canvas' ).css( 'left' ).replace( /\D/g, '' ) );
    canvasLeft += Number( $( '#claim-canvas' ).css( 'padding-left' ).replace( /\D/g, '' ) );

    graphWidth = $( '.canvas-container' ).width() - canvasLeft;
    if ( graphWidth > ( $( window ).width() - canvasLeft ) * 0.95 ) {
      graphWidth = ( $(window).width() - canvasLeft ) * 0.95;
    }
    this.changeGraphSetting( 'graphWidth', graphWidth );

    barOffset = 94;
    graphHeight = 380;
    if ( $( window ).width() < 850 ) {
      barOffset = 52;
      graphHeight = 210;
      $( '#claim-canvas svg' ).css( 'overflow', 'visible' );
    }
    this.changeGraphSetting( 'graphHeight', graphHeight );
    this.changeGraphSetting( 'barOffset', barOffset );

    barWidth = Math.floor( graphWidth / 17 );
    this.changeGraphSetting( 'barWidth', barWidth );

    gutterWidth = Math.floor( graphWidth / 17 );
    this.changeGraphSetting( 'gutterWidth', gutterWidth );

    this.changeGraphSetting( 'barGut', barWidth + gutterWidth );

    heightRatio = ( graphHeight - barOffset ) / SSData.age70;
    this.changeGraphSetting( 'heightRatio', heightRatio );

    $( '#claim-canvas, .x-axis-label' ).width( graphWidth );
    $( '#claim-canvas').height( graphHeight );
    $( '#graph_slider-input' ).width( ( barWidth * 9 ) + ( gutterWidth * 8 ) + 8 );
  },

  /*
   * This helper function draws and redraws the indicator bars for each age
   */
  drawBars: function() {
    var SSData = getModelValues.benefits(),
        gset = this.graphSettings,
        leftOffset = 0;

    $.each( this.ages, function( i, val ) {
      var color = '#e3e4e5',
          key = 'age' + val,
          gset = graphView.graphSettings,
          height = gset.heightRatio * SSData[key],
          $bar = $( '[data-bar_age="' + val + '"]' );
      $bar.css( {
        'left': leftOffset,
        'top': gset.graphHeight - gset.barOffset - height,
        'height': height,
        'width': gset.barWidth,
        'background': color
      } );

      leftOffset += gset.barGut;
      if ( val >= SSData.fullAge ) {
        $bar.css( 'background', '#aedb94' );
      }
    } );
  },

  /*
   * This helper function draws the background lines for the chart
   */
  drawGraphBackground: function() {
    var gset = this.graphSettings,
        barInterval = gset.graphHeight / 4,
        totalWidth = ( gset.barWidth * 9 ) + ( gset.gutterWidth * 8 ),
        yCoord = gset.graphHeight - barInterval,
        $backgroundBars = $( '[data-bg-bar-number]' ),
        $sliderLine = $( '#graph__slider-line' ),
        sliderLineTop;

    $backgroundBars.css( 'width', totalWidth );
    $backgroundBars.each( function() {
      var $ele = $( this ),
          count = $ele.attr( 'data-bg-bar-number' );
      $ele.css( {
        'width': totalWidth,
        'top': yCoord
      } );

      yCoord = gset.graphHeight - Math.round( barInterval * count ) + 1;
    } );
  },

  /**
    * This helper functions draws the age text boxes on the graph
    */
  drawAgeBoxes: function() {
    var leftOffset = 0,
        gset = this.graphSettings;
    // remove existing boxes
    $( '#claim-canvas .age-text' ).remove();
    $.each( this.ages, function(i, val) {
      var left,
          ageDiv;
      $( '#claim-canvas' ).append( '<div class="age-text"><p class="h3">' + val + '</p></div>' );
      ageDiv = $( '#claim-canvas .age-text:last' );
      ageDiv.attr( 'data-age-value', val);

      // set width to bar width (minus stroke width x2)
      ageDiv.width( gset.barWidth );
      if ($(window).width() < 850) {
        ageDiv.css( {
          'left': leftOffset,
          'top': gset.graphHeight - 48 + 'px'
        } );
      } else {
        ageDiv.css( {
          'left': leftOffset,
          'top': gset.graphHeight - 88 + 'px'
        } );
      }
      leftOffset += gset.barGut;
    } );
  },

  /**
    * This function iterates through each drawing helper function
    */
  redrawGraph: function() {
    var SSData = getModelValues.benefits();
    this.setGraphDimensions();
    this.drawGraphBackground();
    this.drawBars();
    this.drawAgeBoxes();
  },

  /**
   * This function draws new bars and updates text. It is primarily for use
   * after new data is received.
   */
  resetView: function() {
    var SSData = getModelValues.benefits();
    this.drawBars();
    this.setTextByAge();
    this.moveIndicatorToAge( SSData.fullAge );
    $( '.benefit-selections-area' ).empty();
  }

};

module.exports = graphView;
