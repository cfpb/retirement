const gulp = require( 'gulp' );
const gulpChanged = require( 'gulp-changed' );
const configCopy = require( '../config' ).copy;
const handleErrors = require( '../utils/handle-errors' );

gulp.task( 'copy:files', () => {
  const pipe = gulp.src( configCopy.files.src )
    .pipe( gulpChanged( configCopy.files.dest ) )
    .on( 'error', handleErrors )
    .pipe( gulp.dest( configCopy.files.dest ) );
  return pipe;
} );

gulp.task( 'copy:fonts', () => {
  const pipe = gulp.src( configCopy.fonts.src )
    .pipe( gulpChanged( configCopy.fonts.dest ) )
    .on( 'error', handleErrors )
    .pipe( gulp.dest( configCopy.fonts.dest ) );
  return pipe;
} );

gulp.task( 'copy:icons', () => {
  const pipe = gulp.src( configCopy.icons.src )
    .pipe( gulpChanged( configCopy.icons.dest ) )
    .on( 'error', handleErrors )
    .pipe( gulp.dest( configCopy.icons.dest ) );
  return pipe;
} );

gulp.task( 'copy:vendorjs', () => {
  const pipe = gulp.src( configCopy.vendorjs.src )
    .pipe( gulpChanged( configCopy.vendorjs.dest ) )
    .on( 'error', handleErrors )
    .pipe( gulp.dest( configCopy.vendorjs.dest ) );
  return pipe;
} );

gulp.task( 'copy',
  gulp.parallel(
    'copy:files',
    'copy:fonts',
    'copy:icons',
    'copy:vendorjs'
  )
);
