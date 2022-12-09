# BOMdBase

BOMdBase is a simple database with a web UI for electronic engineers who need to produce BOMs (Bills of Material). It allows the user to build a library of parts, to import raw BOM data from their CAD software, and to output essential data that contract electronics manufacturers need to source parts and assemble boards.

Written in Python, BOMdBase uses the [Django framework](https://www.djangoproject.com/), with [Bootstrap 5](https://getbootstrap.com/) styling and icons from [Material Design](https://material.io/resources/icons).

At present, BOMdBase imports BOM data from OrCAD Capture directly. KiCad support is planned.

**Please note that the tool is in a preview state at present, with Django debugging enabled.**

## Parts

BOMdBase provdes 3 part types:

1) Logical Parts: These are used by design engineers in schematics; they represent the designer's intentions and requirements; part numbering is user defined. Typically a logical part number is stored as a user defined property in a schematic part. The database supports optional notes for logical parts; these can be used to specify substitution or sourcing policies for logical parts, among other things.

2) Manufacturer Parts: These are the physical parts that are approved by the designer. A logical part may be linked with multiple manufacturer parts. Note that manufacturer parts may be assigned a measurement unit, for example of weight or of volume.

3) Supplier Parts: Suppliers stock and sell manufacturer parts; their part numbers are sometimes known as order codes or SKUs. A supplier part is linked with a single manufacturer part; multiple alternative supplier parts may be linked to the same manufacturer part. The user does not have to specify a supplier part; contract electronic manufacturers will normally be able to - and may prefer to - source manufacturer parts from their own supply chains.

In some cases, parts may have a known supplier but an unknown manufacturer. In these cases it is suggested that a dummy manufacturer part is created to act as a shim between the logical and supplier parts, with the manufacturer organisation being 'unspecified' and the manufacturer part number being a concatenation of the supplier name and supplier part number.

The UI allows the user to browse, edit, delete and create parts, and to make or break links between parts. Parts may optionally be assigned to categories. These make sorting and browsing parts and BOMs data easier.

## BOMs

The UI allows the user to browse, edit, delete and create BOMs. Note that this refers to BOM names and descriptions - not BOM items. Items are created by importing from CAD software, or by database Restore/Import. BOMs may be viewed in and printed from the browser, and exported to a CSV file.

## Organizations

Organizations include both manufacturers and suppliers. BOMdBase' UI allows the user to browse, edit, delete and create organizations.

## Backup/Export and Restore/Import

All data may be backed up or restored from a CSV file. The restore/import process is flexible and allows users to build parts data in spreadsheets and to import that data in bulk; a CSV row may contain fields relating to a logical part, manufacturer part and up to 10 alternative supplier parts, along with associated data such as part category and notes.

## Installation

Python 3.9 or later is required for installing and using BOMdBase.

The following instructions are for Windows users. A Windows setup batch file (setup.bat) is provided in the root directory. Alternatively, perform the following steps:

1. Clone the repository to an appropriate directory.

2. Navigate to the installation path:

     `C:\WINDOWS\system32> cd \utils\BOMdBase`

3. Create a virtual environment:

     `C:\utils\BOMdBase> python -m venv .venv`

4. Activate the virtual environment:

     `C:\utils\BOMdBase> .venv\Scripts\activate.bat`

5. Install Python dependancies:

     `(.venv) C:\utils\BOMdBase> python -m pip install -r requirements.txt`

6. Initialise database:

     `(.venv) C:\utils\BOMdBase> python manage.py migrate`

7. Create superuser (optional):

     `(.venv) C:\utils\BOMdBase> python manage.py createsuperuser`

## Launching

A Windows launcher batch file (launch.bat) is provided in the root directory. Alternatively, perform the following steps:

1. Launch a command prompt.

2. Navigate to the installation directory:

     `C:\WINDOWS\system32> cd \utils\BOMdBase`

3. Activate the virtual environment, if required:

     `C:\utils\BOMdBase> .venv\Scripts\activate.bat`

4. Start the application:

    `(.venv) C:\utils\BOMdBase> manage.py runserver`

5. Open the [local server URL](http://127.0.0.1:8000/) in a web browser.
