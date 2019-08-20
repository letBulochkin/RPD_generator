# RPD_generator (en)
Python util for parsing Microsoft Excel (`.xlsx`) tables and processing Microsoft Word (`.docx`) files.

Util was made in order to optimize document processing at one of departements of Russian Technological Univercity. Util gets data from standartized Excel table following rules written in `.xml` file and then puts it to `.docx` template. User fills additional data in to the forms, provided by user interface.

RPD_generator uses:
* Python 3.7
* PyQt5
* openpyxl 2.5.9
* python-docx 0.8.7

### Overview

RPD_generator has following structure:

#### main.py

Contains:
* `RPD_Window` class, which provides interaction between user interface and core. 

#### ui_RPD.py

Contains PyQt interface classes:
* `Ui_MainWindow` class, which describes components of the main window of application.
* `Ui_competencyBox`, `Ui_moduleBox`, `Ui_taskBox` and `Ui_semesterBox` classes represent different interface elements (PyQt `QGroupBox` instances, to be specific.)

#### pycore

`pycore/` folder contains core classes for the application. They were designed specifically to the subject area - bureaucratic system of russian education facilities. Therefore they designation may be unclear to unfamiliar reader.

* `struct.py` provides main entities for application and getters/setter for their data.
* `crawler.py` provides functions necessary to get data from Microsoft Excel table.
* `generator.py` provides functions necessary to paste data to Microsoft Word document. In order to navigate over document easily, application uses specially prepared document template with special marks included in it. Marks are defined sequence of symbols (e.g. `<>`) which can be detected in Word paragraphs and runs.
* `commutator.py` describes the consequence of actions in order to form correct document.

### TODO

This project was aimed to optimize workflow and document preparation. RPD_generator was designed to generate documents according to defined template. Though, template is constantly changing, which requires application to be adaptive to this changes.

This can be achieved by higher abstraction between final template and core methods of the application. Ideally core functions should provide only basic methods to get and paste data. That is why `crawler.py` and `generator.py` were made as separate modules.

There also should be a way to control and manage the ways how data is being taken, modified, represented and pasted to final document. That is why I tried to use `.xml` files to define from where data is taken. But this is now enough.

- [] New interface using HTML, CSS, JS and so on.
- [] Higher abstraction between information sources and core functions of the application. Futher use of `.xml` rules

Ugh. I will never do this. 