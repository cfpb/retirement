All notable changes to this project will be documented in this file.
We follow the [Semantic Versioning 2.0.0](http://semver.org/) format.

## 1.5.0 - 2015-11-30

### Changed
- Converted `.h#()` mixins to `.heading-#()` mixins to match cf-core's current usage


## 1.4.0 - 2015-07-16

### Additions

- Adds new input-warning color var
- Adds error exclamation icon


## 1.3.1 - 2015-06-05

### Changed

- Moved @import rules to top of source file to make compilation cleaner.


## 1.3.0 - 2015-06-01

### Changed

- Build process now uses @import statements instead of Grunt concatenation.

### Added

- pa11y accessibility tests running in Travis.


## 1.2.0 - 2015-01-16

### Changed
- Replaces all CFPB color variables with non-CFPB colors. To add the CFPB theme
  to your project you will need to include the CFPB color palette and the
  Capital Framework theme overrides file. Both files can be found in the
  generator-cf repo here:
  <https://github.com/cfpb/generator-cf/tree/master/app/templates/src/static/css>
  Background info on the new Capital Framework color variables can be found at
  <https://github.com/cfpb/capital-framework/issues/115>.

### Updated
- NPM dependencies.


## 1.1.1 - 2014-12-05

### Added
- Update cf-component-demo dev dependency to 0.9.0


## 1.1.0 - 2014-09-11

### Added
- New .input__super pattern.
- New .input-with-btn pattern.
- New .btn-inside-input pattern.


## 1.0.1 - 2014-09-02

### Fixed
- Bottom margins for .form-group_item have been replaced with top margins on
  siblings which, fixes issues of double margins in form groups.
