const fs = require( 'fs' );

/**
 * Set up file paths
 */
const loc = {
  src:  './src',
  dist: './retirement_api/static/retirement',
  lib:  './node_modules',
  test: './test'
};

module.exports = {
  // eslint-disable-next-line no-sync
  pkg: JSON.parse( fs.readFileSync( 'package.json' ) ),
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
      loc.src + '/js/*.js'
    ],
    dest: loc.dist + '/js/',
    name: 'main.js'
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
        '!' + loc.lib + '/**/*.html'
      ],
      dest: loc.dist
    },
    fonts: {
      src:  loc.lib + '/cf-icons/src/fonts/*',
      dest: loc.dist + '/fonts/'
    },
    icons: {
      src:  loc.lib + '/cf-icons/src/icons/*',
      dest: loc.dist + '/icons/'
    },
    vendorjs: {
      src: [
        loc.lib + '/html5shiv/dist/html5shiv-printshiv.min.js'
      ],
      dest: loc.dist + '/js/'
    }
  }
};
