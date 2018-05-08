const configClean = require( '../config' ).clean;
const del = require( 'del' );
const gulp = require( 'gulp' );

gulp.task( 'clean', function() {
  return del( configClean.dest );
} );
