"""
This submodule is currently under development

It will contain functionality for creating components,
subassemblies, and assemblies.
"""

from __future__ import annotations
from typing import TypeAlias
from collections.abc import Iterable
from copy import deepcopy


import trimesh
import numpy as np
import numpy.typing as npt

from engscript.export import Scene
from engscript.engscript import Solid

_Vec3: TypeAlias = tuple[float, float, float]


class Component:
    """
    A grouping class for individual components assemblies. This class can hold
    multiple 3D mesh objects which are treated as a single component.

    Create a component with

    ```python
    my_component = Component([obj1, obj2, obj3])
    ```

    the input components can be `engscript.engscript.Solid` objects or `trimesh.Trimesh`
    objects. This component will convert any solids into trimeshes.

    This means that non-watertight meshes that cannot be manipulated as solids can still
    be used in rendering of assemblies.
    """

    def __init__(
        self,
        geometry: list[trimesh.Trimesh | Solid] | trimesh.Trimesh | Solid
    ) -> None:
        """
        Create a component with from a solid, a trimesh or a list containing a mixture
        of the two

        :param geometry: The geometry objects to add to this component.
        """

        self._tmeshs: list[trimesh.Trimesh] = []
        self.add_geometry(geometry)

    @property
    def as_trimesh(self) -> trimesh.Trimesh:
        """
        Read only property. Returns the entire component as a single
        Unioned trimesh. This can remove color information and combines all
        underlying meshes of the component.

        See also `all_trimeshes`
        """
        tmesh: trimesh.Trimesh = trimesh.util.concatenate(self._tmeshs)
        return tmesh

    @property
    def all_trimeshes(self) -> list[trimesh.Trimesh]:
        """
        Read only property. Returns a list of each of the underlying meshes
        that make up this component. This will preserve colour, but is less
        useful than a single mesh when trying to ascertain properties such
        as the bounding box.

        See also `as_trimesh`
        """
        return self._tmeshs

    def apply_transform(
        self,
        matrix: npt.NDArray[np.float32 | np.float64]
    ) -> None:
        """
        Apply a a 3D affine transformation matrix to the geometry in this
        component

        :param matrix: A 4x4 numpy array containing the matrix. Note that
            np.matrix is not supported as it is being deprecated.
        """
        for tmesh in self._tmeshs:
            tmesh.apply_transform(matrix)

    def add_geometry(
        self,
        geometry: list[trimesh.Trimesh | Solid] | trimesh.Trimesh | Solid
    ) -> None:
        """
        Add new geometry to this component.

        :param geometry: The geometry objects to add to this component. This can be
            a solid, a trimesh or a list containing a mixutre of the two.
        """
        if not isinstance(geometry, Iterable):
            geometry = [geometry]
        for geometry_el in geometry:
            if isinstance(geometry_el, Solid):
                self._tmeshs.append(geometry_el.as_trimesh)
            elif isinstance(geometry_el, trimesh.Trimesh):
                self._tmeshs.append(deepcopy(geometry_el))
            else:
                raise TypeError(
                    'A component should be made up of trimesh or solid objects')

    def scale(self, factor: float | _Vec3) -> None:
        """
        Scale this component by a fixed factor or a 3D vector.

        :param factor: The scaling factor. To scale differently in x,y, and z you can
            enter a list or tuple of (x,y,z) scaling factors.
        """
        if not isinstance(factor, Iterable):
            factor = (factor, factor, factor)
        self.apply_transform(
            np.array([
                [factor[0], 0.0, 0.0, 1.0],
                [0.0, factor[1], 0.0, 1.0],
                [0.0, 0.0, factor[2], 1.0],
                [0.0, 0.0, 0.0, 0.0]]
            )
        )

    def translate(self, xyz: _Vec3) -> None:
        """
        Translate this Component in by a 3D vector.

        :param xyz: The (x,y,z) vector for translation.

        See also: `Component.translate_x()`, `Component.translate_y()`, and
        `Component.translate_z()`
        """
        self.apply_transform(
            np.array([
                [1.0, 0.0, 0.0, xyz[0]],
                [0.0, 1.0, 0.0, xyz[1]],
                [0.0, 0.0, 1.0, xyz[2]],
                [0.0, 0.0, 0.0, 0.0]]
            )
        )

    def translate_x(self, x: float) -> None:
        """
        Translate the Component in only the x-direction.

        :param x: The distance to translate in x.

        See also: `Component.translate()`, `Component.translate_y()`, and
        `Component.translate_z()`
        """
        self.apply_transform(
            np.array([
                [1.0, 0.0, 0.0, x],
                [0.0, 1.0, 0.0, 0.0],
                [0.0, 0.0, 1.0, 0.0],
                [0.0, 0.0, 0.0, 0.0]]
            )
        )

    def translate_y(self, y: float) -> None:
        """
        Translate the Component in only the y-direction.

        :param y: The distance to translate in y.

        See also: `Component.translate()`, `Component.translate_x()`, and
        `Component.translate_z()`
        """
        self.apply_transform(
            np.array([
                [1.0, 0.0, 0.0, 0.0],
                [0.0, 1.0, 0.0, y],
                [0.0, 0.0, 1.0, 0.0],
                [0.0, 0.0, 0.0, 0.0]]
            )
        )

    def translate_z(self, z: float) -> None:
        """
        Translate the Component in only the z-direction.

        :param z: The distance to translate in z.

        See also: `Component.translate()`, `Component.translate_x()`, and
        `Component.translate_y()`
        """
        self.apply_transform(
            np.array([
                [1.0, 0.0, 0.0, 0.0],
                [0.0, 1.0, 0.0, 0.0],
                [0.0, 0.0, 1.0, z],
                [0.0, 0.0, 0.0, 0.0]]
            )
        )

    @property
    def scene(self) -> Scene:
        """
        Read only property. Returns an `engscript.export.Scene`
        object with this set as the geometry in the scene.
        This can be used for 3D rendering.
        """
        return Scene(self.all_trimeshes)

    def export_glb(self, filename: str) -> None:
        """
        Export this component as a glb file. This is primarily used
        for 3D viewing on the web.

        :param filename: the filename of the glb file.
        """
        trimesh.exchange.export.export_mesh(self.scene.scene, filename, "glb")

    def export_stl(self, filename: str) -> None:
        """
        Export this component as an STL file. This is the standard
        file format used for 3D printing.

        Note that as the component meshes are not always watertight especially if
        they are imported from other sources like STEP files from manufacturers.
        Where possible it is best to export STLs of `engscript.engscript.Solid`
        objects rather than of components.

        :param filename: the filename of the stl file.
        """
        trimesh.exchange.export.export_mesh(self.as_trimesh, filename, "stl")
