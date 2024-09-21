# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.3.7]
### Changed
- Removed distinct on initial admin queryset, because of delete missbehaviour.

## [0.3.6]
### Changed
- One interlocutor connection for one token by default, even if interlocutor and network are different next time.

## [0.3.5]
### Fixed
- Token interlocutor connections duplication on it's registration.

## [0.3.4]
### Changed
- Improvements in admin panel informativity.

## [0.3.1]
### Changed
- Improvements in admin panel informativity.

## [0.3.0]
### Added
- Device registry.
- Token registry pipeline.
- Expire old tokens on refresh.
- Token archiver.

### Changed
- Extended configurations.

### Fixed
- Different fixes.

## [0.2.3]
### Fixed
- Authentication fixes.

## [0.2.0]
### Added
- Tokens registry.
### Changed
- Reduced amount of code dependent on simplejwt. Small improvements because of that and more flexible and extendable code as result.

## [0.1.4]
### Added
- Translation strings.

## [0.1.1]
Initial version.
