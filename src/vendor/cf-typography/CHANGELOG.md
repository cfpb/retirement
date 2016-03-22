All notable changes to this project will be documented in this file.
We follow the [Semantic Versioning 2.0.0](http://semver.org/) format.

## 1.3.0 -2015-11-30

### Changed
- Converted `.h#()` mixins to `.heading-#()` mixins to match cf-core's current usage


## 1.2.0 - 2015-11-01
- Added @font-size vars to .micro-copy() and .jump-link()

## 1.1.0 - 2015-10-28
- Change default colors to match 18F color pallete from US Web Design Standards
- Fixing typos in code comments

## 1.0.1 - 2015-07-05
- Moved @import rules to top of source file to make compilation cleaner.

## 1.0.0 - 2015-07-01
- Build process now uses @import statements instead of Grunt concatenation
- Added pa11y tests accessibility tests

## 0.8.1 - 2015-04-01

### Fixed
- Restores borders back to the `.block-link` pattern (and, in turn,
  `.jump-link`s).

### Updated
- cf-icons dependency for docs & demo.


## 0.8.0 - 2015-03-23

### Added
- Adds default and icon list `.list__links` pattern from cfgov-refresh `lists.less`.


## 0.7.0 - 2015-01-21

### Changed
- Replaces all CFPB color variables with non-CFPB colors. To add the CFPB theme
  to your project you will need to include the CFPB color palette and the
  Capital Framework theme overrides file. Both files can be found in the
  generator-cf repo here:
  <https://github.com/cfpb/generator-cf/tree/master/app/templates/src/static/css>
  Background info on the new Capital Framework color variables can be found at
  <https://github.com/cfpb/capital-framework/issues/115>.

### Updated
- Dependencies.


## 0.6.0 - 2015-01-15

### Added
- Typographical patterns from cf-core & cfgov-refresh:

- From cfgov-refresh `lists.less`:
- `.list_link`
- `.list__unstyled`
- `.list__spaced`
- `.list_item__spaced`
- `.list__horizontal`
- `.list__icons`
- ~~`.list__links`~~ - added in `0.8.0`.

- From cfgov-refresh `misc.less`:
- `.micro-copy`
- `.short-desc`
- `.icon-link`
- `.styled-link`
- `.jump-link`
- `.block-link `

- From cfgov-refresh `meta.less`:
- `.date`
- `.category-slug`
- `.header-slug`
- `.padded-header`
- `.fancy-slug`
- `.meta-header`

- From `cf-core`:
- `.pull-quote`
- `.list__branded`
