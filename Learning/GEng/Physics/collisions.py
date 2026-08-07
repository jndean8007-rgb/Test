import numpy as np

class Collisions:
    EPSILON = 1e-8

    @staticmethod
    def check_collisions(object_pairs):
        for object_a, object_b in object_pairs:
            collision_stats = Collisions.intersects(object_a, object_b)
            if collision_stats is not None:
                Collisions.collide(*collision_stats)

    @classmethod
    def collide_with_world(cls, body, world):
        """
        Keep a body inside a rectangular world.

        Supports spheres and convex bodies with world-space vertices.
        """
        if body.properties.get("mass", 0) == 0:
            return

        world_min = np.zeros(3, dtype=float)
        world_max = np.asarray(
            world.properties["dimensions"],
            dtype=float,
        )

        shape = body.properties["shape"]

        if shape == "sphere":
            center = np.asarray(
                body.properties["center"],
                dtype=float,
            )
            radius = float(body.radius)

            body_min = center - radius
            body_max = center + radius
        else:
            vertices = cls.get_world_vertices(body)
            body_min = vertices.min(axis=0)
            body_max = vertices.max(axis=0)

        for axis in range(3):
            # Lower wall: x=0, y=0, or z=0
            if body_min[axis] < world_min[axis]:
                penetration = world_min[axis] - body_min[axis]

                inward_normal = np.zeros(3, dtype=float)
                inward_normal[axis] = 1.0

                cls.resolve_world_collision(
                    body,
                    world,
                    inward_normal,
                    penetration,
                )

            # Upper wall: x=max, y=max, or z=max
            elif body_max[axis] > world_max[axis]:
                penetration = body_max[axis] - world_max[axis]

                inward_normal = np.zeros(3, dtype=float)
                inward_normal[axis] = -1.0

                cls.resolve_world_collision(
                    body,
                    world,
                    inward_normal,
                    penetration,
                )

    @staticmethod
    def resolve_world_collision(body, world, inward_normal, penetration):
        """
        Move the body back inside and reflect its outward velocity.
        """
        center = np.asarray(
            body.properties["center"],
            dtype=float,
        )
        velocity = np.asarray(
            body.properties["velocity"],
            dtype=float,
        )

        # Positional correction.
        body.properties["center"] = (
                center + inward_normal * penetration
        )

        velocity_toward_inside = np.dot(
            velocity,
            inward_normal,
        )

        # Only reflect the velocity if the body is moving out of the world.
        if velocity_toward_inside >= 0:
            return

        body_elasticity = body.properties.get("elasticity", 0.0)
        world_elasticity = world.properties.get("elasticity", 0.0)
        elasticity = min(body_elasticity, world_elasticity)

        body.properties["velocity"] = (
                velocity
                - (1.0 + elasticity)
                * velocity_toward_inside
                * inward_normal
        )

    @staticmethod
    def sphere_sphere(a, b):
        center_a = a.properties["center"]
        center_b = b.properties["center"]

        radius_a = float(a.radius)
        radius_b = float(b.radius)

        difference = center_b - center_a
        distance_squared = difference @ difference

        radius_sum = radius_a + radius_b

        if distance_squared > radius_sum ** 2:
            return None

        distance = np.sqrt(distance_squared)

        if distance > 0:
            normal = difference / distance
        else:
            normal = np.array([1.0, 0.0, 0.0])

        penetration = radius_sum - distance

        point_on_a = center_a + normal * radius_a
        point_on_b = center_b - normal * radius_b
        contact_point = (point_on_a + point_on_b) / 2

        return a, b, contact_point, normal, penetration

    @staticmethod
    def normalize(vector):
        vector = np.asarray(vector, dtype=float)
        length = np.linalg.norm(vector)

        if length < Collisions.EPSILON:
            return None

        return vector / length

    @staticmethod
    def get_world_vertices(body):
        """
        Return an (n, 3) array containing the body's world-space vertices.
        """
        if hasattr(body, "world_vertices"):
            vertices = body.world_vertices()

        elif hasattr(body, "vertices"):
            vertices = body.vertices

        else:
            vertices = body.properties["vertices"]

        return np.asarray(vertices, dtype=float)

    @staticmethod
    def get_faces(body):
        """
        Return faces as tuples of vertex indices.

        These defaults assume the same box vertex order previously used.
        """
        if hasattr(body, "faces"):
            return body.faces

        shape = body.properties["shape"]

        if shape == "rectangle":
            return [
                (0, 1, 3, 2),  # back
                (4, 6, 7, 5),  # front
                (0, 4, 5, 1),  # bottom
                (2, 3, 7, 6),  # top
                (0, 2, 6, 4),  # left
                (1, 5, 7, 3),  # right
            ]

        if shape == "tetrahedron":
            return [
                (0, 2, 1),
                (0, 1, 3),
                (0, 3, 2),
                (1, 2, 3),
            ]

        raise ValueError(f"Faces not defined for {shape}")

    @staticmethod
    def get_edges(body):
        if hasattr(body, "edges"):
            return body.edges

        shape = body.properties["shape"]

        if shape == "rectangle":
            return [
                (0, 1), (0, 2), (0, 4),
                (1, 3), (1, 5),
                (2, 3), (2, 6),
                (3, 7),
                (4, 5), (4, 6),
                (5, 7),
                (6, 7),
            ]

        if shape == "tetrahedron":
            return [
                (0, 1),
                (0, 2),
                (0, 3),
                (1, 2),
                (1, 3),
                (2, 3),
            ]

        raise ValueError(f"Edges not defined for {shape}")

    @staticmethod
    def face_normals(vertices, faces):
        """
        Calculate one normal for each face.
        """
        normals = []

        for face in faces:
            vertex_a = vertices[face[0]]
            vertex_b = vertices[face[1]]
            vertex_c = vertices[face[2]]

            edge_ab = vertex_b - vertex_a
            edge_ac = vertex_c - vertex_a

            normal = np.cross(edge_ab, edge_ac)
            normal = Collisions.normalize(normal)

            if normal is not None:
                normals.append(normal)

        return normals

    @staticmethod
    def edge_directions(vertices, edges):
        """
        Return normalized edge directions, avoiding parallel duplicates.
        """
        directions = []

        for index_a, index_b in edges:
            direction = vertices[index_b] - vertices[index_a]
            direction = Collisions.normalize(direction)

            if direction is None:
                continue

            duplicate = any(
                abs(np.dot(direction, existing)) > 1.0 - 1e-6
                for existing in directions
            )

            if not duplicate:
                directions.append(direction)

        return directions

    @staticmethod
    def project_vertices(vertices, axis):
        projections = vertices @ axis
        return projections.min(), projections.max()

    @staticmethod
    def approximate_contact_point(vertices_a, vertices_b, normal):
        """
        Approximate a contact point using support points.

        A more advanced engine would construct a full contact manifold.
        """
        projections_a = vertices_a @ normal
        projections_b = vertices_b @ normal

        furthest_a = vertices_a[
            np.isclose(
                projections_a,
                projections_a.max(),
                atol=1e-6,
            )
        ]

        furthest_b = vertices_b[
            np.isclose(
                projections_b,
                projections_b.min(),
                atol=1e-6,
            )
        ]

        point_a = np.mean(furthest_a, axis=0)
        point_b = np.mean(furthest_b, axis=0)

        return (point_a + point_b) / 2

    @staticmethod
    def sat_collision(a, b):
        """
        SAT collision test for two convex polyhedra.

        Returns:
            (a, b, contact_point, normal, penetration)

        The normal points from a toward b.
        """
        vertices_a = Collisions.get_world_vertices(a)
        vertices_b = Collisions.get_world_vertices(b)

        faces_a = Collisions.get_faces(a)
        faces_b = Collisions.get_faces(b)

        edges_a = Collisions.get_edges(a)
        edges_b = Collisions.get_edges(b)

        normals_a = Collisions.face_normals(vertices_a, faces_a)
        normals_b = Collisions.face_normals(vertices_b, faces_b)

        directions_a = Collisions.edge_directions(vertices_a, edges_a)
        directions_b = Collisions.edge_directions(vertices_b, edges_b)

        candidate_axes = []
        candidate_axes.extend(normals_a)
        candidate_axes.extend(normals_b)

        # Edge-edge separating axes.
        for edge_a in directions_a:
            for edge_b in directions_b:
                axis = np.cross(edge_a, edge_b)
                axis = Collisions.normalize(axis)

                if axis is not None:
                    candidate_axes.append(axis)

        smallest_overlap = np.inf
        collision_normal = None

        center_a = np.mean(vertices_a, axis=0)
        center_b = np.mean(vertices_b, axis=0)
        center_difference = center_b - center_a

        for axis in candidate_axes:
            axis = Collisions.normalize(axis)

            if axis is None:
                continue

            min_a, max_a = Collisions.project_vertices(
                vertices_a,
                axis,
            )

            min_b, max_b = Collisions.project_vertices(
                vertices_b,
                axis,
            )

            overlap = min(max_a, max_b) - max(min_a, min_b)

            # A separating axis means no collision.
            if overlap < 0:
                return None

            if overlap < smallest_overlap:
                smallest_overlap = overlap
                collision_normal = axis

        if collision_normal is None:
            return None

        # Ensure normal points from A toward B.
        if np.dot(center_difference, collision_normal) < 0:
            collision_normal = -collision_normal

        contact_point = Collisions.approximate_contact_point(
            vertices_a,
            vertices_b,
            collision_normal,
        )

        return (
            a,
            b,
            contact_point,
            collision_normal,
            smallest_overlap,
        )

    # ---------------------------------------------------------
    # Closest-point helpers
    # ---------------------------------------------------------

    @staticmethod
    def closest_point_on_triangle(point, triangle_a, triangle_b, triangle_c):
        """
        Return the closest point on a triangle to a given point.

        Based on region tests around the triangle's vertices and edges.
        """
        ab = triangle_b - triangle_a
        ac = triangle_c - triangle_a
        ap = point - triangle_a

        d1 = np.dot(ab, ap)
        d2 = np.dot(ac, ap)

        if d1 <= 0 and d2 <= 0:
            return triangle_a

        bp = point - triangle_b
        d3 = np.dot(ab, bp)
        d4 = np.dot(ac, bp)

        if d3 >= 0 and d4 <= d3:
            return triangle_b

        vc = d1 * d4 - d3 * d2

        if vc <= 0 and d1 >= 0 and d3 <= 0:
            denominator = d1 - d3

            if abs(denominator) < Collisions.EPSILON:
                return triangle_a

            interpolation = d1 / denominator
            return triangle_a + interpolation * ab

        cp = point - triangle_c
        d5 = np.dot(ab, cp)
        d6 = np.dot(ac, cp)

        if d6 >= 0 and d5 <= d6:
            return triangle_c

        vb = d5 * d2 - d1 * d6

        if vb <= 0 and d2 >= 0 and d6 <= 0:
            denominator = d2 - d6

            if abs(denominator) < Collisions.EPSILON:
                return triangle_a

            interpolation = d2 / denominator
            return triangle_a + interpolation * ac

        va = d3 * d6 - d5 * d4

        if va <= 0 and (d4 - d3) >= 0 and (d5 - d6) >= 0:
            bc = triangle_c - triangle_b

            denominator = (
                    d4 - d3
                    + d5 - d6
            )

            if abs(denominator) < Collisions.EPSILON:
                return triangle_b

            interpolation = (d4 - d3) / denominator
            return triangle_b + interpolation * bc

        denominator = va + vb + vc

        if abs(denominator) < Collisions.EPSILON:
            return triangle_a

        inverse_denominator = 1.0 / denominator

        v = vb * inverse_denominator
        w = vc * inverse_denominator

        return triangle_a + ab * v + ac * w

    @staticmethod
    def point_inside_convex_polyhedron(point, vertices, faces):
        """
        Determine whether a point lies inside a convex polyhedron.

        Face normals are automatically oriented away from the centroid.
        """
        centroid = np.mean(vertices, axis=0)

        for face in faces:
            vertex_a = vertices[face[0]]
            vertex_b = vertices[face[1]]
            vertex_c = vertices[face[2]]

            normal = np.cross(
                vertex_b - vertex_a,
                vertex_c - vertex_a,
            )

            normal = Collisions.normalize(normal)

            if normal is None:
                continue

            face_center = np.mean(vertices[list(face)], axis=0)

            # Make normal point outward.
            if np.dot(normal, face_center - centroid) < 0:
                normal = -normal

            if np.dot(normal, point - vertex_a) > Collisions.EPSILON:
                return False

        return True

    # ---------------------------------------------------------
    # Sphere–rectangle
    # ---------------------------------------------------------

    @staticmethod
    def sphere_rectangle(sphere, rectangle):
        sphere_center = np.asarray(
            sphere.properties["center"],
            dtype=float,
        )

        box_center = np.asarray(
            rectangle.properties["center"],
            dtype=float,
        )

        radius = float(sphere.radius)

        rotation = rectangle.rotation_matrix
        half_extents = rectangle.half_extents

        # Move the sphere center into box-local coordinates.
        local_center = rotation.T @ (
                sphere_center - box_center
        )

        closest_local = np.clip(
            local_center,
            -half_extents,
            half_extents,
        )

        closest_world = (
                box_center
                + rotation @ closest_local
        )

        difference = closest_world - sphere_center
        distance_squared = np.dot(difference, difference)

        # Sphere center is outside the box.
        if distance_squared > Collisions.EPSILON:
            if distance_squared > radius ** 2:
                return None

            distance = np.sqrt(distance_squared)
            normal = difference / distance
            penetration = radius - distance
            contact_point = closest_world

            return (
                sphere,
                rectangle,
                contact_point,
                normal,
                penetration,
            )

        # Sphere center is inside the box.
        distances_to_faces = (
                half_extents - np.abs(local_center)
        )

        nearest_axis = int(np.argmin(distances_to_faces))
        distance_to_face = distances_to_faces[nearest_axis]

        outward_local = np.zeros(3, dtype=float)

        if local_center[nearest_axis] >= 0:
            outward_local[nearest_axis] = 1.0
        else:
            outward_local[nearest_axis] = -1.0

        outward_world = rotation @ outward_local

        # The solver moves sphere by -normal, so normal must point inward.
        normal = -outward_world

        contact_local = local_center.copy()
        contact_local[nearest_axis] = (
                outward_local[nearest_axis]
                * half_extents[nearest_axis]
        )

        contact_point = (
                box_center
                + rotation @ contact_local
        )

        penetration = radius + distance_to_face

        return (
            sphere,
            rectangle,
            contact_point,
            normal,
            penetration,
        )

    # ---------------------------------------------------------
    # Rectangle–rectangle
    # ---------------------------------------------------------

    @staticmethod
    def rectangle_rectangle(a, b):
        return Collisions.sat_collision(a, b)

    # ---------------------------------------------------------
    # Tetrahedron–rectangle
    # ---------------------------------------------------------

    @staticmethod
    def tetrahedron_rectangle(tetrahedron, rectangle):
        return Collisions.sat_collision(
            tetrahedron,
            rectangle,
        )

    # ---------------------------------------------------------
    # Tetrahedron–tetrahedron
    # ---------------------------------------------------------

    @staticmethod
    def tetrahedron_tetrahedron(a, b):
        return Collisions.sat_collision(a, b)

    # ---------------------------------------------------------
    # Tetrahedron–sphere
    # ---------------------------------------------------------

    @staticmethod
    def tetrahedron_sphere(tetrahedron, sphere):
        vertices = Collisions.get_world_vertices(tetrahedron)
        faces = Collisions.get_faces(tetrahedron)

        sphere_center = np.asarray(
            sphere.properties["center"],
            dtype=float,
        )

        radius = float(sphere.radius)

        inside = Collisions.point_inside_convex_polyhedron(
            sphere_center,
            vertices,
            faces,
        )

        closest_point = None
        smallest_distance_squared = np.inf
        closest_outward_normal = None

        tetrahedron_center = np.mean(vertices, axis=0)

        for face in faces:
            vertex_a = vertices[face[0]]
            vertex_b = vertices[face[1]]
            vertex_c = vertices[face[2]]

            candidate = Collisions.closest_point_on_triangle(
                sphere_center,
                vertex_a,
                vertex_b,
                vertex_c,
            )

            difference = sphere_center - candidate
            distance_squared = np.dot(difference, difference)

            if distance_squared < smallest_distance_squared:
                smallest_distance_squared = distance_squared
                closest_point = candidate

                face_normal = np.cross(
                    vertex_b - vertex_a,
                    vertex_c - vertex_a,
                )

                face_normal = Collisions.normalize(face_normal)

                if face_normal is not None:
                    face_center = np.mean(
                        vertices[list(face)],
                        axis=0,
                    )

                    if np.dot(
                            face_normal,
                            face_center - tetrahedron_center,
                    ) < 0:
                        face_normal = -face_normal

                closest_outward_normal = face_normal

        if closest_point is None:
            return None

        distance = np.sqrt(smallest_distance_squared)

        if not inside and distance > radius:
            return None

        if inside:
            if closest_outward_normal is None:
                return None

            normal = closest_outward_normal

            # The sphere must travel to the surface, plus its radius.
            penetration = distance + radius

        else:
            if distance > Collisions.EPSILON:
                normal = (
                                 sphere_center - closest_point
                         ) / distance
            else:
                if closest_outward_normal is None:
                    return None

                normal = closest_outward_normal

            penetration = radius - distance

        return (
            tetrahedron,
            sphere,
            closest_point,
            normal,
            penetration,
        )

    @classmethod
    def intersects(cls, a, b):
        shape_pair = (
            a.properties["shape"],
            b.properties["shape"],
        )

        checks = {
            ("sphere", "sphere"): cls.sphere_sphere,
            ("sphere", "rectangle"): cls.sphere_rectangle,
            ("rectangle", "rectangle"): cls.rectangle_rectangle,
            ("tetrahedron", "sphere"): cls.tetrahedron_sphere,
            ("tetrahedron", "rectangle"): cls.tetrahedron_rectangle,
            ("tetrahedron", "tetrahedron"): cls.tetrahedron_tetrahedron,
        }

        check = checks.get(shape_pair)

        if check is not None:
            return check(a, b)

        reverse_pair = shape_pair[::-1]
        reverse_check = checks.get(reverse_pair)

        if reverse_check is not None:
            result = reverse_check(b, a)

            if result is None:
                return None

            body_b, body_a, point, normal, penetration = result

            return body_a, body_b, point, -normal, penetration

        raise NotImplementedError(
            f"No collision algorithm for {shape_pair}"
        )

    @staticmethod
    def collide(a, b, point, normal, penetration):
        velocity_a = a.properties["velocity"]
        velocity_b = b.properties["velocity"]

        mass_a = a.properties["mass"]
        mass_b = b.properties["mass"]

        inverse_mass_a = 0.0 if mass_a == 0 else 1.0 / mass_a
        inverse_mass_b = 0.0 if mass_b == 0 else 1.0 / mass_b

        total_inverse_mass = inverse_mass_a + inverse_mass_b

        if total_inverse_mass == 0:
            return

        # Move overlapping bodies apart.
        correction = normal * penetration / total_inverse_mass

        a.properties["center"] -= correction * inverse_mass_a
        b.properties["center"] += correction * inverse_mass_b

        relative_velocity = velocity_b - velocity_a
        velocity_along_normal = np.dot(relative_velocity, normal)

        # They are already separating, so do not add another impulse.
        if velocity_along_normal > 0:
            return

        elasticity_a = a.properties.get("elasticity", 0.0)
        elasticity_b = b.properties.get("elasticity", 0.0)

        # Use the less elastic body.
        elasticity = min(elasticity_a, elasticity_b)

        impulse_magnitude = (
            -(1.0 + elasticity)
            * velocity_along_normal
            / total_inverse_mass
        )

        impulse = impulse_magnitude * normal

        a.properties["velocity"] -= impulse * inverse_mass_a
        b.properties["velocity"] += impulse * inverse_mass_b