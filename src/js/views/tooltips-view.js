'use strict';

var tooltipsView = {

  init: function() {
    // Tooltip handler
    $( '[data-tooltip-target]' ).click( function( ev ) {
      ev.preventDefault();
      ev.stopPropagation();
      tooltipsView.toolTipper( $( this ) );
    } );
  },

  toolTipper: function( $elem ) {
    // position tooltip-container based on the element clicked
    var $ttc = $( '#tooltip-container' ),
        $target = $( '[data-tooltip-current-target]' ),
        name = $elem.attr( 'data-tooltip-target' ),
        content = $( '[data-tooltip-name="' + name + '"]' ).html(),
        innerTip = $ttc.find( '.innertip' ),
        outerTip = $ttc.find( '.outertip' ),
        pagePadding = parseInt( $( '#maincontent' ).css( 'padding-left' ), 10 ),
        newTop,
        newLeft,
        elemCenter,
        elemRightOffset;

    $ttc.width( $( '#claiming-social-security' ).width() / 3 );

    $ttc.find( '.content' ).html( content );
    $target.removeAttr( 'data-tooltip-current-target' );
    $elem.attr( 'data-tooltip-current-target', true );

    $ttc.show();
    newTop = $elem.offset().top + $elem.outerHeight() + 10;
    newLeft = $elem.offset().left + $elem.outerWidth() / 2 -
      $ttc.outerWidth( true ) / 2;
    $ttc.css( { top: newTop, left: newLeft } );

    // check offset again, properly set tips to point to the element clicked
    var tipOffset = Math.floor( $ttc.outerWidth() / 2 );
    innerTip.css( 'left', Math.floor( tipOffset - innerTip.outerWidth() / 2 ) );
    outerTip.css( 'left', Math.floor( tipOffset - outerTip.outerWidth() / 2 ) );

    // Prevent tooltip from falling off the left side of screens
    if ( newLeft < pagePadding ) {
      elemCenter = $elem.offset().left + $elem.width() / 2;
      $ttc.css( 'left', pagePadding );
      innerTip.css(
        'left',
        elemCenter - innerTip.outerWidth() / 2 - pagePadding
      );
      outerTip.css(
        'left',
        elemCenter - outerTip.outerWidth() / 2 - pagePadding
      );
    }

    // Prevent tooltip from falling off the right side of screens
    if ( $ttc.offset().left + $ttc.outerWidth( true ) > $( window ).width() ) {
      elemCenter = $elem.offset().left + $elem.width() / 2;
      elemRightOffset = $( window ).width() - elemCenter;
      newLeft = $( window ).width() - $ttc.outerWidth( true ) - pagePadding;
      $ttc.css( 'left', newLeft );
      innerTip.css( 'left', $ttc.outerWidth() - innerTip.outerWidth() / 2 -
        elemRightOffset + pagePadding );
      outerTip.css( 'left', $ttc.outerWidth() - outerTip.outerWidth() / 2 -
        elemRightOffset + pagePadding );
    }

    // if userAgent is an iPhone, iPad, iPod
    if ( /iP/i.test( navigator.userAgent ) ) {
      // make the body clickable
      $( 'body' ).css( 'cursor', 'pointer' );
    }

    $( 'html' ).on( 'click', 'body', function() {
      document.onclick = function() {
        // iPhone Safari fix?
      };
      $ttc.hide();
      $ttc.find( '.content' ).html( '' );
      $( '[data-tooltip-current-target]' )
        .removeAttr( 'data-tooltip-current-target' );
      $( 'html' ).off( 'click' );
      $( 'body' ).css( 'cursor', 'inherit' );
    } );
    $( window ).resize( function() {
      if ( $( '#tooltip-container' ).is( ':visible' ) ) {
        $( '#tooltip-container' ).hide();
        tooltipsView.toolTipper( $( '[data-tooltip-current-target]' ) );
      }
    } );
  }
};

module.exports = tooltipsView;
