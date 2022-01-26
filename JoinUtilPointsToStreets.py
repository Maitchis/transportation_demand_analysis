# -*- coding: utf-8 -*-
"""
Created on Mon Apr 12 17:28:17 2021

@author: tchis
"""

def JoinUtilPointsToStreets(fcPoint,fcPolyline,search_dist,field_name,workspace):
    
    # Import required modules
    import arcpy
    import os
    import sys
    import traceback
    
    # Set the current workspace
    arcpy.env.workspace = workspace
    
    # Define custom exceptions
    class WorkspaceExistsError(Exception):
        pass
    class fcPointExistsError(Exception):
        pass
    class fcPolylineExistsError(Exception):
        pass
    class WorkspaceEmptyError(Exception):
        pass
    class fcPointShapeError(Exception):
        pass
    class fcPolylineShapeError(Exception):
        pass
    
    try:
        # Test if workspace exists
        if arcpy.Exists(workspace):
            pass
        else:
            raise WorkspaceExistsError
            
        # Test if there are any feature classes in the specified folder or geodatabase
        # Walk through the input folder or geodatabase and find all feature classes; add their names to the fclist
        fclist = []
        checkwalk = arcpy.da.Walk(workspace,datatype = "FeatureClass")
        for dirpath, dirnames, filenames in checkwalk:
            for file in filenames:
                fclist.append(str(file))
                
        # If fclist is empty, then there were no feature classes in the specified folder or geodatabase
        if not fclist:
            raise WorkspaceEmptyError
        else: pass
            
        # Test if fcPoint exists
        if arcpy.Exists(fcPoint):
            pass
        else:
            raise fcPointExistsError
            
        # Test if fcPolyline exists
        if arcpy.Exists(fcPolyline):
            pass
        else:
            raise fcPolylineExistsError
            
        # Test if point feature class shapeType is valid
        desc = arcpy.Describe(fcPoint)
        if desc.shapeType != "Point":
            raise fcPointShapeError
        else: pass
    
        # Test if polyline feature class shapeType is valid
        desc = arcpy.Describe(fcPolyline)
        if desc.shapeType != "Polyline":
            raise fcPolylineShapeError
        else: pass
    
    
    except WorkspaceExistsError:
        print("WorkspaceExistsError: The specified workspace could not be found!")
        
    except WorkspaceEmptyError:
        print("WorkspaceEmptyError: Workspace appears to contain no feature classes!")
        
    except fcPointExistsError:
        print("fcPointExistsError: The specified points feature class could not be found!")
    
    except fcPolylineExistsError:
        print("fcPolylineExistsError: The specified polyline feature class could not be found!")
        
    except fcPointShapeError:
        print("fcPointShapeError: The specified feature class must be a points feature class!")
        
    except fcPolylineShapeError:
        print("fcPolylineShapeError: The specified feature class must be a polyline feature class!")
        
    else:
        try:
            # Define function output name
            output_fc = fcPolyline + "_join"
            
            # Run a spatial join between the specified points feature class and polyline feature class
            arcpy.analysis.SpatialJoin(fcPolyline, fcPoint, output_fc, join_type = "KEEP_ALL", match_option = "WITHIN_A_DISTANCE", search_radius = search_dist)
            
            # Rename the counts field
            arcpy.management.AlterField(output_fc, "Join_Count", field_name, field_name)
            
            # Rejoin to original input polyline
            arcpy.management.JoinField(fcPolyline, "SEGID", output_fc, "SEGID", field_name)
            
            # Delete unneeded join file
            delfc = os.path.join(workspace, output_fc)
            arcpy.management.Delete(delfc)
        
        except arcpy.ExecuteError: 
            # Get the tool error messages 
            msgs = arcpy.GetMessages(2) 

            # Return tool error messages for use with a script tool 
            arcpy.AddError(msgs) 

            # Print tool error messages for use in Python
            print("Tool Error:", msgs)

        except:
            # Get the traceback object
            tb = sys.exc_info()[2]
            tbinfo = traceback.format_tb(tb)[0]

            # Put error information into a message string
            pymsg = "PYTHON ERRORS:\nTraceback info:\n" + tbinfo + "\nError Info:\n" + str(sys.exc_info()[1])
            msgs = "ArcPy ERRORS:\n" + arcpy.GetMessages(2) + "\n"

            # Return python error messages for use in script tool or Python window
            arcpy.AddError(pymsg)
            arcpy.AddError(msgs)

            # Print Python error messages for use in Python / Python window
            print(pymsg)
            print(msgs)