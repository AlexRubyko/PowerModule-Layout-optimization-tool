import vtk
import argparse


class PolydataReader(object):

    """
        PolyData read file of a surface and determine if it is closed surface
    """
    def __init__(self):
        print("Class PolyDataChecker")

    @staticmethod
    def get_program_parameters():

        description = 'Read a .stl file. Enter available .stl files that you want to be read'
        epilogue = ''''''
        parser = argparse.ArgumentParser(description=description, epilog=epilogue,
                                         formatter_class=argparse.RawDescriptionHelpFormatter)
        parser.add_argument('filename', help='Default')
        args = parser.parse_args()
        return args.filename

    @staticmethod
    def readPolyData(file_name):
        import os
        path, extension = os.path.splitext(file_name)
        extension = extension.lower()
        if extension == ".ply":
            reader = vtk.vtkPLYReader()
            reader.SetFileName(file_name)
            reader.Update()
            poly_data = reader.GetOutput()
        elif extension == ".vtp":
            reader = vtk.vtkXMLpoly_dataReader()
            reader.SetFileName(file_name)
            reader.Update()
            poly_data = reader.GetOutput()
        elif extension == ".obj":
            reader = vtk.vtkOBJReader()
            reader.SetFileName(file_name)
            reader.Update()
            poly_data = reader.GetOutput()
        elif extension == ".stl":
            reader = vtk.vtkSTLReader()
            reader.SetFileName(file_name)
            reader.Update()
            poly_data = reader.GetOutput()
        elif extension == ".vtk":
            reader = vtk.vtkpoly_dataReader()
            reader.SetFileName(file_name)
            reader.Update()
            poly_data = reader.GetOutput()
        elif extension == ".g":
            reader = vtk.vtkBYUReader()
            reader.SetGeometryFileName(file_name)
            reader.Update()
            poly_data = reader.GetOutput()
        else:
            # Return a None if the extension is unknown.
            poly_data = None
        return poly_data

    @staticmethod
    def checking_for_poly_data():
        linpak = PolydataReader.get_program_parameters()
        polyData = PolydataReader.readPolyData(linpak)
        featureEdges = vtk.vtkFeatureEdges()
        featureEdges.FeatureEdgesOff()
        featureEdges.BoundaryEdgesOn()
        featureEdges.NonManifoldEdgesOn()
        featureEdges.SetInputData(polyData)
        featureEdges.Update()

        num_open_edg = featureEdges.GetOutput().GetNumberOfCells()
        print(num_open_edg)

        if num_open_edg > 0:
            print("Surface '{}' is not closed.".format(str(linpak)))
            print("The number of open edges->{}".format(num_open_edg))
        else:
            print("Surface '{}' is indeed closed.".format(str(linpak)))


PolydataReader.checking_for_poly_data()
