const gulp = require( 'gulp' );
const gulpSourcemaps = require( 'gulp-sourcemaps' );
const gulpUglify = require( 'gulp-uglify' );
const browserify = require( 'browserify' );
const source = require( 'vinyl-source-stream' );
const buffer = require( 'vinyl-buffer' );
const configScripts = require( '../config' ).scripts;
const handleErrors = require( '../utils/handleErrors' );

gulp.task( 'scripts', function() {
  const b = browserify( {
    entries: configScripts.entrypoint,
    debug: true
  } );

  return b.bundle()
    .pipe( source( 'main.js' ) )
    .pipe( buffer().on( 'error', handleErrors ) )
    .pipe( gulpSourcemaps.init( { loadMaps: true } ) )
    .pipe( gulpUglify() )
    .pipe( gulpSourcemaps.write( './' ) )
    .pipe( gulp.dest( configScripts.dest ) );
} );
