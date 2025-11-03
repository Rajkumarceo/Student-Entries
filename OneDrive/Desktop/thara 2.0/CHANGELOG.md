# Changelog

All notable changes to Purple 2.0 will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.0.0] - 2025-11-02

### Added
- Advanced voice recognition with Google Speech API
- Dual input modes (voice and text)
- Application management (open/close)
- Social media integration (Facebook, WhatsApp, Instagram, YouTube, ChatGPT)
- Google search integration with auto-exit feature
- System monitoring (CPU, Memory, Disk, Network, Battery)
- Volume control (up, down, mute)
- Daily schedule management
- Custom LLM chatbot integration
- Intelligent command parsing and pattern matching
- Process termination with multiple fallback methods
- Windows Store App support (Calculator)
- Browser tab management
- Smart LLM response filtering
- Extended voice input support (60-second timeout)

### Changed
- Improved command detection logic for close operations
- Enhanced error handling throughout the application
- Optimized TensorFlow/Keras imports for version compatibility
- Better microphone error handling

### Fixed
- Fixed close command detection (was incorrectly opening apps)
- Fixed TensorFlow import errors for newer versions
- Fixed unwanted LLM responses for system commands
- Improved process termination reliability

## [1.0.0] - Initial Release

### Added
- Basic voice recognition
- Text-to-speech functionality
- Simple command processing

---

## Version History

- **v2.0.0**: Major feature release with LLM integration and comprehensive system controls
- **v1.0.0**: Initial release with basic voice assistant capabilities

