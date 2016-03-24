'use strict';

var delay = require( '../utils/delay' );
var numToMoney = require( '../utils/num-to-money' );
var calculateAge = require( '../utils/calculate-age' );
var validDates = require( '../utils/valid-dates' );
var getModelValues = require( '../wizards/get-model-values' );
var questionsView = require( './questions-view' );
var fetch = require( '../wizards/fetch-api-data' );

var graphView = {
  barGraph: {},
  indicator: false,
  sliderLine: {},
  graphBackground: {},
  bars: {},
  gset: {
    'graphHeight' : 0,
    'gutterWidth' : 0,
    'barWidth' : 0,
    'indicatorWidth' : 0,
    'indicatorSide' : 0,
    'graphWidth' : 0,
    'barGut' : 0,
    'indicatorLeftSet' : 0,
    'barOffset' : 0
  },
  ages: [ 62, 63, 64, 65, 66, 67, 68, 69, 70 ],
  selectedAge: 0,

  init: function() {
    var SSData = getModelValues.benefits();
    this.selectedAge = SSData.fullAge;
    this.barGraph = new Raphael( $("#claim-canvas")[0] , 600, 400 );

    $( 'input[name="benefits-display"]' ).click( function() {
      graphView.setTextByAge();
    });

    $( '#step-one-form' ).submit( function(e) {
      e.preventDefault();
      $( '#salary-input' ).blur();
      graphView.checkEstimateReady();
      graphView.getYourEstimates();
    });

    $( '#claim-canvas' ).on( 'click', '.age-text', function() {
      var SSData = getModelValues.benefits();
      graphView.moveIndicatorToAge( $(this).attr( 'data-age-value' ), SSData.currentAge );
    });

    $(document).keypress( function(ev) {
      if ( ev.which === 58 ) {
        $.each( this.bars, function(i ,val ) {
          var rot = 360;
          if ( this.transform().length !== 0 ) {
            rot = this.transform()[0][1] + 360;
          }
          this.animate( { transform: 'r' + rot }, 2000 ) ;
        })
      }
      if ( ev.which === 55 && ev.ctrlKey === true ) {
        $( '#bd-day' ).val("7");
        $( '#bd-month' ).val("7");
        $( '#bd-year' ).val("1977");
        $( '#salary-input' ).val("70000");
        $( '#step-one-form' ).submit();
      }
    });

    // Retirement age selector handler
    $( '#retirement-age-selector' ).change( function() {
      $( '.next-step-description' ).hide();
      $( '.next-step-two .step-two_option' ).hide();
      $( '#age-selector-response' ).show();
      $( '#age-selector-response .age-response-value' ).text( $(this).find( 'option:selected' ).val() );
      if ( $(this).find( 'option:selected' ).val() < SSData.fullAge ) {
        $( '.next-step-two_under' ).show();
      }
      else if ( $(this).find( 'option:selected' ).val() > SSData.fullAge ) {
        $( '.next-step-two_over' ).show();
      }
      else {
        $( '.next-step-two_equal' ).show();
      }

      // Scroll response into view if it's not visible
      if ( isElementInView( '#age-selector-response' ) === false ) {
        $( 'html, body' ).animate({
            scrollTop: $("#retirement-age-selector").offset().top - 20
        }, 300);
      }

    });

    // Helpful button
    $( '#age-selector-response .helpful-btn' ).click( function() {
      $( '#age-selector-response .thank-you' ).show();
      $( '#age-selector-response .helpful-btn' ).attr( 'disabled', true).addClass( 'btn__disabled' ).hide();
    });

    // reformat salary
    $( '#salary-input' ).blur( function() {
      var salary = numToMoney( $( '#salary-input' ).val().replace(/\D/g,'' ) )
      $( '#salary-input' ).val( salary );
    });

    // reformat date fields
    $( '.birthdate-inputs' ).blur( function() {
      var month = $( '#bd-month' ).val().replace( /\D/g,'' ),
          day = $( '#bd-day' ).val().replace( /\D/g,'' ),
          year = $( '#bd-year' ).val().replace( /\D/g,'' );
    });

    // Check if the estimate is ready
    $( '.birthdate-inputs, #salary-input' ).keyup( function() {
      graphView.checkEstimateReady();
    });

    // Initialize the app
    this.redrawGraph();

    // Window resize handler
    $( window ).resize( function() {
      if ( $( '#tooltip-container' ).is( ':visible' ) ) {
        $( '#tooltip-container' ).hide();
        toolTipper( $( '[data-tooltip-current-target]' ) );
      }
      graphView.redrawGraph();
    });

    // Hamburger menu
    $( '.toggle-menu' ).on( 'click', function( ev ) {
        ev.preventDefault();
        $( 'nav.main ul' ).toggleClass( 'vis' );
    });
  },

  checkEstimateReady: function() {
    /***-- checkEstimateReady(): checks if the page is ready for the Estimate button to be hit. --***/
    var $button = $( '#get-your-estimates' ),
        m = ( $( '#bd-month' ).val() !== '' ),
        d = ( $( '#bd-day' ).val() !== '' ),
        y = ( $( '#bd-year' ).val() !== '' ),
        s = ( $( '#salary-input' ).val() !== '' );
    if ( m && d && y && s ) {
      $button.attr( 'disabled', false).removeClass( 'btn__disabled' );
    }
    else {
      $button.attr( 'disabled', true).addClass( 'btn__disabled' );
    }
  },

  highlightAgeFields: function( bool ) {
    var $ageFields = $( '#bd-day, #bd-month, #bd-year' );
    if ( bool ) {
      $ageFields.addClass( 'notification-input__warning' );
    } else {
      $ageFields.removeClass( 'notification-input__warning' );
    }
  },

  isElementInView: function( selector ) {
    var $ele = $( selector ),
        target;
    if ( $ele.offset().top > $(window).scrollTop() + $(window).height() - 150 ) {
      return false;
    }
    else {
      return true;
    }
  },

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

  getYourEstimates: function() {
    var dataLang = $( "body" ).attr('data-lang'),
        dates = this.validateBirthdayFields(),
        salary = $( '#salary-input' ).val().replace(/\D/g,'' ),
        SSData;

    // Hide warnings, show loading indicator
    $( '.cf-notification' ).slideUp();
    this.highlightAgeFields( false );
    $( '#api-data-loading-indicator' ).css( 'display', 'inline-block' );
    $.when( fetch.apiData( dates.concat, salary, dataLang ) ).done( function( resp ) {
      if ( resp.error === '' ) {
        SSData = getModelValues.benefits();

        $( '.step-two, #estimated-benefits-input, #graph-container' ).css( 'opacity', 1);
        $( '.step-two .question' ).css( 'display', 'inline-block' );
        $( '.step-three' ).css( 'opacity', 1);
        $( '.step-one-hidden, .step-three .hidden-content' ).show();
        
        questionsView.update( SSData.currentAge );
        graphView.redrawGraph();
        graphView.resetView();
        // Scroll graph into view if it's not visible
        if ( graphView.isElementInView( '#claim-canvas' ) === false ) {
          $( 'html, body' ).animate({
              scrollTop: $( '#estimated-benefits-description' ).offset().top - 20
          }, 300);
        }
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

  toggleMonthlyAnnual: function () {
    /***-- toggleMonthlyAnnual(): toggles the graph text between monthly view and annual view --***/
    var SSData = getModelValues.benefits(),
        benefitsValue = SSData['age' + this.selectedAge];
    if ( $( 'input[name="benefits-display"]:checked' ).val() === 'annual' ) {
      benefitsValue = benefitsValue * 12;
      $( '#graph-container .monthly-view' ).hide();
      $( '#graph-container .annual-view' ).show();
    }
    else {
      $( '#graph-container .monthly-view' ).show();
      $( '#graph-container .annual-view' ).hide();
    }
  },

  /***-- setTextByAge(): Changes text of benefits and age fields based on this.selectedAge --***/
  setTextByAge: function() {
    var gset = this.gset,
        SSData = getModelValues.benefits(),
        x = this.ages.indexOf( this.selectedAge ) * gset.barGut + gset.indicatorLeftSet,
        lifetimeBenefits = numToMoney( ( 85 - this.selectedAge ) * 12 * SSData[ 'age' + this.selectedAge ] ),
        fullAgeBenefitsValue = SSData[ 'age' + SSData.fullAge ],
        benefitsValue = SSData[ 'age' + this.selectedAge ],
        benefitsTop,
        benefitsLeft,
        fullAgeTop,
        fullAgeLeft;

    if ( SSData.currentAge > 62 ) {
      lifetimeBenefits = numToMoney( ( ( 85 - this.selectedAge ) * 12 - SSData.monthsPastBirthday ) *
        SSData[ 'age' + this.selectedAge ] );
    }

    if ( $( '#estimated-benefits-input [name="benefits-display"]:checked' ).val() === 'annual' ) {
      benefitsValue = benefitsValue * 12;
      fullAgeBenefitsValue = fullAgeBenefitsValue * 12;
    }
    this.toggleMonthlyAnnual();

    $( '#claim-canvas .age-text' ).removeClass( 'selected-age' );
    // Set selected-age
    $( '#claim-canvas .age-text[data-age-value="' + this.selectedAge + '"]' ).addClass( 'selected-age' ),

    // set text and position for #benefits-text div
    $( '#benefits-text' ).text( numToMoney( benefitsValue ) );
    benefitsTop = this.bars[ 'age' + this.selectedAge ].attr( 'y' ) - $( '#benefits-text' ).height() - 10;
    benefitsLeft = this.bars[ 'age' + this.selectedAge ].attr( 'x' ) - $( '#benefits-text' ).width() / 2 + gset.barWidth / 2;
    $( '#benefits-text' ).css( 'top', benefitsTop );
    $( '#benefits-text' ).css( 'left', benefitsLeft );

    // set text, position and visibility of #full-age-benefits-text
    $( '#full-age-benefits-text' ).text( numToMoney( fullAgeBenefitsValue ) );
    fullAgeTop = this.bars[ 'age' + SSData.fullAge ].attr( 'y' ) - $( '#full-age-benefits-text' ).height() - 10;
    fullAgeLeft = this.bars[ 'age' + SSData.fullAge ].attr( 'x' ) - $( '#full-age-benefits-text' ).width() / 2 + gset.barWidth / 2;
    $( '#full-age-benefits-text' ).css( 'top', fullAgeTop );
    $( '#full-age-benefits-text' ).css( 'left', fullAgeLeft );
    if ( this.selectedAge === SSData.fullAge ) {
      $( '#full-age-benefits-text' ).hide();
    }
    else {
      $( '#full-age-benefits-text' ).show();
    }

    // set lifetime benefits text
    $( '.lifetime-benefits-value' ).text( lifetimeBenefits );

    // Set extra text for early and full retirement ages
    if ( this.selectedAge === 70 ) {
      $( '.selected-retirement-age-value' ).text( gettext('70') );
    }
    else if ( this.selectedAge === SSData.earlyAge ) {
      $( '.selected-retirement-age-value' ).text( gettext( SSData.earlyRetirementAge ) );
    }
    else if ( this.selectedAge === SSData.fullAge && SSData.currentAge < SSData.fullAge ) {
      $( '.selected-retirement-age-value' ).text( gettext( SSData.fullRetirementAge ) );
    }
    else {
      $( '.selected-retirement-age-value' ).text( gettext( this.selectedAge ) );
    }

    // Graph content
    $( '.graph-content .content-container' ).hide();
    if ( this.selectedAge === 70 ) {
      $( '.graph-content .content-container.max-retirement' ).show();
    }
    else if ( this.selectedAge < SSData.fullAge ) {
      $( '.graph-content .content-container.early-retirement' ).show();
    }
    else {
      $( '.graph-content .content-container.full-retirement' ).show();
    }

    if ( this.selectedAge === SSData.fullAge ) {
      if ( SSData.past_fra ) {
        if ( SSData.currentAge === 70 ) {
          $( '.benefit-modification-text' ).html( gettext('is your maximum benefit claiming age.') );
          $( '.compared-to-full' ).hide();
          }
        else {
          $( '.benefit-modification-text' ).html( gettext('is past your full benefit claiming age.') );
          $( '.compared-to-full' ).hide();
          }
      }
      else {
        $( '.benefit-modification-text' ).html( gettext('is your full benefit claiming age.') );
        $( '.compared-to-full' ).hide();
      }
    }

    else if ( this.selectedAge < SSData.fullAge ) {
      var percent = ( SSData['age' + SSData.fullAge] - SSData['age' + this.selectedAge] ) / SSData['age' + SSData.fullAge];
      percent = Math.abs( Math.round( percent * 100 ) );
      $( '.benefit-modification-text' ).html( gettext('<strong>reduces</strong> your monthly benefit by&nbsp;<strong>') + percent + '</strong>%' );
      $( '.compared-to-full' ).html( gettext( 'Compared to claiming at your full benefit claiming age.' ) );
      $( '.compared-to-full' ).show();
    }
    else if ( this.selectedAge > SSData.fullAge ) {
      var percent = ( SSData['age' + SSData.fullAge] - SSData['age' + this.selectedAge] ) / SSData['age' + SSData.fullAge];
      percent = Math.abs( Math.round( percent * 100 ) );
      $( '.benefit-modification-text' ).html( gettext('<strong>increases</strong> your benefit by&nbsp;<strong>') + percent + '</strong>%' );
      if ( SSData.past_fra ) {
        var comparedToClaimingFullEs = gettext( 'Compared to claiming at' );
        var comparedToClaimingEs = comparedToClaimingFullEs.split( "XXX" );
        $( '.compared-to-full' ).html( comparedToClaimingEs[0] + SSData.fullAge + comparedToClaimingEs[1] );
      } else {
        $( '.compared-to-full' ).html( gettext( 'Compared to claiming at your full benefit claiming age.' ) );
      }
      $( '.compared-to-full' ).show();
    }
  },

  /***-- moveIndicator(dx, dy): Move the pointed indicator based on mouse delta.
    Note: while dy is not used, it is sent by Raphael's element.drag()
  --***/
  moveIndicator: function (dx, dy) {
    var newX = graphView.indicator.odx + dx,
        gset = graphView.gset,
        SSData = getModelValues.benefits();
    // If new position is farther right than the right-most position, set it to the max value.
    if ( newX > gset.barGut * 8 ) {
      newX = gset.barGut * 8;
    }
    // If new position is farther left than the left-most position, set it to the min value.
    if ( newX < 0 ) {
      newX = 0;
    }
    newX = Math.round( newX / ( gset.barGut ) ) * ( gset.barGut ) + gset.indicatorLeftSet;
    graphView.indicator.transform( 't' + newX + ',0' );
    if ( graphView.selectedAge !== Math.round( newX / gset.barGut ) ) {
      graphView.selectedAge = 62 + Math.round( newX / gset.barGut );
      // Don't let the user select an age younger than they are now
      if ( graphView.selectedAge < SSData.currentAge ) {
        graphView.selectedAge = SSData.currentAge;
        graphView.moveIndicatorToAge( graphView.selectedAge, SSData.currentAge );
      }
      graphView.drawBars();
      graphView.setTextByAge();
    }
  },

  /***-- moveIndicatorToAge(age): Uses moveIndicator to move the indicator to age
    NOTE: This function is all that's require to change the chart to a different age
  --***/
  moveIndicatorToAge: function( age, currentAge ) {
    var gset = this.gset;
    age = Number( age );
    currentAge = Number( currentAge );
    if (age >= currentAge) {
      var iPosX = graphView.indicator.transform()[0][1];
      var newX = Math.round( this.ages.indexOf( age ) ) * ( gset.barGut ) + gset.indicatorLeftSet;
      graphView.indicator.odx = iPosX;
      this.moveIndicator( ( newX - iPosX ), 0 );
    } else {
      return false;
    }
  },

 /***-- drawIndicator(): draws the indicator --***/
  drawIndicator: function() {
    var path,
        gset = this.gset,
        SSData = getModelValues.benefits(),
        // greenPath,
        // whiteLines, // vision dreams of passion
        posX;

    // Clear existing indicator, set up new one.
    if ( typeof graphView.indicator === 'object' ) {
      graphView.indicator.remove();
    }
    // draw a new slider line
    if ($(window).width() < 850) {
      graphView.indicator = this.barGraph.circle( 0, gset.graphHeight - 10 , 15);
    } else {
      graphView.indicator = this.barGraph.circle( 0, gset.graphHeight - 20 , 15);
    }
    graphView.indicator.attr( { 'fill': '#F8F8F8', 'stroke': '#919395'})

    // set up initial indicator text and position
    if ( SSData.currentAge === 0 ) {
      this.selectedAge = SSData.fullAge;
    }
    posX = this.ages.indexOf( this.selectedAge ) * gset.barGut + gset.indicatorLeftSet
    graphView.indicator.transform( 't' + posX + ',0' );

    var start = function () {
      var t = this.transform();
      this.odx = t[0][1];
    };

    var up = function() {

    };
    graphView.indicator.drag( this.moveIndicator, start, up );
    this.setTextByAge();
  },

  /**
    *
    */
  setGraphDimensions: function() {
    // Graph width settings
    var canvasLeft = Number( $( '#claim-canvas' ).css( 'left' ).replace( /\D/g, '' ) );
    canvasLeft += Number( $( '#claim-canvas' ).css( 'padding-left' ).replace( /\D/g, '' ) );

    this.gset.graphWidth = $( '.canvas-container' ).width() - canvasLeft;
    if ( this.gset.graphWidth > ( ( $( window ).width() - canvasLeft ) ) * .95 )  {
      this.gset.graphWidth = ( $(window).width() - canvasLeft ) * .95;
    }

    if ($(window).width() < 850) {
      this.gset.graphHeight = 210;
      $( '#claim-canvas svg' ).css( 'overflow', 'visible' );
    } else if ($(window).width() >= 850 && $(window).width() < 1045) {
      this.gset.graphHeight = 380;
    } else {
      this.gset.graphHeight = 380;
    }
    // $( '.selected-retirement-age-container' ).css( 'margin-top', this.gset.graphHeight + 75 + 'px' );

    this.gset.barWidth = Math.floor( this.gset.graphWidth / 17 );
    this.gset.gutterWidth = Math.floor( this.gset.graphWidth / 17 );
    this.gset.indicatorWidth = 30;
    this.gset.indicatorSide = 19;

    this.gset.barGut = this.gset.barWidth + this.gset.gutterWidth;
    this.gset.indicatorLeftSet = Math.ceil( ( this.gset.barWidth - this.gset.indicatorWidth ) / 2 ) + ( this.gset.indicatorWidth / 2 ) + 1;
    this.barGraph.setSize( this.gset.graphWidth, this.gset.graphHeight );
    $( '#claim-canvas, .x-axis-label' ).width( this.gset.graphWidth );
  },

  /***-- drawBars(): draws and redraws the indicator bars for each age --***/
  drawBars: function() {
    var SSData = getModelValues.benefits();
    if ($(window).width() < 850) {
      this.gset.barOffset = 52;
    } else {
      this.gset.barOffset = 94;
    }
    var leftOffset =  0;
    var heightRatio = ( this.gset.graphHeight - this.gset.barOffset ) / SSData['age70'];
    $.each( this.ages, function(i, val) {
      var color = '#e3e4e5',
          key = 'age' + val,
          height = heightRatio * SSData[key],
          gset = graphView.gset;
      if ( graphView.bars[key] !== undefined ) {
        graphView.bars[key].remove();
      }
      graphView.bars[key] = graphView.barGraph.rect(
        leftOffset,
        gset.graphHeight - gset.barOffset - height,
        gset.barWidth,
        height
      );
      leftOffset = leftOffset + gset.barGut;
      if ( val >= SSData.fullAge ) {
        color = '#aedb94';
      }
      graphView.bars[key].attr( 'stroke', color);
      graphView.bars[key].attr( 'fill', color);
      $( graphView.bars[key].node ).attr( 'data-age', val );
      graphView.bars[key].data( 'age', val );
      graphView.bars[key].click( function() {
        graphView.moveIndicatorToAge( graphView.bars[key].data( 'age' ), SSData.currentAge );
      });
    });
  },

  /***-- drawGraphBackground(): draws the background lines for the chart --***/
  drawGraphBackground: function() {
    var gset = this.gset,
        barInterval = gset.graphHeight / 4,
        totalWidth = ( gset.barWidth * 9 ) + ( gset.gutterWidth * 8 ),
        yCoord = gset.graphHeight - barInterval,
        path;

    // remove existing background
    if ( typeof this.graphBackground === 'object' && typeof this.graphBackground.remove !== 'undefined' ) {
      this.graphBackground.remove();
    }
    // draw a new background
    for ( var i = 1; i <= 5; i++ ) {
      path = path + 'M 0 ' + yCoord + ' H' + totalWidth;
      yCoord = gset.graphHeight - Math.round( barInterval * i ) + 1;
    }
    this.graphBackground = this.barGraph.path( path );
    this.graphBackground.attr( 'stroke', '#E3E4E5' );

    // remove existing slider line
    if ( typeof this.sliderLine === 'object' && typeof this.sliderLine.remove !== 'undefined' ) {
      this.sliderLine.remove();
    }

    // draw a new slider line
    if ($(window).width() < 850) {
      this.sliderLine = this.barGraph.path( 'M0 ' + ( gset.graphHeight - 10 ) + ' H' + totalWidth );
    } else {
      this.sliderLine = this.barGraph.path( 'M0 ' + ( gset.graphHeight - 20 ) + ' H' + totalWidth );
    }
    this.sliderLine.attr( { 'stroke': '#E3E4E5', 'stroke-width': 5 } )
  },

  /**
    *
    */
  drawAgeBoxes: function() {
    var leftOffset = 0,
        gset = this.gset;
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
      leftOffset = leftOffset + gset.barGut;
    });

    var minAgeLeft = Math.ceil( gset.indicatorLeftSet + ( gset.indicatorWidth - $( '#min-age-text' ).width() ) / 2 );
    $( '#min-age-text' ).css( 'left', minAgeLeft );
    var minAgeRight = Math.ceil( ( this.ages.length - 1 ) * gset.barGut + gset.indicatorLeftSet + ( gset.indicatorWidth - $( '#max-age-text' ).width() ) / 2 );
    $( '#max-age-text' ).css( 'left', minAgeRight );
  },

  /**
    * redrawGraph(): Iterates each drawing function
    */
  redrawGraph: function() {
    var SSData = getModelValues.benefits();
    this.setGraphDimensions();
    this.drawGraphBackground();
    this.drawBars();
    this.drawIndicator();
    this.drawAgeBoxes();
    this.moveIndicatorToAge( this.selectedAge, SSData.currentAge );
  },

  /***-- resetView(): Draws new bars and updates text. For use after new data is received. --***/
  resetView: function() {
    var SSData = getModelValues.benefits();
    this.drawBars();
    this.setTextByAge();
    if ( SSData.currentAge < SSData.fullAge ) {
      this.moveIndicatorToAge( SSData.fullAge, SSData.currentAge );
    }
    else {
      this.moveIndicatorToAge( SSData.currentAge, SSData.currentAge );
    }
    $( '.benefit-selections-area' ).empty();
  }

};

module.exports = graphView;