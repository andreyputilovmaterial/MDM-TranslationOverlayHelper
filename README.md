# MDM-TranslationOverlayHelper
A tool that creates an Excel with fields and labels from MDD, including translations. This is super handy if the project workflow involves manual translation updates. 99% of the time you don't need it - we send files to LI, and they are doing their job fine. But sometimes we need to work on a project and work on translations without any help from LI side. Then, having such Excel file generated make everybody's life much easier - everyone who works on translations, checks it, who needs to review... Or who need to update it in MDD (I mean us, IPS).

Then, if translations were updated in the Excel, this tool can generate scripts to update your MDD back.

Enjoy!

## How to use:

Download files from the latest Release page:
[Releases](../../releases/latest)

To get it started, just edit the BAT file and insert the path to your MDD and desired name for the Excel file with map of all fields. Then just start the BAT file. Please note, there is no "pause" at the end. If it disappears, it means everything worked and finished successfully.

Enjoy.

You need python installed and IBM/Unicom Professional to have this tool running. It is a requirement.

If some python packages are missing, just type
`python -m pip install xxx`
where xxx is a missing package.

The tool is distributed as a .py file, but you can't edit it. If you are not happy with the results, find the source codes (they are open) and re-generate the compiled bundle. Do NOT edit, as this bundle is a tricky file - python is reading and loading parts of self in runtime, and start and end positions of these parts are hardcoded. If you edit anything, block positions will be incorrect, and running the file will lead to undefined behaviour.

# Frequently asked questions
TBD
