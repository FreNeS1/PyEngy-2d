# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.0.4] - 2020-07-29
### Added
- Image resources and resource manager.
- Sprite node capable of rendering an image on screen. Includes texture controls.
### Changed
- Node parent and children are now properties that check and update.

## [0.0.3] - 2020-07-29
### Added
- Image resources and resource manager.
- Sprite node capable of rendering an image on screen. Includes texture controls.
### Changed
- Example app moved to example folder

## [0.0.2] - 2020-07-29
### Added
- App class that acts as a controller for the nodes.
- Node class with inheritance, tree structure and action delegation. The following nodes were created:
    - Utility Nodes: `Node`
    - 2D Nodes: `Node2D`
- Customizable, printable and easy to use errors.
- Custom utils:
    - Math utils for geometry calculations or unit conversions.
    - Custom context object to retrieve and set values.
    - Logger with built in app format and timestamps.
    - Time control based on milliseconds since custom epoch. 
### Changed
- Upped PyGame to version 2.0.0

## [0.0.1] - 2020-07-02
### Added
- Setup simple project.
