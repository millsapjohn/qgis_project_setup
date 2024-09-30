# qgis_project_setup

QGIS plugin to set up a project including default variables, gpkg connections, and Kart repos (in the future).

# Usage

This plugin sets up project variables to allow easier automation of tasks such as layout generation.
After installation, a submenu is created for the plugin, titled "Manage Project." To set project variables,
click the first option ("Project Setup...") to begin the process, and enter values for:

- project file location and name
- template geopackages to import, if any
- project number
- project name
- project client
- project location
- project address
- designed by
- reviewed by
- project datasources

# GeoPackage Templates

If you specify to import GeoPackage templates, you will be prompted to select the template(s) to import.
Optionally, you can specify a default location to look for templates, by setting a global QGIS variable 
called "gpkg_path" (not currently a part of the plugin, you'll need to set this yourself). If this variable
is not set, QGIS will start in your home directory.<br>

The plugin will rename the templates by prepending the project number to the front of the GeoPackage name. <br>
There is one special case hard-coded into the plugin, for a GeoPackage named "Blank.gpkg"; a file with this name will be renamed either "{project number}.gpkg", or "_.gpkg" if a project number isn't specified. The intent with this setup is to allow for setups where you have, for example, a template for layers related to a hydrologic analysis, "hydro.gpkg", which would be saved as "001.001_hydro.gpkg", as well as a blank catch-all GeoPackage just called "001.001.gpkg."

# Project DataSources

Project datasources are intended to be in the format "City of XXXX (2024)" to aid in layout generation.

# Updating Project DataSources

Often it is necessary to add additional datasources over the life of a project. This menu allows you to do so.

# Updating GeoPackage Connections

This plugin is designed to work in concert with embedded QGIS macros, to dynamically add and remove connections
on a per-project basis. The plugin sets a project variable listing all the GeoPackage connections the user wishes
to be associated with the project; by using the macro code [here](https://github.com/millsapjohn/qgis_macros), you
can read this project variable when opening a project, removing any GeoPackage connections unrelated to the project.<br>

Running the "Manage Persistent GeoPackage Connections" dialog will allow you to add any currently-connected GeoPackages 
to the whitelist, ensuring they are still present the next time the project is opened.
