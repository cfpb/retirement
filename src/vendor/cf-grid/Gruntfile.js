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
      // banner: grunt.file.read('./node_modules/cf-grunt-config/cfpb-banner.txt'),
    },

    // Define tasks specific to this project here

    copy: {
      'boxsizing': {
        files:
        [{
          src: ['src/vendor/box-sizing-polyfill/boxsizing.htc'],
          dest: 'custom-demo/static/css/boxsizing.htc'
        }]
      }
    },

    less: {
      // Compile src/cf-grid.less for the docs.
      src: {
        options: {
          paths: grunt.file.expand('src/vendor/**'),
          sourceMap: true,
          sourceMapRootpath: '/'
        },
        files: {
          'docs/static/css/main.css': [
            'src/cf-*.less'
          ]
        }
      },
      // Compile a version of cf-grids for CSS use.
      generated: {
        options: {
          paths: grunt.file.expand('src/vendor/**'),
          sourceMap: false
        },
        files: {
          'src-generated/cf-grid-generated.css': [
            'src-generated/cf-grid-generated.less'
          ]
        }
      },
      // Compile a version of cf-grid-generated.less for the custom demo.
      'custom-demo': {
        options: {
          paths: grunt.file.expand('src/vendor/**','src-generated'),
          sourceMap: false
        },
        files: {
          'custom-demo/static/css/custom-demo.css': [
            'custom-demo/static/css/custom-demo.less'
          ]
        }
      }
    }

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
  grunt.registerTask('vendor', ['copy:boxsizing']);
  grunt.registerTask('default', ['less:src', 'less:generated', 'less:custom-demo', 'autoprefixer', 'topdoc:docs']);

};
