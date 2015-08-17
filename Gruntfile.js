
module.exports = function(grunt) {
  grunt.loadNpmTasks('grunt-contrib-concat');
  grunt.loadNpmTasks('grunt-contrib-watch');
  grunt.loadNpmTasks('gruntify-eslint');

  grunt.registerTask('build', ['concat']);
  grunt.registerTask('lint', ['eslint']);
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
    eslint: {                   
      options: {
        useEslintrc: false,
        configFile: "conf/eslint.yaml"
      },
      src: ["src/*.js"]
    },
    watch: {
      js: {
        options: {
          interrupt: true,
          livereload: true
        },
        files: ['Gruntfile.js', 'src/*.js', 'retirement_api/templates/*', 'retirement_api/static/retirement/**', '!retirement_api/static/retirement/js/claiming-social-security.js'],
        tasks: ['build']
      },
    },
  });
};
