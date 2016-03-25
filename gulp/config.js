'use strict';

var fs = require( 'fs' );

/**
 * Set up file paths
 */
var loc = {
  src:  './src/',
  dist: './retirement_api/static/retirement/',
  lib:  JSON.parse( fs.readFileSync( './.bowerrc' ) ).directory, // eslint-disable-line no-sync, no-inline-comments, max-len
  test: './test'
};

module.exports = {
  pkg:    JSON.parse( fs.readFileSync( 'bower.json' ) ), // eslint-disable-line no-sync, no-inline-comments, max-len
  banner:
      '/*!\n' +
      ' *  <%= pkg.name %> - v<%= pkg.version %>\n' +
      ' *  <%= pkg.homepage %>\n' +
      ' *  Licensed <%= pkg.license %> by Consumer Financial Protection Bureau' +
      ' */',
  lint: {
    src: [
      loc.src + '/js/**/*.js',
      loc.src + '/js/*.js',
      loc.src + '/js/*/*.js',
      '!' + loc.src + '/js/utils/nemo.js'
    ],
    gulp: [
      'gulpfile.js',
      'gulp/**/*.js'
    ]
  },
  test: {
    src:   loc.src + '/js/**/*.js',
    tests: loc.test
  },
  clean: {
    dest: loc.dist
  },
  styles: {
    cwd:      loc.src + '/css',
    src:      '/main.less',
    dest:     loc.dist + '/css',
    settings: {
      paths: [
        loc.lib,
        loc.lib + '/cf-typography/src'
      ],
      compress: true
    }
  },
  scripts: {
    entrypoint: loc.src + '/js/index.js',
    src: [
      loc.lib + '/jquery/dist/jquery.js',
      loc.lib + '/jquery.easing/js/jquery.easing.js',
      loc.lib + '/cf-*/src/js/*.js',
      loc.src + '/js/**/*.js',
      loc.src + '/js/*/*.js',
      loc.src + '/js/*.js',
    ],
    dest: loc.dist + '/js/',
    name: 'main.js'
  },
  browserify: {
    paths: {
      scripts: 'retirement_api/static/retirement/js/claiming-social-security.js',
      dest: 'dist/scripts/'
    }
  },
  images: {
    src:  loc.src + '/img/**',
    dest: loc.dist + '/images'
  },
  templates: {
    src: './retirement_api/templates/**'
  },
  copy: {
    files: {
      src: [
        loc.src + '/**/*.html',
        loc.src + '/**/*.pdf',
        loc.src + '/_*/**/*',
        loc.src + '/robots.txt',
        loc.src + '/favicon.ico',
        '!' + loc.lib + '/**/*.html'
      ],
      dest: loc.dist
    },
    icons: {
      src:  loc.lib + '/cf-icons/src/fonts/*',
      dest: loc.dist + '/fonts/'
    },
    vendorjs: {
      src: [
        loc.lib + '/box-sizing-polyfill/boxsizing.htc',
        loc.lib + '/html5shiv/dist/html5shiv-printshiv.min.js'
      ],
      dest: loc.dist + '/js/'
    }
  }
};
