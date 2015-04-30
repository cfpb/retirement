
// var CFPBClaimingSocialSecurity = ( function($) {
  var SSData = {
    'fullAge': 67,
    'age 62': 1800,
    'age 63': 2000,
    'age 64': 2200,
    'age 65': 2400,
    'age 66': 2650,
    'age 67': 3000,
    'age 68': 3200,
    'age 69': 3400,
    'age 70': 3600,
    'earlyAge': "62 and 1 month"
  };

  // Raphael object
  var barGraph;

  // Raphael elements
  var indicator,
      minAgeText,
      maxAgeText;
  var bars = {};

  // Graph settings
  if ($(window).width() < 768) {
    var barGraphHeight = 240,
      gutterWidth = 10,
      barWidth = ($(window).width() - 40 - (gutterWidth * 8)) / 9,
      indicatorWidth = 40,
      indicatorSide = 60,
      graphWidth = 400; 
  }

  else if ($(window).width() >= 768 && $(window).width() < 1051) {
    var barGraphHeight = 240,
      gutterWidth = 10,
      barWidth = (($(window).width() * 0.66666) - 40 - (gutterWidth * 8)) / 9,
      indicatorWidth = 40,
      indicatorSide = 60,
      graphWidth = 400; 
  }

  else {
    var barGraphHeight = 240,
      barWidth = 25,
      gutterWidth = 30,
      indicatorWidth = 40,
      indicatorSide = 60,
      graphWidth = 400;      
  }

  var barGut = barWidth + gutterWidth, // Useful for quick calculations in graph
      indicatorLeftSet = ( barWidth - indicatorWidth ) / 2;

  // global vars
  var ages = [62,63,64,65,66,67,68,69,70],
      selectedAge = 67,
      currentAge = 0;

  //-- Delay calculations after keyup --//
  var delay = (function(){ 
    var t = 0;
    return function(callback, delay) {
      clearTimeout(t);
      t = setTimeout(callback, delay);
    };
  })(); // end delay()

  //--*** numToMoney(n): Convert from number to money string --//
  function numToMoney(n) { 
    // When n is a string, we should, ironically, strip its numbers first.
    if (typeof n === 'string') {
        n =  Number(n.replace(/[^0-9\.]+/g,""));
    }
    var t = ",";
    if (n < 0) {
      var s = "-";
    }
    else {
      var s = "";
    }
    var i = parseInt(n = Math.abs(+n || 0).toFixed(0)) + "";
    var j = 0;
    if (i.length > 3) {
      j = ((i.length) % 3);
    }
    money = "$" + s;
    if (j > 0) {
      money += i.substr(0,j) + t;
    }
    money += i.substr(j).replace(/(\d{3})(?=\d)/g, "$1" + t);
    return money;
  }

  function calculateAge( month, day, year ) {
    var now = new Date();
    var birthdate = new Date(year, Number(month) - 1, day);
    var age = now.getFullYear() - birthdate.getFullYear();
    var m = now.getMonth() - birthdate.getMonth();
    if ( m < 0 || ( m === 0 && now.getDate() < birthdate.getDate() ) ) {
      age--;
    }
    return age;
  }

  //--*** enforceRange(n, min, max): enforce range of 'min' to 'max' on variable 'n' ***--/
  // Note: If min or max is 'false' then that min or max is not enforced
  function enforceRange(n, min, max) {
    if ( n > max && max !== false ) {
      n = max;
    }
    if ( n < min && min !== false ) {
      n = min;
    }
    return n;
  }

  function validDates( month, day, year ) {
    // get parts of birthday and salary, strip non-numeric strings
    var monthMaxes = { '1': 31, '2': 29, '3': 31, '4': 30, '5': 31, '6': 30,
        '7': 31, '8': 31, '9': 30, '10': 31, '11': 30, '12': 31 };
    month = enforceRange( Number( month.toString().replace(/\D/g,'') ), 1, 12 );
    day = enforceRange( Number( day.toString().replace(/\D/g,'') ), 1, monthMaxes[ month.toString() ] );
    if ( Number(year) < 100 ) {
      year = Number(year) + 1900;
    }
    year = enforceRange( Number( year.toString().replace(/\D/g,'') ), 1900, new Date().getFullYear() );
    return { 'month': month, 'day': day, 'year': year, 'concat': month + '-' + day + '-' + year };
  }

  //--*** getData(): performs a get call, sets SSData with incoming data ***--//
  function getData() {
    var day = $('#bd-day').val(),
        month = $('#bd-month').val(),
        year = $('#bd-year').val(),
        salary = $('#salary-input').val().replace(/\D/g,'');
    var dates = validDates( month, day, year );
    // var url = '/retirement-testing/api.php?birthday=' + dates.concat + '&salary=' + Number(salary);
    var url = '/retirement/retirement-api/estimator/' + dates.concat + '/' + Number(salary) + '/';
    var response = "";
    currentAge = calculateAge( month, day, year );
    if ( currentAge < 50 ) {
      $('.lifestyle-btn.age-split').each( function() {
        $(this).val( $(this).attr('data-base-value') + '-under50' );
      });
    }
    else {
      $('.lifestyle-btn.age-split').each( function() {
        $(this).val( $(this).attr('data-base-value') + '-over50' );
      });    
    }
    $.get( url )
      .done( function( dump ) {
        var data = dump.data;
        if ( dump.error === "" ) {
          SSData = data.benefits;
          SSData.fullAge = data['full retirement age'];
          SSData.earlyAge = data['early retirement age'];
          resetView();
          $('.step-two, #estimated-benefits-input, #graph-container').css('opacity', 1);
          $('.step-two .question').css('display', 'inline-block');
        }
        else {
          alert('An error occurred! ' + dump.error )
          response = "error";
        }
      })
      .error( function(xhr, status, error) {
        alert("An AJAX error occured: " + status + "\nError: " + error + "\nError detail: " + xhr.responseText);
        response = "error";
      });
      return response;
  }

  function toggleMonthlyAnnual() {
    var benefitsValue = SSData['age ' + selectedAge];
    if ( $('input[name="benefits-display"]:checked').val() === 'annual' ) {
      benefitsValue = benefitsValue * 12;
      $('#graph-container .monthly-view').hide();
      $('#graph-container .annual-view').show();
    }
    else {
      $('#graph-container .monthly-view').show();
      $('#graph-container .annual-view').hide();
    }
  }

  //--*** setTextByAge(): Changes text of benefits and age fields based on selectedAge
  function setTextByAge() {
    var x = ages.indexOf( selectedAge ) * barGut + indicatorLeftSet;
    var lifetimeBenefits = numToMoney( ( 85 - selectedAge ) * 12 * SSData[ 'age ' + selectedAge ] );
    var benefitsValue = SSData['age ' + selectedAge];
    if ( $('#estimated-benefits-input [name="benefits-display"]:checked').val() === 'annual' ) {
      benefitsValue = benefitsValue * 12;
    }
    toggleMonthlyAnnual();

    var ageTextLeft = x + ( indicatorWidth - $('#selected-age-text').width() ) / 2;
    $('#selected-age-text').text( selectedAge ).css( 'left', ageTextLeft );
    $('#benefits-text').text( numToMoney( benefitsValue ) );
    var benefitsTop = bars[ 'age ' + selectedAge ].attr('y') - $('#benefits-text').height() - 10;
    $('#benefits-text').css( 'top', benefitsTop );
    var benefitsLeft = bars[ 'age ' + selectedAge ].attr('x') - $('#benefits-text').width() / 2 + barWidth / 2;
    $('#benefits-text').css( 'left', benefitsLeft );
    $('.lifetime-benefits-value').text( lifetimeBenefits );
  }

  /***-- moveIndicator(dx, dy): Move the pointed indicator based on mouse delta.
    Note: while dy is not used, it is sent by Raphael's element.drag()
  --***/
  function moveIndicator(dx, dy) {
    var newX = indicator[0].odx + dx;
    if ( newX > graphWidth + barGut ) {
      newX = graphWidth + barGut;
    }
    if ( newX < 0 ) {
      newX = 0;
    }
    newX = Math.round( newX / ( barGut ) ) * ( barGut ) + indicatorLeftSet;
    indicator.transform('t' + newX + ',0');
    if ( selectedAge !== Math.round( newX / barGut ) ) {
      selectedAge = 62 + Math.round( newX / barGut );
      var key = 'age ' + selectedAge;
      setTextByAge();
      drawBars();
    }
  };

  /***-- moveIndicatorToAge(age): Uses moveIndicator to move the indicator to age --***/
  function moveIndicatorToAge( age ) {
    age = Number( age );
    var iPosX = indicator[0].transform()[0][1];
    var newX = Math.round( ages.indexOf( age ) ) * ( barGut ) + indicatorLeftSet;
    indicator[0].odx = iPosX;
    moveIndicator( ( newX - iPosX ), 0 );
  }

  function createIndicator() {
    var greenPath,
        whiteBox,
        posX;
    indicator = barGraph.set();
    
    // greenPath outlines and fills the indicator handle
    greenPath = barGraph.path( 'M0 380 H40 V320 L20 300 L0 320 V380' )
    greenPath.attr( { 'fill': '#34b14f', 'stroke': '#34b14f' } ) ;
    
    // whiteBox creates the white box for text in the indicator handle
    whiteBox = barGraph.rect(5, 325, 30, 25 );
    whiteBox.attr( { 'fill': '#fff', 'stroke': '#fff' } );

    // greenPath and whiteBox are added to the indicator set
    indicator.push( greenPath, whiteBox );

    // set up initial indicator text and position
    selectedAge = SSData.fullAge;
    posX = ages.indexOf( selectedAge ) * barGut + indicatorLeftSet  
    indicator.transform('t' + posX + ',0' );
    selectedAge = SSData.fullAge;

    var start = function () {
      var t = this.transform();
      this.odx = t[0][1];
    };

    var up = function() {

    };
    indicator.drag( moveIndicator, start, up );
    setTextByAge();
  }

  function drawBars() {
    var leftOffset =  0;
    var heightRatio = barGraphHeight / SSData['age 70'];
    $.each( ages, function(i, val) {
      var color = '#e3e4e5';
      var key = 'age ' + val;
      var height = heightRatio * SSData[key];
      if ( bars[key] !== undefined ) {
        bars[key].remove();
      }
      bars[key] = barGraph.rect( leftOffset, 282 - height, barWidth, height);
      leftOffset = leftOffset + barGut;
      if ( val >= SSData.fullAge ) {
        color = '#aedb94';
      }
      if ( val === selectedAge ) {
        color = '#34b14f';
      }
      bars[key].attr('stroke', color);
      bars[key].attr('fill', color);
      bars[key].data( 'age', val );
      bars[key].click( function() {
        moveIndicatorToAge( bars[key].data( 'age' )  );
      });
    });
  }

  function drawParts() {
    drawBars();
    createIndicator();
    $('#claim-canvas').width( barWidth * 9 + gutterWidth * 8 );

    var minAgeLeft = indicatorLeftSet + ( indicatorWidth - $('#min-age-text').width() ) / 2 
    $('#min-age-text').css( 'left', minAgeLeft );
    var minAgeRight = ( ages.length - 1 ) * barGut + indicatorLeftSet + ( indicatorWidth - $('#max-age-text').width() ) / 2 
    $('#max-age-text').css( 'left', minAgeRight );
  }

  function resetView() {
    drawBars();
    setTextByAge();
    moveIndicatorToAge( SSData.fullAge );
    $('.benefit-selections-area').empty();
    $('#add-to-comparison-button').click();
  }

  $(document).ready( function() {
    
    barGraph = new Raphael( $("#claim-canvas")[0] , 600, 400 );
    $('#claim-canvas svg').css('overflow', 'visible')
  
    // Event handlers
    $('input[name="benefits-display"]').click( function() {
      setTextByAge();
    });

    $('#get-your-estimates').click( function() {
      getData();
    });

    $('#add-to-comparison-button').click( function() {
      if ( $('.benefit-selections-area .benefit-selection').length < 4 ) {
        var html = '<div class="benefit-selection">\
                  <button class="selected-remove">Remove <span class="cf-icon cf-icon-delete-round"></span></button>\
                  <p class="selected-age">67 and something</p>\
                  <p class="selected-full-retirement">Full retirement</p>\
                  <p class="selected-amount"><span class="monthly-view">$1,000</span><span class="annual-view">$12,000</span></p>\
                </div>';
        $benefitDiv = $(html);

        var monthlyBenefit = numToMoney( SSData[ 'age ' + selectedAge ] );
        $benefitDiv.find('.selected-age').text( 'Age ' + selectedAge );
        if ( Number( selectedAge ) === 62 ) {
          $benefitDiv.find('.selected-age').text( 'Age ' + SSData.earlyAge );
        }
        $benefitDiv.find('.monthly-view').text( numToMoney( SSData[ 'age ' + selectedAge ] ) );
        $benefitDiv.find('.annual-view').text( numToMoney( SSData[ 'age ' + selectedAge ] * 12 ) );
        if ( selectedAge === SSData.fullAge ) {
          $benefitDiv.find('selected-full-retirement').show();
        }
        $('.benefit-selections-area').append( $benefitDiv );
        toggleMonthlyAnnual();
      }
    });

    $('.benefits-comparison').on( 'click', '.selected-remove', function() {
      var t = $(this).parents('.benefit-selection').remove();
    });

    $(document).keypress( function(ev) {
      if ( ev.which == 58 ) {
        $.each( bars, function(i ,val ) {
          var rot = 360;
          if ( this.transform().length !== 0 ) {
            rot = this.transform()[0][1] + 360;
          }
          this.animate( { transform: 'r' + rot }, 2000 ) ;
        })
      }
    });

    $(document).keypress( function(ev) {
      if ( ev.which === 55 && ev.ctrlKey === true ) {
        $('#bd-day').val("7");
        $('#bd-month').val("7");
        $('#bd-year').val("1977");
        $('#salary-input').val("70000");
        $('#get-your-estimates').click();
      }
    });

    $('.step-two .question .lifestyle-btn').click(function() {
      var $container = $(this).closest( '.question' );
      var respTo = $(this).val();
      $container.find('.lifestyle-img').slideUp();
      $container.find('.lifestyle-response').not('[data-responds-to="' + respTo + '"]').slideUp();
      $container.find('.lifestyle-response[data-responds-to="' + respTo + '"]').slideDown();

      $container.attr('data-answered', 'yes');
      if ( $('.step-two .question[data-answered="yes"]').length === 5 ) {
        $('.step-three').css('opacity', 1);
        $('.step-three .hidden-content').show();
      }
    })

    $('#retirement-age-selector').change( function() {
      $('#age-selector-response').show();
      $('#age-selector-response .age-response-value').text( $(this).find('option:selected').val() );
    });

    $('#age-selector-response .helpful-btn').click( function() {
      $('#age-selector-response .thank-you').show();
      $('#age-selector-response .helpful-btn').attr('disabled', true).addClass('btn__disabled');
    });

    $('#salary-input').blur( function() {
      var salary = numToMoney( $( '#salary-input' ).val().replace(/\D/g,'') )
      $('#salary-input').val( salary );
    });

    $('.birthdate-inputs').blur( function() {
      var month = $( '#bd-month' ).val().replace(/\D/g,''),
          day = $( '#bd-day' ).val().replace(/\D/g,''),
          year = $( '#bd-year' ).val().replace(/\D/g,'');

    });

    // Initialize the app
    $('#graph-container').css('height', $('#graph-container').height() );
    drawParts();
    $('#add-to-comparison-button').click(); // add initial value to comparison

    if ( location.hash === '#B' ) {
      $('.version-a').hide();
      $('.version-b').show();
      $('.step-one').css('border-top', '1px solid #e3e3e1')
    }

  });
// })(jQuery);