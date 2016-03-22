module.exports = function(grunt) {

  'use strict';

  require('time-grunt')(grunt);

  var path = require('path');
  var extend = require('node.extend');


  /**
   * Load the tasks we want to use, which are specified as dependencies in
   * the package.json file of cf-grunt-config.
   */

  // Loads all Grunt tasks in the node_modules directory within the new CWD.
  require('jit-grunt')(grunt, {
    // Below line needed because task name does not match package name
    bower: 'grunt-bower-task'
  })({
    // Options
    pluginsRoot: 'node_modules/cf-grunt-config/node_modules'
  });


  /**
   * Initialize a variable to represent the Grunt task configuration.
   */
  var config = {

    // Define a couple of utility variables that may be used in task options.
    pkg: grunt.file.readJSON('bower.json'),
    env: process.env,
    opt: {
      // Include path to compiled extra CSS for IE7 and below.
      // Definitely needed if this component depends on an icon font.
      // ltIE8Source: 'static/css/main.lt-ie8.min.css',

      // Include path to compiled alternate CSS for IE8 and below.
      // Definitely needed if this component depends on media queries.
      // ltIE9AltSource: 'static/css/main.lt-ie9.min.css',

      // Set whether or not to include html5shiv for demoing a component.
      // Only necessary if component patterns include new HTML5 elements
      html5Shiv: true,

      // Set whether you'd like to use a JS hack to force a redraw in the browser
      // to avoid an IE8 bug where fonts do not appear or appear as boxes on load.
      // ie8FontFaceHack: true,

      // Set a path to a concatenated JS file that you'd like to add before the
      // closing body tag.
      // jsBody: 'static/js/component.min.js',

      // Here's a banner with some template variables.
      // We'll be inserting it at the top of minified assets.
      banner: grunt.file.read('./node_modules/cf-grunt-config/cfpb-banner.txt'),
    },

    // Define tasks specific to this project here
    less: {
      core: {
        options: {
          paths: grunt.file.expand('src/**'),
          sourceMap: true
        },
        files: {
          'demo/static/css/main.css': [
            'src/cf-core.less'
          ]
        }
      }
    },

  };


  /**
   * Define a function that, given the path argument, returns an object
   * containing all JS files in that directory.
   */
  function loadConfig(path) {
    var glob = require('glob');
    var object = {};
    var key;

    glob.sync('*', {cwd: path}).forEach(function(option) {
      key = option.replace(/\.js$/,'');
      object[key] = require(path + option);
      grunt.verbose.writeln("External config item - " + key);
    });

    return object;
  }


  /**
   * Combine the config variable defined above with the results of calling the
   * loadConfig function with the given path, which is where our external
   * task options get installed by npm.
   */
  config = extend(true, loadConfig('./node_modules/cf-grunt-config/tasks/options/'), config);

  grunt.initConfig(config);


  /**
   * Load any project-specific tasks installed in the customary location.
   */
  require('load-grunt-tasks')(grunt);


  /**
   * Create custom task aliases for our component build workflow.
   */
  grunt.registerTask('vendor', ['copy:component_assets', 'copy:docs_assets']);
  grunt.registerTask('default', ['less:core', 'autoprefixer', 'copy:docs', 'topdoc']);

};

module.exports = function(grunt) {

  'use strict';

  require('time-grunt')(grunt);

  var path = require('path');
  var extend = require('node.extend');


  /**
   * Load the tasks we want to use, which are specified as dependencies in
   * the package.json file of cf-grunt-config.
   */

  // Loads all Grunt tasks in the node_modules directory within the new CWD.
  require('jit-grunt')(grunt, {
    // Below line needed because task name does not match package name
    bower: 'grunt-bower-task'
  })({
    // Options
    pluginsRoot: 'node_modules/cf-grunt-config/node_modules'
  });


  /**
   * Initialize a variable to represent the Grunt task configuration.
   */
  var config = {

    // Define a couple of utility variables that may be used in task options.
    pkg: grunt.file.readJSON('bower.json'),
    env: process.env,
    opt: {
      // Include path to compiled extra CSS for IE7 and below.
      // Definitely needed if this component depends on an icon font.
      // ltIE8Source: 'static/css/main.lt-ie8.min.css',

      // Include path to compiled alternate CSS for IE8 and below.
      // Definitely needed if this component depends on media queries.
      // ltIE9AltSource: 'static/css/main.lt-ie9.min.css',

      // Set whether or not to include html5shiv for demoing a component.
      // Only necessary if component patterns include new HTML5 elements
      html5Shiv: true,

      // Set whether you'd like to use a JS hack to force a redraw in the browser
      // to avoid an IE8 bug where fonts do not appear or appear as boxes on load.
      ie8FontFaceHack: true,

      // Set a path to a concatenated JS file that you'd like to add before the
      // closing body tag.
      // jsBody: 'static/js/component.min.js',

      // Here's a banner with some template variables.
      // We'll be inserting it at the top of minified assets.
      banner: grunt.file.read('./node_modules/cf-grunt-config/cfpb-banner.txt'),
    },

    // Define tasks specific to this project here

  };


  /**
   * Define a function that, given the path argument, returns an object
   * containing all JS files in that directory.
   */
  function loadConfig(path) {
    var glob = require('glob');
    var object = {};
    var key;

    glob.sync('*', {cwd: path}).forEach(function(option) {
      key = option.replace(/\.js$/,'');
      object[key] = require(path + option);
      grunt.verbose.writeln("External config item - " + key + ": " + object[key]);
    });

    return object;
  }


  /**
   * Combine the config variable defined above with the results of calling the
   * loadConfig function with the given path, which is where our external
   * task options get installed by npm.
   */
  config = extend(true, loadConfig('./node_modules/cf-grunt-config/tasks/options/'), config);

  grunt.initConfig(config);


  /**
   * Load any project-specific tasks installed in the customary location.
   */
  require('load-grunt-tasks')(grunt);


  /**
   * Create custom task aliases for our component build workflow.
   */
  grunt.registerTask('vendor', ['copy:component_assets', 'copy:docs_assets']);
  grunt.registerTask('default', ['less', 'autoprefixer', 'copy:docs', 'topdoc']);

};

