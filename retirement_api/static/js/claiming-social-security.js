
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
      indicatorWidth = 36,
      indicatorSide = 30,
      graphWidth = 400; 
  }

  else if ($(window).width() >= 768 && $(window).width() < 1051) {
    var barGraphHeight = 240,
      gutterWidth = 10,
      barWidth = (($(window).width() * 0.66666) - 40 - (gutterWidth * 8)) / 9,
      indicatorWidth = 36,
      indicatorSide = 30,
      graphWidth = 400; 
  }

  else {
    var barGraphHeight = 240,
      barWidth = 38,
      gutterWidth = 40,
      indicatorWidth = 36,
      indicatorSide = 30,
      graphWidth = 600;      
  }

  var barGut = barWidth + gutterWidth, // Useful for quick calculations in graph
      indicatorLeftSet = Math.ceil( ( barWidth - indicatorWidth ) / 2 );

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
          $('.step-three').css('opacity', 1);
          $('.step-three .hidden-content').show();
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

  //--*** toolTipper(): Handles tooltips ***--//

  function toolTipper( target ) {
    // position tooltip-container based on the element clicked
    var tooltip = $('.tooltip-container[data-target="' + target + '"]');
    var thisoff = tooltip.offset();
    var ttc = $("#tooltip-container");
    ttc.show();
    ttc.css(
        {"left": (thisoff.left + 10) + "px",
         "top": (thisoff.top + $(this).height() + 5) + "px"});
    var ttcoff = ttc.offset();
    var right = ttcoff.left + ttc.outerWidth(true);
    if (right > $(window).width()) {
        var left = $(window).width() - ttc.outerWidth(true) - 20;
        ttc.offset({"left": left});
    }
    // check offset again, properly set tips to point to the element clicked
    ttcoff = ttc.offset();
    var tipset = Math.max(thisoff.left - ttcoff.left, 0);
    ttc.find(".innertip").css("left", (tipset + 8));
    ttc.find(".outertip").css("left", (tipset + 5));
    $("#tooltip-container > p").html($(this).attr("data-tooltip"));
    
    $("html").on('click', "body", function() {
        $("#tooltip-container").hide();
        $("html").off('click');
    });
    var tooltip = $(this).attr("data-tipname");
    if ( tooltip == undefined ){
        tooltip = "Name not found";
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
    $('#claim-canvas .age-text').removeClass('selected-age');
    var selectedAgeDiv = $('#claim-canvas .age-text[data-age-value="' + selectedAge + '"]').addClass('selected-age');
    $('#benefits-text').text( numToMoney( benefitsValue ) );
    var benefitsTop = bars[ 'age ' + selectedAge ].attr('y') - $('#benefits-text').height() - 10;
    $('#benefits-text').css( 'top', benefitsTop );
    var benefitsLeft = bars[ 'age ' + selectedAge ].attr('x') - $('#benefits-text').width() / 2 + barWidth / 2;
    $('#benefits-text').css( 'left', benefitsLeft );
    $('.lifetime-benefits-value').text( lifetimeBenefits );

    $('.selected-retirement-age-value').text( selectedAge );
    if ( selectedAge === SSData.fullAge ) {
      $('.benefit-modification-text').html( 'is your full retirement age.' )
      $('.compared-to-full').hide();
    }
    else if ( selectedAge < SSData.fullAge ) {
      var percent = ( SSData['age ' + SSData.fullAge] - SSData['age ' + selectedAge] ) / SSData['age ' + SSData.fullAge];
      percent = Math.abs( Math.floor( percent * 100 ) );
      $('.benefit-modification-text').html( '<strong>reduces</strong> your benefit by ' + percent + '%' );
      $('.compared-to-full').show();
    }
    else if ( selectedAge > SSData.fullAge ) {
      var percent = ( SSData['age ' + SSData.fullAge] - SSData['age ' + selectedAge] ) / SSData['age ' + SSData.fullAge];
      percent = Math.abs( Math.floor( percent * 100 ) );
      $('.benefit-modification-text').html( '<strong>increases</strong> your benefit by ' + percent + '%' );
      $('.compared-to-full').show();
    }
  }

  /***-- moveIndicator(dx, dy): Move the pointed indicator based on mouse delta.
    Note: while dy is not used, it is sent by Raphael's element.drag()
  --***/
  function moveIndicator(dx, dy) {
    var newX = indicator[0].odx + dx;
    if ( newX > barGut * 8 ) {
      newX = barGut * 8;
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
        whiteLines, // vision dreams of passion
        posX;
    indicator = barGraph.set();
    
    // greenPath outlines and fills the indicator handle
    greenPath = barGraph.path( 'M0 380 H34 V350 L17 345 L0 350 V380' )
    greenPath.attr( { 'fill': '#34b14f', 'stroke': '#34b14f' } ) ;
    
    // whiteLines are the three lines on the indicator handle
    whiteLines = barGraph.path( 'M12 370 V360 M17 372.5 V357.5 M22 370 V360');
    whiteLines.attr( { 'fill': '#fff', 'stroke': '#fff' } );

    // greenPath and whiteLines are added to the indicator set
    indicator.push( greenPath, whiteLines );

    // set up initial indicator text and position
    selectedAge = SSData.fullAge;
    posX = ages.indexOf( selectedAge ) * barGut + indicatorLeftSet  
    indicator.transform( 't' + posX + ',0' );
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
    $('#claim-canvas').css( 'left', '40px');
    var leftOffset = 0;
    $.each( ages, function(i, val) {
      $('#claim-canvas').append('<div class="age-text"><p class="h3"><strong>' + val + '<strong></p></div>');
      var ageDiv = $('#claim-canvas .age-text:last');
      ageDiv.attr('data-age-value', val);
      var left = Math.ceil( leftOffset + ( indicatorWidth - ageDiv.width() ) / 2 );
      ageDiv.css('left', left );
      leftOffset = leftOffset + barGut;
    });

    var minAgeLeft = Math.ceil( indicatorLeftSet + ( indicatorWidth - $('#min-age-text').width() ) / 2 );
    $('#min-age-text').css( 'left', minAgeLeft );
    var minAgeRight = Math.ceil( ( ages.length - 1 ) * barGut + indicatorLeftSet + ( indicatorWidth - $('#max-age-text').width() ) / 2 );
    $('#max-age-text').css( 'left', minAgeRight );
  }

  function resetView() {
    drawBars();
    setTextByAge();
    moveIndicatorToAge( SSData.fullAge );
    $('.benefit-selections-area').empty();
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

    $('#claim-canvas .age-text').click( function() {
      console.log('test')
      // var ageValue = $(this).attr('data-age-value');
      // bars['age' + ageValue].click();
    });

    $('.benefits-comparison').on( 'click', '.selected-remove', function() {
      var t = $(this).parents('.benefit-selection').remove();
    });

    $(document).keypress( function(ev) {
      if ( ev.which === 58 ) {
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
      $('.step-two .question .lifestyle-btn').removeClass('active');
      $(this).addClass('active');

      $container.find('.lifestyle-img').slideUp();
      $container.find('.lifestyle-response').not('[data-responds-to="' + respTo + '"]').slideUp();
      $container.find('.lifestyle-response[data-responds-to="' + respTo + '"]').slideDown();

      $container.attr('data-answered', 'yes');

    })

    $('#retirement-age-selector').change( function() {
      $('#age-selector-response').show();
      $('#age-selector-response .age-response-value').text( $(this).find('option:selected').val() );
    });

    $('#age-selector-response .helpful-btn').click( function() {
      $('#age-selector-response .thank-you').show();
      $('#age-selector-response .helpful-btn').attr('disabled', true).addClass('btn__disabled').hide();
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

    if ( location.hash === '#B' ) {
      $('.version-a').hide();
      $('.version-b').show();
      $('.step-one').css('border-top', '1px solid #e3e3e1')
    }

    // Tooltip handler
    $('.tooltip-target').click( function() {
      event.preventDefault();
      event.stopPropagation();
    });

  });
// })(jQuery);