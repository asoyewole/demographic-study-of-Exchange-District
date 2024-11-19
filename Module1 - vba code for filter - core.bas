Attribute VB_Name = "Module1"
Sub SelectSlicerItemsCore()
    Dim slicer As SlicerCache
    Dim slicerItem As slicerItem

    ' Set the slicer
    Set slicer = ThisWorkbook.SlicerCaches("Slicer_Area")

    ' Select all items in the slicer
    slicer.ClearManualFilter

    ' Deselect the items not in core list
    slicer.SlicerItems("Barber Street-46110670").Selected = False
    slicer.SlicerItems("Carlton Street-46110632").Selected = False
    slicer.SlicerItems("Cercle Moliere-46110805").Selected = False
    slicer.SlicerItems("Charles Street-46110069").Selected = False
    slicer.SlicerItems("Deacon Street-46110081").Selected = False
    slicer.SlicerItems("Edmonton Street-46110080").Selected = False
    slicer.SlicerItems("Good Street-46110635").Selected = False
    slicer.SlicerItems("Grove Street-46110671").Selected = False
    slicer.SlicerItems("Hargrave Street-46110630").Selected = False
    slicer.SlicerItems("Hargrave Street-46110631").Selected = False
    slicer.SlicerItems("Harriet Street-46110073").Selected = False
    slicer.SlicerItems("Israel Asper Way-46110810").Selected = False
    slicer.SlicerItems("Laura Street-46110070").Selected = False
    slicer.SlicerItems("Logan Avenue-46110176").Selected = False
    slicer.SlicerItems("Lydia Street-46110074").Selected = False
    slicer.SlicerItems("McDermot Avenue-46110075").Selected = False
    slicer.SlicerItems("Ross Avenue-46110072").Selected = False
    slicer.SlicerItems("Rue Aulneau Street-46110809").Selected = False
    slicer.SlicerItems("Smith Street-46111178").Selected = False
    slicer.SlicerItems("Spence Street-46110077").Selected = False
    slicer.SlicerItems("Vaughan Street-46110633").Selected = False
    slicer.SlicerItems("Young Street-46110634").Selected = False
    slicer.SlicerItems("(blank)").Selected = False
End Sub

