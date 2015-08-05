
module.exports = function(grunt) {
  grunt.loadNpmTasks('grunt-contrib-concat');
  grunt.loadNpmTasks('grunt-contrib-watch');

  grunt.registerTask('build', ['concat']);
  grunt.registerTask('default', ['concat']);

  grunt.initConfig({
    concat: {
      options: {
        separator: '\n\n',
      },
      dist: {
        src: ['src/claiming-functions.js', 'src/claiming-graph.js'],
        dest: 'retirement_api/static/retirement/js/claiming-social-security.js',
      },
    },
    watch: {
      js: {
        options: {
          interrupt: true,
        },
        files: ['Gruntfile.js', 'src/*.js'],
        tasks: ['build']
      },
    },
  });
};