var gulp = require('gulp');
var babel = require('gulp-babel');
var watch = require('gulp-watch');

const root = './peek/app/static';

gulp.task('babel', function(){
    return gulp.src(root + '/jsx/*.jsx')
        .on('error', function(e) {
            console.log('Error', e);
        })
        .pipe(babel({
            plugins: ['transform-react-jsx']
        }))
        .pipe(gulp.dest(root + '/js/gen/'))
    ;
});

gulp.task('watch', function () {
    gulp.watch(root + '/jsx/*.jsx', ['babel']);
});

gulp.task('default', ['babel', 'watch']);
