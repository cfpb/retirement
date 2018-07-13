const gulp = require( 'gulp' );
const gulpChanged = require( 'gulp-changed' );
const gulpImagemin = require( 'gulp-imagemin' );
const configImages = require( '../config' ).images;
const handleErrors = require( '../utils/handleErrors' );

gulp.task( 'images', function() {
  return gulp.src( configImages.src )
    .pipe( gulpChanged( configImages.dest ) )
    .pipe( gulpImagemin() )
    .on( 'error', handleErrors )
    .pipe( gulp.dest( configImages.dest ) );
} );
