module.exports = function( grunt )
{
var dest = '../../todolist_web_api_website/';


grunt.initConfig({
        pkg: grunt.file.readJSON( 'package.json' ),

            // delete the destination folder (apart from the git repository and the virtual environment)
        clean: {
            options: {
                force: true
            },
            release: [
                dest + '*',
                '!' + dest + '.git',
                '!' + dest + '.gitignore',
                '!' + dest + 'env/**'
            ]
        },

            // copy the necessary files
        copy: {
            release: {
                expand: true,
                cwd: '../',
                src: [
                    'accounts/**/*.py',
                    'todolist/**/*.py',
                    'todolist_web_api/**/*.py',
                    'static/**',
                    'templates/**',
                    'manage.py',
                    'Procfile',
                    'requirements.txt',
                    'runtime.txt'
                ],
                dest: dest
            }
        },

            // minimize the javascript
        uglify: {
            release: {
                files: [
                    {
                        expand: true,
                        cwd: dest + 'static/js/',
                        src: [ '**/*.js' ],
                        dest: dest + 'static/js/'
                    }
                ]
            }
        },

            // minimize the css
        cssmin: {
            release: {
                files: [{
                    expand: true,
                    cwd: dest + 'static/css/',
                    src: '**/*.css',
                    dest: dest + 'static/css/'
                }]
            }
        }
    });

    // load the plugins
grunt.loadNpmTasks( 'grunt-contrib-copy' );
grunt.loadNpmTasks( 'grunt-contrib-uglify' );
grunt.loadNpmTasks( 'grunt-contrib-cssmin' );
grunt.loadNpmTasks( 'grunt-contrib-clean' );

    // tasks
grunt.registerTask( 'default', [ 'clean', 'copy', 'uglify', 'cssmin' ] );
};