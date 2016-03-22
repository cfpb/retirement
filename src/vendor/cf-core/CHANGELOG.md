# Changelog

All notable changes to this project will be documented in this file.
We follow the [Semantic Versioning 2.0.0](http://semver.org/) format.

## Unreleased

## 1.4.0 - 2015-11-18

Updating web type spacing and leading

__Note:__ We are no longer optically adjusting margins/padding to match design mockups pixel perfectly

### Changed

- Updated text leading (line-height) to match recommendation from CFPB Design Manual issue #349
- Updated text top and bottom margins to match recommendation from CFPB Design Manual issue #269
- Renamed subheader to lead-paragraph

### Fixed

- Fixed subheading font-weight

## 1.3.1 - 2015-11-12
- Changed web superheading to regular weight.
- Changed name of `.superheader` to `.superheading`.
  - :warn: **Use of `.superheader` is deprecated and the class will be removed
    at the 2.0 release of cf-core.**

## 1.3.0 - 2015-10-28
- Updated colors to use 18F's US Web Standards color palette.

## 1.2.0 - 2015-10-13

- Updated to DMs t-shirt sized breakpoint variables
- Prepared old device centric variable for deprecation

## 1.1.3 - 2015-10-08
- Changed default colors for links to make them 508 compliant.

## 1.1.2 - 2015-10-05
- Added styles to override browser defaults for TH

## 1.1.1 - 2015-20-05
- Re-exposing the @font-size variable for code that relies on it to build appropriate em values

## 1.1.0 - 2015-10-05
- Added long-form heading mixins for defining the styles vs short-form for using them
  - Makes it possible to extend the headings for single-use custom sizes
  - Fixes an issue with breakpoint recursion in the short-form headings

## 1.0.3 - 2015-09-24
- Changed table styling and removed some styles (in preperation for cf-tables)

## 1.0.2 - 2015-07-30
- Fixed font-weight mixins that were using the reverse variables.

## 1.0.1 - 2015-06-05
- Moved @import rules to top of source file to make compilation cleaner.

## 1.0.0 - 2015-06-01

### Changed
- Build process now uses @import statements instead of Grunt concatenation.

### Added
- pa11y accessibility tests running in Travis.

## 0.11.0 - 2015-05-13

### Added
- Added webfont variables to make it easy to override defaults in cf-theme-overrides.less

### Removed
- Removing CFPB fonts and replaced it with system fonts. To add your own custom webfonts, add your @font-face rules and modify the `@webfont-regular/italic/medium/demi` variables.


## 0.10.0 - 2015-05-04

### Added
- A `.subheader` class for styling longer subheaders that we don't want to be
  too large or heavier than the regular weight.


## 0.9.0 - 2015-01-19

### Changed
- Replaces all CFPB color variables with non-CFPB colors. To add the CFPB theme
  to your project you will need to include the CFPB color palette and the
  Capital Framework theme overrides file. Both files can be found in the
  generator-cf repo here:
  <https://github.com/cfpb/generator-cf/tree/master/app/templates/src/static/css>
  Background info on the new Capital Framework color variables can be found at
  <https://github.com/cfpb/capital-framework/issues/115>.

### Removed
- `cf-brand-colors.less`, see note above why it's no longer needed.

### Updated
- NPM dependencies.


## 0.8.1 - 2014-12-05

### Added
- Updated cf-component-demo dev dependency to 0.9.0


## 0.8.0 - 2014-11-07

### Added
- Figure image enhancements.
- Superheader line height reduction
- Small text utility
- Hide/show on mobile utility classes
- Percentage width utility classes
- List with brand-color bullets


## 0.7.0 - 2014-11-04

### Added
- Responsive headers (h1-h3).
- Screen size variables.


## 0.6.0 - 2014-11-04

### Added
- Set `max-width` for all `img` elements to 100%.
- Top and bottom margin utility classes.


## 0.5.0 - 2014-09-11

### Added
- Default font family for labels is now Avenir Regular.
- Checkboxes and radios inside of labels now have default margins to separate
  it from the label text.


## 0.4.0 - 2014-09-04

### Added
- .u-js-only utility class for hiding stuff when JS is not available.


## 0.3.2 - 2014-09-02

### Fixed
- Fixes horizontal margins for `<figure>` elements.


## 0.3.1 - 2014-09-02

### Fixed
- .u-link__colors mixin now uses the same border targeting as normal links;
  all borders instead of bottom borders.


## 0.3.0 - 2014-08-15

### Added
- Added base table styling.


## 0.2.0 - 2014-08-12

### Added
- Adds custom demo of basic form elements from cf-forms.
- Updates cf-component-demo and rebuilds docs.
  This adds an "edit on Codepen" button to each HTML pattern.


## 0.1.0 - 2014-08-06

### Added
This component contains core styles for starting a Capital Framework project or
component. It includes normalize, normalize-legacy-addon, variables (including
cf-colors), media query and utility mixins, class utilities and standard base
styling (including cf-typography and some base styles from cf-forms).

All Capital Framework components that used to depend any of the following will
move to using cf-core instead: normalize, normalize-legacy-addon, cf-typography,
or cf-colors.
