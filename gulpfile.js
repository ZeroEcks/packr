'use strict';

var gulp = require('gulp');
var sass = require('gulp-sass');
var jshint = require('gulp-jshint');
var concat = require('gulp-concat');
var concatCss = require('gulp-concat-css');

// Sources
var angularLibsJs = [
    'packr/static/libs/angular/angular.js',
    'packr/static/libs/angular-animate/angular-animate.js',
    'packr/static/libs/angular-aria/angular-aria.js',
    'packr/static/libs/angular-material/angular-material.js',
    'packr/static/libs/angular-messages/angular-messages.js',
    'packr/static/libs/angular-route/angular-route.js'
];
var angularLibsCss = [
    'packr/static/libs/angular-material/angular-material.css',
    'packr/static/libs/angular-material/angular-material.layouts.css'
];
var images = [
    'packr/static/img/**/*'
];
var angularAppJs = ['packr/static/app/**/*.js'];
var angularAppScss = ['packr/static/css/*.scss'];

// Tasks
gulp.task('jshint', function () {
    return gulp.src(angularAppJs)
        .pipe(jshint())
        .pipe(jshint.reporter('jshint-stylish'))
        .pipe(jshint.reporter('fail'));
});

gulp.task('watch', function () {
    gulp.watch(angularAppJs, ['jshint', 'concat-app-js']);
    gulp.watch(angularAppScss, ['sass']);
});

gulp.task('concat-app-js', function () {
    return gulp.src(angularAppJs)
        .pipe(concat('app-bundle.js'))
        .pipe(gulp.dest('packr/static/public/')) ;
});

gulp.task('sass', function () {
    return gulp.src(angularAppScss)
        .pipe(sass().on('error', sass.logError))
        .pipe(concatCss('app-bundle-styles.css'))
        .pipe(gulp.dest('packr/static/public/'));
});

gulp.task('concat-libs-css', function () {
    return gulp.src(angularLibsCss)
        .pipe(concatCss('libs-bundle-styles.css'))
        .pipe(gulp.dest('packr/static/public/'));
});

gulp.task('concat-libs-js', function () {
    return gulp.src(angularLibsJs)
        .pipe(concat('libs-bundle.js'))
        .pipe(gulp.dest('packr/static/public/'));
});

gulp.task('move-images', function () {
   return gulp.src(images)
       .pipe(gulp.dest('packr/static/public/img/'))
});

gulp.task('build-app', ['concat-app-js', 'jshint', 'sass', 'concat-libs-js', 'concat-libs-css', 'move-images']);
gulp.task('default', ['jshint', 'build-app', 'watch']);