/**
 * cf-expandables
 * https://github.com/cfpb/cf-expandables
 *
 * A public domain work of the Consumer Financial Protection Bureau
 */

(function( $ ) {

  $.fn.expandable = function( userSettings ) {

    return $( this ).each(function() {

      var $this = $( this ),
          $target = $this.find('.expandable_target').not( $this.find('.expandable .expandable_target') ),
          $cueOpen = $this.find('.expandable_cue-open').not( $this.find('.expandable .expandable_cue-open') ),
          $cueClose = $this.find('.expandable_cue-close').not( $this.find('.expandable .expandable_cue-close') ),
          $content = $this.find('.expandable_content').not( $this.find('.expandable .expandable_content') ),
          $groupParent = $this.parents('.expandable-group'),
          accordion = $groupParent.length > 0 && $groupParent.data('accordion');

      if ( accordion ) {
        var $siblings = $this.siblings('.expandable');
      }

      this.init = function() {
        // Todo: recommend using an id on all expandables so that we can use
        // the aria-controls attribute.
        $target.attr( 'aria-controls', $content.attr('id') );
        if ( $this.hasClass('expandable__expanded') ) {
          this.expand( 0 );
        } else {
          this.collapse( 0 );
        }
        $target.on( 'click', $.proxy( this.handleClick, this ) );
      };

      this.handleClick = function( ev ) {
        ev.preventDefault();
        ev.stopPropagation();
        this.toggle();
        if ( accordion ) {
          $siblings.each( function( index, sibling ) {
            sibling.collapse();
          });
        }
      };

      this.toggle = function() {
        if ( $target.attr('aria-pressed') === 'true' ) {
          this.collapse();
        } else {
          this.expand();
        }
      };

      this.expand = function( duration ) {
        $cueOpen.css( 'display', 'none' );
        $cueClose.css( 'display', 'inline' );
        $content.attr( 'aria-expanded', 'true' );
        $target.attr( 'aria-pressed', 'true' );
        if ( typeof duration === 'undefined' ) {
          duration = $.fn.expandable.calculateExpandDuration( $content.height() );
        }
        $this.addClass('expandable__expanded');
        $content.slideDown({
          duration: duration,
          easing: 'easeOutExpo'
        });
      };

      this.collapse = function( duration ) {
        $cueOpen.css( 'display', 'inline' );
        $cueClose.css( 'display', 'none' );
        $content.attr( 'aria-expanded', 'false' );
        $target.attr( 'aria-pressed', 'false' );
        if ( typeof duration === 'undefined' ) {
          duration = $.fn.expandable.calculateCollapseDuration( $content.height() );
        }
        $this.removeClass('expandable__expanded');
        $content.slideUp({
          duration: duration,
          easing: 'easeOutExpo'
        });
      };

      this.init();

    });

  };

  $.fn.expandable.calculateExpandDuration = function( height ) {
    return $.fn.expandable.constrainValue( 450, 900, height * 4 );
  };

  $.fn.expandable.calculateCollapseDuration = function( height ) {
    return $.fn.expandable.constrainValue( 350, 900, height * 2 );
  };

  $.fn.expandable.constrainValue = function( min, max, duration ) {
    if ( duration > max ) {
        return max;
    } else if ( duration < min ) {
        return min;
    } else {
        return duration;
    }
  };

  // Auto init
  $('.expandable').expandable();

}(jQuery));
