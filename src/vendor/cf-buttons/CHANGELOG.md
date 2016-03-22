All notable changes to this project will be documented in this file.
We follow the [Semantic Versioning 2.0.0](http://semver.org/) format.

## 1.7.0 - 2015-07-30
- Updated the base button font-size to Design Manual spec

## 1.6.2 - 2015-06-05
- Moved @import rules to top of source file to make compilation cleaner.

## 1.6.1 - 2015-06-01

### Changed
- Build process now uses @import statements instead of Grunt concatenation.

### Added
- pa11y accessibility tests running in Travis.

## 1.5.1 - 2015-05-18

### Added
- You can now use the `disabled` attribute in place of `btn__disabled` if you want to.

## 1.5.0 - 2015-05-18

### Added
- React Component: `CFButton`

## 1.4.2 - 2015-04-15

### Fixed
- Updated `btn__link` to use link styles from cf-core, instead of btn-bg styles.


## 1.4.1 - 2015-03-05

### Changed
- Transition no longer affects all button properties, only the background color.


## 1.4.0 - 2015-01-13

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


## 1.3.1 - 2014-11-02

### Changed
- Updated npm and bower deps and recompiled. This updates the docs template.


## 1.3.0 - 2014-09-09

### Added
- Updated focus styling for button links.
- Added `.btn__link.btn__secondary` styles.


## 1.2.0 - 2014-09-05

### Added
- Focus styles.
