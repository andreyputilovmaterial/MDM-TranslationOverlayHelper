


template_begin = """



#define INP_FILE "<<MDDINPNAME>>"
#define OUT_FILE "<<MDDOUTNAME>>"


debug.log("starting script")
debug.echo("starting script")
	
	Dim objMDM
	dim fso
	
debug.log("Deleting the output MDD and creating a new copy with such name")
debug.echo("Deleting the output MDD and creating a new copy with such name")

	Set fso = CreateObject("Scripting.FileSystemObject")
	If (fso.FileExists(OUT_FILE)) Then
		fso.DeleteFile(OUT_FILE)
	End If
	fso.CopyFile(INP_FILE,OUT_FILE)
	set fso = null
	
	
	
debug.log("opening MDD")
debug.echo("opening MDD")

	Set objMDM = CreateObject("MDM.Document")
	objMDM.Open(OUT_FILE)
	

dim newline
'newline = "<br />"
newline = mr.lf

'dim sLangTextOrig<<LOCALVARS>>

debug.log("applying overlay updates")
debug.echo("applying overlay updates")

"""


template_end = """


debug.log("saving MDD...")
debug.echo("saving MDD...")

	objMDM.Save()

debug.log("done!")
debug.echo("done!")

"""

