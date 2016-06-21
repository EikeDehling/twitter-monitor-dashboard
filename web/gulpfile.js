// Include gulp
var gulp = require('gulp'); 

// Include Our Plugins
var jshint = require('gulp-jshint');
var sass = require('gulp-sass');
var concat = require('gulp-concat');
var uglify = require('gulp-uglify');
var rename = require('gulp-rename');
var browserify = require('browserify');
var babelify = require('babelify');
var source = require("vinyl-source-stream");

// Lint Task
/* gulp.task('lint', function() {
    return gulp.src('cluster/js/*.js')
        .pipe(jshint())
        .pipe(jshint.reporter('default'));
}); */

// Compile Our Sass
gulp.task('sass', function() {
    return gulp.src('cluster/scss/*.scss')
        .pipe(sass())
        .pipe(gulp.dest('css'));
});

// Concatenate & Minify JS
gulp.task('scripts', function() {
    return browserify(['index.jsx'])
        .transform(babelify, {presets: ["es2015", "react"]})
        .bundle()
        .pipe(source('bundle.min.js'))
        .pipe(gulp.dest('cluster/static/'));

    /* return gulp.src('cluster/js/*.js')
        .pipe(concat('all.js'))
        .pipe(gulp.dest('dist'))
        .pipe(rename('all.min.js'))
        .pipe(uglify())
        .pipe(gulp.dest('dist')); */
});

// Watch Files For Changes
/* gulp.task('watch', function() {
    gulp.watch('cluster/js/*.js', ['lint', 'scripts']);
    gulp.watch('cluster/scss/*.scss', ['sass']);
}); */

// Default Task
gulp.task('default', ['scripts']);
