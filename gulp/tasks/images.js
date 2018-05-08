const gulp = require( 'gulp' );
const gulpChanged = require( 'gulp-changed' );
const gulpImagemin = require( 'gulp-imagemin' );
const configImages = require( '../config' ).images;
const imageminGifsicle = require( 'imagemin-gifsicle' );
const imageminJpegtran = require( 'imagemin-jpegtran' );
const imageminOptipng = require( 'imagemin-optipng' );
const imageminSvgo = require( 'imagemin-svgo' );
const handleErrors = require( '../utils/handleErrors' );

gulp.task( 'images', function() {
  return gulp.src( configImages.src )
    .pipe( gulpChanged( configImages.dest ) )
    .pipe( gulpImagemin( [
      imageminGifsicle(),
      imageminJpegtran(),
      imageminOptipng(),
      imageminSvgo()
    ] ) )
    .on( 'error', handleErrors )
    .pipe( gulp.dest( configImages.dest ) );
} );
