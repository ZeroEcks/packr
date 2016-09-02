'use strict';

var gulp = require('gulp');
var sass = require('gulp-sass');
var jshint = require('gulp-jshint');
var concat = require('gulp-concat');
var concatCss = require('gulp-concat-css');

// Sources
var angularLibsJs = [
    'app/static/libs/angular/angular.js',
    'app/static/libs/angular-animate/angular-animate.js',
    'app/static/libs/angular-aria/angular-aria.js',
    'app/static/libs/angular-material/angular-material.js',
    'app/static/libs/angular-messages/angular-messages.js',
    'app/static/libs/angular-route/angular-route.js'
];
var angularLibsCss = [
    'app/static/libs/angular-material/angular-material.css',
    'app/static/libs/angular-material/angular-material.layouts.css'
];
var angularAppJs = ['app/static/app/**/*.js'];
var angularAppScss = ['app/static/css/*.scss'];

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
        .pipe(gulp.dest('app/static/public/')) ;
});

gulp.task('sass', function () {
    return gulp.src(angularAppScss)
        .pipe(sass().on('error', sass.logError))
        .pipe(concatCss('app-bundle-styles.css'))
        .pipe(gulp.dest('app/static/public/'));
});

gulp.task('concat-libs-css', function () {
    return gulp.src(angularLibsCss)
        .pipe(concatCss('libs-bundle-styles.css'))
        .pipe(gulp.dest('app/static/public/'));
});

gulp.task('concat-libs-js', function () {
    return gulp.src(angularLibsJs)
        .pipe(concat('libs-bundle.js'))
        .pipe(gulp.dest('app/static/public/'));
});

gulp.task('build-app', ['concat-app-js', 'jshint', 'sass', 'concat-libs-js', 'concat-libs-css']);
gulp.task('default', ['jshint', 'build-app', 'watch']);
