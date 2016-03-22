All notable changes to this project will be documented in this file.
We follow the [Semantic Versioning 2.0.0](http://semver.org/) format.


## 0.5.0 - 2015-01-19

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


## 0.4.2 - 2014-12-05

### Added
- Update cf-component-demo dev dependency to 0.9.0


## 0.4.1 - 2014-10-02

### Added
- Updated to use the originally intended super buttons.
- Updated to use more cf-core utilities, some of which allow for better
  accessibility support.

### Fixed
- Did some code refactoring.


## 0.4.0 - 2014-08-28

### Added
- Bower dependency cf-core (replaces dependencies removed, listed below)

### Removed
- Bower depencencies cf-colors, cf-forms, cf-typography, normalize

### Fixed
- Updated npm/Bower depenencies and rebuild docs
- Example markup and .pagination_form padding to work with updates to cf-buttons
