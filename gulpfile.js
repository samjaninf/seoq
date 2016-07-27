////////////////////////////////
    //Setup//
////////////////////////////////

// Plugins
var gulp = require('gulp'),
      pjson = require('./package.json'),
      gutil = require('gulp-util'),
      sass = require('gulp-sass'),
      autoprefixer = require('gulp-autoprefixer'),
      cssnano = require('gulp-cssnano'),
      rename = require('gulp-rename'),
      del = require('del'),
      plumber = require('gulp-plumber'),
      pixrem = require('gulp-pixrem'),
      uglify = require('gulp-uglify'),
      imagemin = require('gulp-imagemin'),
      run = require('gulp-run'),
      runSequence = require('run-sequence'),
      browserSync = require('browser-sync');


// Relative paths function
var pathsConfig = function (appName) {
  this.app = "./" + (appName || pjson.name);

  return {
    app: this.app,
    templates: this.app + '/templates',
    css: this.app + '/static/css',
    sass: this.app + '/static/sass',
    fonts: this.app + '/static/fonts',
    images: this.app + '/static/images',
    js: this.app + '/static/js',
  }
};

var paths = pathsConfig();
var path = paths;
var _ = require('gulp-load-plugins')({lazy: false})
////////////////////////////////
    //Tasks//
////////////////////////////////

// Styles autoprefixing and minification
gulp.task('styles', function() {
  return gulp.src(paths.sass + '/**/*.scss')
    .pipe(sass().on('error', sass.logError))
    .pipe(plumber()) // Checks for errors
    .pipe(autoprefixer({browsers: ['last 2 version']})) // Adds vendor prefixes
    .pipe(pixrem())  // add fallbacks for rem units
    .pipe(gulp.dest(paths.css))
    .pipe(rename({ suffix: '.min' }))
    .pipe(cssnano()) // Minifies the result
    .pipe(gulp.dest(paths.css));
});

// Javascript minification
gulp.task('scripts', function() {
  return gulp.src(paths.js + '/project.js')
    .pipe(plumber()) // Checks for errors
    .pipe(uglify()) // Minifies the js
    .pipe(rename({ suffix: '.min' }))
    .pipe(gulp.dest(paths.js));
});

// Image compression
gulp.task('imgCompression', function(){
  return gulp.src([paths.images + '/*.jpg', paths.images + '/*.jpeg', paths.images + '/*.png', paths.images + '/*.gif'])
    .pipe(imagemin()) // Compresses PNG, JPEG, GIF
    .pipe(gulp.dest(paths.images))
});

// Run django server
gulp.task('runServer', function() {
  run('python manage.py runserver 0.0.0.0:8000').exec();
});

// Browser sync server for live reload
gulp.task('browserSync', function() {
    browserSync.init(
      [paths.css + "/*.css", paths.js + "*.js", paths.templates + '*.html'], {
        proxy:  "localhost:8000"
    });
});

// Default task
gulp.task('default', function() {
    runSequence(['styles', 'scripts', 'imgCompression'], 'runServer', 'browserSync');
});

gulp.task('build-js', function() {
  gulp.src([`${path.vendor}/jquery/dist/jquery.js`,
    `${path.vendor}/alertify.js/lib/alertify.min.js`,
    `${path.vendor}/bootstrap/dist/js/bootstrap.js`,
    `${path.vendor}/bootbox.js/bootbox.js`,
    `${path.vendor}/geocomplete/jquery.geocomplete.js`,
    `${path.vendor}/select2/dist/js/select2.js`,
    `${path.vendor}/jquery-validation/dist/jquery.validate.js`,
      `${path.vendor}/angular/angular.js`,
      `${path.vendor}/angular-resource/angular-resource.js`,
      `${path.vendor}/angular-sanitize/angular-sanitize.js`,
      `${path.vendor}/progressbar.js/dist/progressbar.js`,
      `${path.vendor}/html2canvas/build/html2canvas.js` ])
    .pipe(_.plumber({errorHandler: HandlersError}))
    .pipe(_.concat('components.js'))
    .pipe(gulp.dest(path.dist))
    .pipe(_.rename({ extname: '.min.js'}))
    .pipe(_.uglify())
    .pipe(gulp.dest(path.dist))
})

////////////////////////////////
    //Watch//
////////////////////////////////

// Watch
gulp.task('watch', ['default'], function() {
  gulp.watch(paths.sass + '/**/*.scss', ['styles']);
  gulp.watch(paths.js + '/**/*.js', ['scripts']);
  gulp.watch('/bower_components/**/*', ['styles', 'scripts']);
});
