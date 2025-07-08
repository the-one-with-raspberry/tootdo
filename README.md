![GitHub Actions Build Workflow Status](https://img.shields.io/github/actions/workflow/status/the-one-with-raspberry/tootdo/build.yml)
![GitHub Actions Release Workflow Status](https://img.shields.io/github/actions/workflow/status/the-one-with-raspberry/tootdo/release.yml?label=release)

# tootdo

A lightweight CLI todo list app.

# Installation

1. [Download the latest release of tootdo for your platform](https://github.com/the-one-with-raspberry/tootdo/releases/latest).
2. Copy it to a folder on your computer (preferrably in your user home or in a folder in the root).
3. Add the file to path.
    - On Windows:
        1. Search for "Edit the system/user environment variables".
        2. Click on "Environment Variables..." in the bottom right.
        3. Go to either user or system variables and double-click on `Path`.
        4. Click "New" and type the path to the file.
        5. Press "Ok" on both of the windows.
        6. Restart any shell apps.
    - On Linux/macOS:
        1. Open your terminal's profile path (most probably `~/.bashrc`, `~/.bash_profile` or `~/.zshrc`) in a text editor.
        2. Add the following line: `export PATH="/path/to/tootdo:$PATH"` and change `/path/to/tootdo` with the actual path. Don't forget to save!
        3. Restart any shell apps.
4. Done! You can now run it using `tootdo` in the terminal.

# Usage

Run `tootdo -h` for help. You can also run commands like `tootdo add -h` for more info.