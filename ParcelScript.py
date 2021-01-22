import arcpy
import os

#set workspace environment to your GDB
arcpy.env.workspace = r"D:\Test\MeganParcel\ParcelProject.gdb"
CensusUrbanBoundary = r"D:\Test\MeganParcel\Boundaries.gdb\CensusUrbanBoundary"

#list the feature classes
fcList = arcpy.ListFeatureClasses()

#loop through list
for fc in fcList:
    print("**********Working on {} county*************".format(fc))
    
    print("Adding fields...") # Adds new fields to feature classes
    arcpy.AddField_management(fc,"Calc_Acres","DOUBLE")
    arcpy.AddField_management(fc,"PricePerAcre","DOUBLE")
    arcpy.AddField_management(fc,"SapCounty","SHORT")
    arcpy.AddField_management(fc,"TempID","LONG")
    arcpy.AddField_management(fc,"Urban","TEXT")

    print("Updating values...")
    arcpy.CalculateField_management(fc,"TempID", "!OBJECTID!")
    arcpy.CalculateField_management(fc,"Calc_Acres","!shape.geodesicArea@ACRES!")
    arcpy.CalculateField_management(fc,"PricePerAcre","!PARVAL! / !Calc_Acres!")

    print("Identifying urban parcels within census boundary...")
    selection = arcpy.SelectLayerByLocation_management(fc, 'INTERSECT', CensusUrbanBoundary)
    selectionCount = int(arcpy.GetCount_management(selection)[0])
    print ("Total parcels selected are: {}".format(selectionCount))

    # Process only if the matched records are more than Zero
    if selectionCount != 0:
        # Creating a list of TempIDs to be updated in the main feature class
        selectionList = []
        with arcpy.da.SearchCursor(selection,['TempID']) as cursor:
            for row in cursor:
                selectionList.append(row[0])

        print("Updating urban parcles...")
        with arcpy.da.UpdateCursor(fc,['TempID','Urban']) as cursor:
            for row in cursor:
                if row[0] in selectionList:
                    row[1] = 'Yes'
                cursor.updateRow(row)
    
        del selectionList
        del selection
print ('Done')
