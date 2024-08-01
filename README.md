# Mocha ☕
Mocha is a sleek, easy to use and (somewhat) customisable online video downloader which supports thousands of sites.

## Installation
You can either build it from source or use the releases tab to download an exe. The exe is build using auto-py-to-exe and has all the libraries bundled in, hence the atrocious file size.

### Building from source
To build from source you can use these simple commands, you will need [python](https://www.python.org/downloads/) and [git](https://git-scm.com/downloads) installed.

``git clone https://github.com/YoxieGraphics/mocha.git``

``cd mocha``

``pip install -r requirements.txt``

``pyinstaller --noconfirm --onefile --windowed --icon ".\logo.ico" --name "Mocha" --add-data ".\.gitignore;." --add-data ".\downloader.py;." --add-data ".\gui.py;." --add-data ".\logo.ico;." --add-data ".\logo.png;." --add-data ".\settings.py;."  ".\main.py"`` (This may take a few minutes)

Now navigate to the 'dist' directory and the mocha binary will be there
