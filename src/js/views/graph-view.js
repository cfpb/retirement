import fetch from '../wizards/fetch-api-data';
import getModelValues from '../wizards/get-model-values';
import isElementInView from '../utils/is-element-in-view';
import nextStepsView from './next-steps-view';
import numToMoney from '../utils/num-to-money';
import questionsView from './questions-view';
import strToNum from '../utils/handle-string-input';
import validDates from '../utils/valid-dates';

// TODO: remove jquery.
import $ from 'jquery';

const graphView = {
  mouseCoords: {},
  indicator: false,
  sliderLine: {},
  graphBackground: {},
  bars: {},
  graphSettings: {
    graphHeight: 0,
    gutterWidth: 0,
    barWidth: 0,
    indicatorSide: 0,
    graphWidth: 0,
    barGut: 0,
    barOffset: 0
  },
  ages: [ 62, 63, 64, 65, 66, 67, 68, 69, 70 ],
  selectedAge: 0,
  textlets: {
    currentAge: 0,
    fullRetirementAge: 0,
    yourMax: 'is your maximum benefit claiming age.',
    pastFull: 'is past your full benefit claiming age.',
    yourFull: 'is your full benefit claiming age.',
    reduces: '<strong>reduces</strong> your monthly benefit by&nbsp;<strong>',
    increases: '<strong>increases</strong> your benefit by&nbsp;<strong>',
    comparedFull: 'Compared to claiming at your full benefit claiming age.',
    comparedAt: 'Compared to claiming at'
  },

  init: function() {
    const SSData = getModelValues.benefits();
    this.getTranslations();

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
      const age = $( this ).attr( 'data-bar_age' );
      graphView.moveIndicatorToAge( age );
    } );

    $( document ).keypress( function( ev ) {
      if ( ev.which === 57 && ev.ctrlKey === true ) {
        $( '#bd-day' ).val( '1' );
        $( '#bd-month' ).val( '1' );
        $( '#bd-year' ).val( '1948' );
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

    // reformat salary
    $( '#salary-input' ).blur( function() {
      const salaryNumber = strToNum( $( '#salary-input' ).val() ),
            salary = numToMoney( salaryNumber );
      $( '#salary-input' ).val( salary );
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
      const hiddenContent = '.step-one-hidden, .step-three .hidden-content';
      if ( $( hiddenContent ).is( ':visible' ) ) {
        graphView.redrawGraph();
      }
    } );

    // Hamburger menu
    $( '.toggle-menu' ).on( 'click', function( ev ) {
      ev.preventDefault();
      $( 'nav.main ul' ).toggleClass( 'vis' );
    } );
  },

  /* This method is the preferred way of changing the graphSettings property
     @param {string} setting - The property name of the setting to be changed
     @param {string|number} value - The new value of the setting */
  changeGraphSetting: function( setting, value ) {
    this.graphSettings[setting] = value;
  },

  /* This function checks if the page is ready for the Estimate button to be
     hit. "Ready" means that the inputs have values typed into them. */
  checkEstimateReady: function() {
    const $button = $( '#get-your-estimates' );
    const m = $( '#bd-month' ).val() !== '';
    const d = $( '#bd-day' ).val() !== '';
    const y = $( '#bd-year' ).val() !== '';
    const s = $( '#salary-input' ).val() !== '';

    if ( m && d && y && s ) {
      $button.attr( 'disabled', false ).removeClass( 'a-btn__disabled' );
    } else {
      $button.attr( 'disabled', true ).addClass( 'a-btn__disabled' );
    }
  },

  /* Initializes the listener on the slider indicator */
  initIndicator: function() {
    const $indicator = $( '#graph_slider-input' );

    /* Need both onchange and oninput to work in all browsers
       http://www.impressivewebs.com/onchange-vs-oninput-for-range-sliders/ */
    $indicator.on( 'change input', function() {
      const indicatorValue = Number( $( this ).val() );
      graphView.setAgeWithIndicator( indicatorValue );
    } );
  },

  /* This function toggles the highlighting of the date of birth fields
     @param {boolean}   Whether the fields should be highlighted (true|false) */
  highlightAgeFields: function( bool ) {
    const $ageFields = $( '#bd-day, #bd-month, #bd-year' );
    if ( bool ) {
      $ageFields.addClass( 'notification-input__warning' );
    } else {
      $ageFields.removeClass( 'notification-input__warning' );
    }
  },

  /* This function validates the numbers in the date of birth fields as
     valid dates */
  validateBirthdayFields: function() {
    const dayDom = document.querySelector( '#bd-day' );
    const monthDom = document.querySelector( '#bd-month' );
    const yearDom = document.querySelector( '#bd-year' );
    const day = dayDom.value;
    const month = monthDom.value;
    const year = yearDom.value;
    const dates = validDates( month, day, year );
    dayDom.value = dates.day;
    monthDom.value = dates.month;
    yearDom.value = dates.year;

    return dates;
  },

  /* This is the main function in the graph view. It hits the API with the birth
     date and salary values, then updates the graph view with the returned data
     using a variety of view-updating functions */
  getYourEstimates: function() {
    const dataLang = document.body.getAttribute( 'data-lang' );
    const dates = this.validateBirthdayFields();
    const salary = strToNum( $( '#salary-input' ).val() );
    let lifetimeData;
    let SSData;

    // Hide warnings, show loading indicator
    $( '.m-notification' ).slideUp();
    this.highlightAgeFields( false );
    const loadIndDom = document.querySelector( '#api-data-loading-indicator' );
    loadIndDom.style.display = 'inline-block';
    $.when(
      fetch.apiData( dates.concat, salary, dataLang )
    ).done( function( resp ) {
      if ( resp.error === '' ) {
        SSData = getModelValues.benefits();
        lifetimeData = getModelValues.lifetime();
        $( '.step-two .question' ).css( 'display', 'inline-block' );
        $( '.step-one-hidden,' +
            '.before-step-two,' +
            '.step-two,' +
            '.before-step-three,' +
            '.step-three,' +
            '.step-three .hidden-content' ).show();

        graphView.textlets.currentAge = window.gettext( SSData.currentAge );
        graphView.textlets.fullRetirementAge = window.gettext(
          SSData.fullRetirementAge
        );
        questionsView.update( SSData.currentAge );
        nextStepsView.init( SSData.currentAge, SSData.fullAge );
        graphView.redrawGraph();
        graphView.resetView();

        // Scroll graph into view if it's not visible
        if ( isElementInView( '#claim-canvas' ) === false ) {
          $( 'html, body' ).animate( {
            scrollTop: $( '#estimated-benefits-description' ).offset().top - 20
          }, 300 );
        }

      } else {
        $( '.m-notification' ).slideDown();
        $( '.m-notification .m-notification_content' ).html( resp.note );
        if ( resp.current_age >= 71 || resp.current_age < 21 ) {
          graphView.highlightAgeFields( true );
        }
      }
      $( '#api-data-loading-indicator' ).css( 'display', 'none' );
    } );
  },

  /**
   * This function updates the placement of the benfits text boxes
   */
  placeBenefitsText: function() {
    const SSData = getModelValues.benefits();
    const gset = this.graphSettings;
    let fullAgeBenefitsValue = SSData['age' + SSData.fullAge];
    let benefitsValue = SSData['age' + this.selectedAge];
    let $selectedBar = 5;
    let benefitsTop;
    let benefitsLeft;
    let fullAgeLeft;
    let fullAgeTop;
    const $fullAgeBenefits = $( '#full-age-benefits-text' );

    if ( $( '[name="benefits-display"]:checked' ).val() === 'annual' ) {
      benefitsValue *= 12;
      fullAgeBenefitsValue *= 12;
    }

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
    $fullAgeBenefits.text( numToMoney( fullAgeBenefitsValue ) );
    const $fullAgeBar = $( '[data-bar_age="' + SSData.fullAge + '"]' );
    fullAgeTop = parseInt( $fullAgeBar.css( 'top' ), 10 );
    fullAgeTop -= $fullAgeBenefits.height() + 10;
    fullAgeLeft = parseInt( $fullAgeBar.css( 'left' ), 10 );
    fullAgeLeft -= $fullAgeBenefits.width() / 2 -
      gset.barWidth / 2;
    $fullAgeBenefits.css( 'top', fullAgeTop );
    $fullAgeBenefits.css( 'left', fullAgeLeft );

  },

  /* This function changes the text of benefits elements based on selectedAge */
  setTextByAge: function() {
    const gset = this.graphSettings;
    const textlets = this.textlets;
    const SSData = getModelValues.benefits();
    const lifetimeData = getModelValues.lifetime();
    const lifetimeBenefits = numToMoney( lifetimeData['age' + this.selectedAge] );
    const fullAgeValue = Number( SSData['age' + SSData.fullAge] );
    const currentAgeValue = Number( SSData['age' + SSData.currentAge] );
    const selectedAgeValue = Number( SSData['age' + this.selectedAge] );
    let percent;
    let text;
    const selectedBelowFRA = this.selectedAge < SSData.fullAge;
    const selectedFRA = this.selectedAge === SSData.fullAge;
    const selectedAboveFRA = this.selectedAge > SSData.fullAge;
    const selectedCurrent = this.selectedAge === SSData.currentAge;
    const isFRA = SSData.currentAge === SSData.fullAge;
    const isYoungerThanFRA = SSData.currentAge < SSData.fullAge;
    const $benefitsMod = $( '.benefit-modification-text' );
    const $selectedAgeText = $( '#selected-retirement-age-value' );
    const $fullAgeBenefits = $( '#full-age-benefits-text' );
    const $comparedToFull = $( '.compared-to-full' );

    // Set default state
    $fullAgeBenefits.show();

    // Put the benefits text in the right place
    graphView.placeBenefitsText();

    // Set selected-age class on correct age
    $( '#claim-canvas .age-text' ).removeClass( 'selected-age' );
    $( '[data-age-value="' + graphView.selectedAge + '"]' )
      .addClass( 'selected-age' );

    // Set lifetime benefits text
    $( '#lifetime-benefits-value' ).text( lifetimeBenefits );

    // Set the selected retirement age text
    $selectedAgeText.text( this.selectedAge );

    // The user is older than FRA
    if ( SSData.past_fra ) {
      $fullAgeBenefits.hide();
    }

    /* !! Now we update text based on the age selected !! //
       XXXXX //
       Clear the content container */
    $( '.graph-content .content-container' ).hide();

    // The user has selected an age below FRA

    if ( selectedBelowFRA ) {
      $( '.graph-content .content-container.early-retirement' ).show();
      percent = ( fullAgeValue - selectedAgeValue ) / fullAgeValue;
      percent = Math.abs( Math.round( percent * 100 ) );
      $benefitsMod.html( textlets.reduces + percent + '</strong>%' );
      $comparedToFull.html( textlets.comparedFull ).show();
      $( '.selected-retirement-age__fra' ).hide();
      $( '.selected-retirement-age__not-fra' ).show();
    }

    // The user has selected FRA, or current age if past FRA
    if ( selectedFRA || ( selectedCurrent && SSData.past_fra ) ) {
      $fullAgeBenefits.hide();
      $selectedAgeText.html( textlets.fullRetirementAge );
      $( '.graph-content .content-container.full-retirement' ).show();
      $benefitsMod.html( textlets.yourFull );

      // If the user is past FRA, display pastFull
      if ( SSData.past_fra ) {
        $benefitsMod.html( textlets.pastFull );
        $selectedAgeText.html( SSData.currentAge );
      }

      $comparedToFull.hide();
      $( '.selected-retirement-age__fra' ).show();
      $( '.selected-retirement-age__not-fra' ).hide();
    }

    // The user has selected an age above FRA, but it's not their current age
    if ( selectedAboveFRA && !selectedCurrent ) {
      $( '.graph-content .content-container.full-retirement' ).show();
      percent = ( fullAgeValue - selectedAgeValue ) / fullAgeValue;

      // If user is past FRA, percent is compared to current Age instead
      if ( SSData.past_fra ) {
        percent = ( currentAgeValue - selectedAgeValue ) / currentAgeValue;
        text = textlets.comparedAt;
        // Text replace for Spanish version
        if ( text.indexOf( 'XXX' ) === -1 ) {
          text += ' ' + SSData.currentAge + '.';
        } else {
          text = text.replace( /XXX/i, SSData.currentAge );
        }
      } else {
        text = textlets.comparedFull;
      }
      $comparedToFull.html( text );
      percent = Math.abs( Math.round( percent * 100 ) );
      $benefitsMod.html( textlets.increases + percent + '</strong>%' );
      $comparedToFull.show();
      $( '.selected-retirement-age__fra' ).hide();
      $( '.selected-retirement-age__not-fra' ).show();
    }

    // The user has selected age 70
    if ( this.selectedAge === 70 ) {
      $( '.graph-content .content-container' ).hide();
      $( '.graph-content .content-container.max-retirement' ).show();
    }

    // If the user is 70, override other content
    if ( SSData.currentAge === 70 ) {
      $selectedAgeText.html( textlets.selectedAge );
      $benefitsMod.html( textlets.yourMax );
    }
  },

  /* Sets an age on the graph when the indicator is moved
     @param {number} indicatorValue Value of the range slider */
  setAgeWithIndicator: function( indicatorValue ) {
    const SSData = getModelValues.benefits();
    const $indicator = $( '#graph_slider-input' );
    graphView.selectedAge = indicatorValue;
    graphView.textlets.selectedAge = window.gettext( graphView.selectedAge );
    // Don't let the user select an age younger than they are now
    if ( graphView.selectedAge < SSData.currentAge ) {
      graphView.selectedAge = SSData.currentAge;
      $indicator.val( graphView.selectedAge );
    }
    graphView.drawBars();
    graphView.setTextByAge();
  },

  /* Uses setAgeWithIndicator to move the indicator to age
     NOTE: This function is all that's require to change the chart to a
     different age
     @param {number} age  The age for the indicator to be set to */
  moveIndicatorToAge: function( age ) {
    const SSData = getModelValues.benefits();
    const indicatorDom = document.querySelector( '#graph_slider-input' );
    if ( age < SSData.currentAge ) {
      age = SSData.currentAge;
    }
    age = Number( age );
    indicatorDom.value = age;
    graphView.setAgeWithIndicator( age );
  },

  /**
    * This function updates the  graphSettings object based on window size
    * and the position of various elements
    */
  setGraphDimensions: function() {
    let canvasLeft;
    let graphWidth;
    let graphHeight;
    let barOffset;
    const SSData = getModelValues.benefits();

    // Update width settings
    canvasLeft = Number(
      $( '#claim-canvas' ).css( 'left' ).replace( /\D/g, '' )
    );
    canvasLeft += Number(
      $( '#claim-canvas' ).css( 'padding-left' ).replace( /\D/g, '' )
    );

    graphWidth = $( '.canvas-container' ).width() - canvasLeft;
    if ( graphWidth > ( $( window ).width() - canvasLeft ) * 0.95 ) {
      graphWidth = ( $( window ).width() - canvasLeft ) * 0.95;
    }
    graphView.changeGraphSetting( 'graphWidth', graphWidth );

    barOffset = 94;
    graphHeight = 380;
    if ( $( window ).width() < 850 ) {
      barOffset = 52;
      graphHeight = 210;
      $( '#claim-canvas svg' ).css( 'overflow', 'visible' );
    }
    graphView.changeGraphSetting( 'graphHeight', graphHeight );
    graphView.changeGraphSetting( 'barOffset', barOffset );

    const barWidth = Math.floor( graphWidth / 17 );
    graphView.changeGraphSetting( 'barWidth', barWidth );

    const gutterWidth = Math.floor( graphWidth / 17 );
    graphView.changeGraphSetting( 'gutterWidth', gutterWidth );

    graphView.changeGraphSetting( 'barGut', barWidth + gutterWidth );

    const heightRatio = ( graphHeight - barOffset ) / SSData.age70;
    graphView.changeGraphSetting( 'heightRatio', heightRatio );

    $( '#claim-canvas, .x-axis-label' ).width( graphWidth );
    $( '#claim-canvas' ).height( graphHeight );
    $( '#graph_slider-input' ).width( barWidth * 9 + gutterWidth * 8 + 8 );
  },

  /* This helper function draws and redraws the indicator bars for each age */
  drawBars: function() {
    const SSData = getModelValues.benefits();
    let leftOffset = 0;

    $.each( this.ages, function( i, val ) {
      const color = '#e3e4e5';
      const key = 'age' + val;
      const gset = graphView.graphSettings;
      const height = gset.heightRatio * SSData[key];
      const $bar = $( '[data-bar_age="' + val + '"]' );
      $bar.css( {
        left: leftOffset,
        top: gset.graphHeight - gset.barOffset - height,
        height: height,
        width: gset.barWidth,
        background: color
      } );

      leftOffset += gset.barGut;
      if ( val >= SSData.fullAge ) {
        $bar.css( 'background', '#aedb94' );
      }
    } );
  },

  /* This helper function draws the background lines for the chart */
  drawGraphBackground: function() {
    const gset = graphView.graphSettings;
    const barInterval = gset.graphHeight / 4;
    const totalWidth = gset.barWidth * 9 + gset.gutterWidth * 8;
    let yCoord = gset.graphHeight - barInterval;
    const $backgroundBars = $( '[data-bg-bar-number]' );

    $backgroundBars.css( 'width', totalWidth );
    $backgroundBars.each( function() {
      const $ele = $( this );
      const count = $ele.attr( 'data-bg-bar-number' );
      $ele.css( {
        width: totalWidth,
        top: yCoord
      } );

      yCoord = gset.graphHeight - Math.round( barInterval * count ) + 1;
    } );
  },

  /**
    * This helper functions draws the age text boxes on the graph
    */
  drawAgeBoxes: function() {
    let leftOffset = 0;
    const gset = graphView.graphSettings;
    // remove existing boxes
    $( '#claim-canvas .age-text' ).remove();
    $.each( graphView.ages, function( i, val ) {
      $( '#claim-canvas' )
        .append(
          '<div class="age-text"><p class="h3">' + val + '</p></div>'
        );
      const ageDiv = $( '#claim-canvas .age-text:last' );
      ageDiv.attr( 'data-age-value', val );

      // set width to bar width (minus stroke width x2)
      ageDiv.width( gset.barWidth );
      if ( $( window ).width() < 850 ) {
        ageDiv.css( {
          left: leftOffset,
          top: gset.graphHeight - 48 + 'px'
        } );
      } else {
        ageDiv.css( {
          left: leftOffset,
          top: gset.graphHeight - 88 + 'px'
        } );
      }
      leftOffset += gset.barGut;
    } );
  },

  /**
    * This function iterates through each drawing helper function
    */
  redrawGraph: function() {
    graphView.setGraphDimensions();
    graphView.drawGraphBackground();
    graphView.drawBars();
    graphView.drawAgeBoxes();
  },

  /**
   * This function draws new bars and updates text. It is primarily for use
   * after new data is received.
   */
  resetView: function() {
    const SSData = getModelValues.benefits();
    graphView.drawBars();
    graphView.setTextByAge();
    graphView.moveIndicatorToAge( SSData.fullAge );
    $( '.benefit-selections-area' ).empty();
  },

  getTranslations: function() {
    for ( const key in this.textlets ) {
      if ( {}.hasOwnProperty.call( this.textlets, key ) ) {
        this.textlets[key] = window.gettext( this.textlets[key] );
      }
    }
  }
};

export default graphView;
