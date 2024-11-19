Attribute VB_Name = "Module3"
Sub SelectSlicerItemsAll()
    Dim slicer As SlicerCache
    Dim slicerItem As slicerItem

    ' Set the slicer
    Set slicer = ThisWorkbook.SlicerCaches("Slicer_Area")

    ' Select all items in the slicer
    slicer.ClearManualFilter

    ' Deselect blank
    slicer.SlicerItems("(blank)").Selected = False
End Sub

