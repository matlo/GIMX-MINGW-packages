GIMX-MINGW-packages
===================

See https://github.com/msys2/MINGW-packages/blob/master/README.md

## SDL2

* SDL2-haptic-first-axis.patch: [The haptic API does not allow to select the direction axes](https://bugzilla.libsdl.org/show_bug.cgi?id=3446)
* SDL2-GetRawInputDeviceList.patch: [GetRawInputDeviceList may return less entries than requested](https://bugzilla.libsdl.org/show_bug.cgi?id=4006)
* PKGBUILD: disable SDL timers

## avrdude

* PKGBUILD: Remove libftdi and libusb dependencies.

## pdcurses

* There was no recipie in the official msys2/MINGW-packages repository when I created this one. I will look at switching to the official one.

## libusb

* libusb-clock-gettime.patch: disable the threaded windows\_clock\_gettime on Windows versions >= 7
