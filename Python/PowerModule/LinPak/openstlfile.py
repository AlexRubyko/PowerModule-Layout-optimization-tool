import vtk
import argparse
from stl import mesh
from mpl_toolkits import mplot3d
from matplotlib import pyplot
import math
import stl
from stl import mesh
import numpy


class LinpakSTL(object):
    """
        Opens .STL format file only
    """
    def __init__(self):
        pass

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
    def rendering_lin_pak():
        colors = vtk.vtkNamedColors()

        filename = LinpakSTL.get_program_parameters()

        reader = vtk.vtkSTLReader()

        reader.SetFileName(filename)

        # making adges
        edges = vtk.vtkFeatureEdges()
        edges.SetInputConnection(reader.GetOutputPort())
        edges.BoundaryEdgesOn()
        edges.FeatureEdgesOn()
        edges.ManifoldEdgesOn()
        edges.NonManifoldEdgesOff()
        edges.Update()

        # visualize edges
        edgeMapper = vtk.vtkPolyDataMapper()
        edgeMapper.SetInputConnection(edges.GetOutputPort())
        edgeActor = vtk.vtkActor()
        edgeActor.SetMapper(edgeMapper)

        #Visualize
        mapper = vtk.vtkPolyDataMapper()
        mapper.SetInputConnection(reader.GetOutputPort())
        actor = vtk.vtkActor()
        actor.SetMapper(mapper)

        # Create a rendering window and renderer
        ren = vtk.vtkRenderer()
        renWin = vtk.vtkRenderWindow()
        renWin.AddRenderer(ren)

        # Create a renderwindowinteractor
        iren = vtk.vtkRenderWindowInteractor()
        iren.SetRenderWindow(renWin)

        # Assign actor to the renderer
        ren.AddActor(edgeActor)
        ren.AddActor(actor)

        # axes
        axes = vtk.vtkAxesActor()
        widget = vtk.vtkOrientationMarkerWidget()
        rgba = [1] * 4
        colors.GetColor("Carrot", rgba)
        widget.SetOutlineColor(rgba[1], rgba[1], rgba[2])
        widget.SetOrientationMarker(axes)
        widget.SetInteractor(iren)
        widget.SetViewport(0.0, 0.0, 0.4, 0.4)
        widget.SetEnabled(1)
        widget.InteractiveOn()

        ren.GetActiveCamera().Azimuth(50)
        ren.GetActiveCamera().Elevation(-30)

        ren.ResetCamera()
        #ren.SetBackground(colors.GetColor3d("blue"))
        ren.SetBackground(colors.GetColor3d("black"))
        # Enable user interface interractor
        iren.Initialize()
        renWin.Render()
        iren.Start()

    @staticmethod
    def pyplotting_stl():

        """

        :return:
        """

        filename = LinpakSTL.get_program_parameters()

        # Create a new plot
        figure = pyplot.figure()
        axes = mplot3d.Axes3D(figure)
        # Load the STL files and add the vectors to the plot
        your_mesh = mesh.Mesh.from_file(filename)
        axes.add_collection3d(mplot3d.art3d.Poly3DCollection(your_mesh.vectors))
        # Auto scale to the mesh size
        scale = your_mesh.points.flatten(-1)
        axes.auto_scale_xyz(scale, scale, scale)
        # Show the plot to the screen
        pyplot.show()

    @staticmethod
    def convert_to_mesh():
        filename = LinpakSTL.get_program_parameters()
        main_body = mesh.Mesh.from_file(filename)
        main_body.save('stlToASCII', mode=stl.Mode.ASCII)
        main_body.save('stltoBinary', mode=stl.Mode.BINARY)


LinpakSTL.convert_to_mesh()