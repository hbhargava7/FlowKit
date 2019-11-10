import unittest
import sys
import os
import numpy as np
import pandas as pd

sys.path.append(os.path.abspath('..'))

import flowkit as fk

data1_fcs_path = 'examples/gate_ref/data1.fcs'
data1_sample = fk.Sample(data1_fcs_path)

quadrants_q1 = {
            'FL2P-FL4P': [
                {
                    'divider': 'FL2',
                    'dimension': 'FL2-H',
                    'location': 15.0,
                    'min': 12.14748,
                    'max': None
                },
                {
                    'divider': 'FL4',
                    'dimension': 'FL4-H',
                    'location': 15.0,
                    'min': 14.22417,
                    'max': None
                }
            ],
            'FL2N-FL4P': [
                {
                    'divider': 'FL2',
                    'dimension': 'FL2-H',
                    'location': 5.0,
                    'min': None,
                    'max': 12.14748
                },
                {
                    'divider': 'FL4',
                    'dimension': 'FL4-H',
                    'location': 15.0,
                    'min': 14.22417,
                    'max': None
                }
            ],
            'FL2N-FL4N': [
                {
                    'divider': 'FL2',
                    'dimension': 'FL2-H',
                    'location': 5.0,
                    'min': None,
                    'max': 12.14748
                },
                {
                    'divider': 'FL4',
                    'dimension': 'FL4-H',
                    'location': 5.0,
                    'min': None,
                    'max': 14.22417
                }
            ],
            'FL2P-FL4N': [
                {
                    'divider': 'FL2',
                    'dimension': 'FL2-H',
                    'location': 15.0,
                    'min': 12.14748,
                    'max': None
                },
                {
                    'divider': 'FL4',
                    'dimension': 'FL4-H',
                    'location': 5.0,
                    'min': None,
                    'max': 14.22417
                }
            ]
        }

quadrants_q2 = {
    'FSCD-FL1P': [
        {
            'dimension': 'FSC-H',
            'divider': 'FSC',
            'location': 30.0,
            'max': 70.02725,
            'min': 28.0654},
        {
            'dimension': 'FL1-H',
            'divider': 'FL1',
            'location': 10.0,
            'max': None,
            'min': 6.43567
        }
    ],
    'FSCD-SSCN-FL1N': [
        {
            'dimension': 'FSC-H',
            'divider': 'FSC',
            'location': 30.0,
            'max': 70.02725,
            'min': 28.0654
        },
        {
            'dimension': 'SSC-H',
            'divider': 'SSC',
            'location': 10.0,
            'max': 17.75,
            'min': None
        },
        {
            'dimension': 'FL1-H',
            'divider': 'FL1',
            'location': 5.0,
            'max': 6.43567,
            'min': None
        }
    ],
    'FSCN-SSCN': [
        {
            'dimension': 'FSC-H',
            'divider': 'FSC',
            'location': 10.0,
            'max': 28.0654,
            'min': None
        },
        {
            'dimension': 'SSC-H',
            'divider': 'SSC',
            'location': 10.0,
            'max': 17.75,
            'min': None
        }
    ],
    'FSCN-SSCP-FL1P': [
        {
            'dimension': 'FSC-H',
            'divider': 'FSC',
            'location': 10.0,
            'max': 28.0654,
            'min': None
        },
        {
            'dimension': 'SSC-H',
            'divider': 'SSC',
            'location': 20.0,
            'max': None,
            'min': 17.75
        },
        {
            'dimension': 'FL1-H',
            'divider': 'FL1',
            'location': 15.0,
            'max': None,
            'min': 6.43567
        }
    ],
    'FSCP-SSCN-FL1N': [
        {
            'dimension': 'FSC-H',
            'divider': 'FSC',
            'location': 80.0,
            'max': None,
            'min': 70.02725
        },
        {
            'dimension': 'SSC-H',
            'divider': 'SSC',
            'location': 10.0,
            'max': 17.75,
            'min': None
        },
        {
            'dimension': 'FL1-H',
            'divider': 'FL1',
            'location': 5.0,
            'max': 6.43567,
            'min': None
        }
    ]
}


class GatingTestCase(unittest.TestCase):
    @staticmethod
    def test_add_min_range_gate():
        res_path = 'examples/gate_ref/truth/Results_Range1.txt'

        gs = fk.GatingStrategy()

        dim1 = fk.Dimension("FSC-H", compensation_ref="uncompensated", range_min=100)
        dims = [dim1]

        rect_gate = fk.gates.RectangleGate("Range1", None, dims, gs)
        gs.add_gate(rect_gate)

        truth = pd.read_csv(res_path, header=None, squeeze=True, dtype='bool').values

        result = gs.gate_sample(data1_sample, 'Range1')

        np.testing.assert_array_equal(truth, result.get_gate_indices('Range1'))

    @staticmethod
    def test_add_rect1_gate():
        gs = fk.GatingStrategy()

        dim1 = fk.Dimension("SSC-H", compensation_ref="uncompensated", range_min=20, range_max=80)
        dim2 = fk.Dimension("FL1-H", compensation_ref="uncompensated", range_min=70, range_max=200)
        dims = [dim1, dim2]

        rect_gate = fk.gates.RectangleGate("Rectangle1", None, dims, gs)
        gs.add_gate(rect_gate)

        res_path = 'examples/gate_ref/truth/Results_Rectangle1.txt'
        truth = pd.read_csv(res_path, header=None, squeeze=True, dtype='bool').values

        result = gs.gate_sample(data1_sample, 'Rectangle1')

        np.testing.assert_array_equal(truth, result.get_gate_indices('Rectangle1'))

    @staticmethod
    def test_add_rect2_gate():
        gs = fk.GatingStrategy()

        dim1 = fk.Dimension("SSC-H", compensation_ref="FCS", range_min=20, range_max=80)
        dim2 = fk.Dimension("FL1-H", compensation_ref="FCS", range_min=70, range_max=200)
        dims = [dim1, dim2]

        rect_gate = fk.gates.RectangleGate("Rectangle2", None, dims, gs)
        gs.add_gate(rect_gate)

        res_path = 'examples/gate_ref/truth/Results_Rectangle2.txt'
        truth = pd.read_csv(res_path, header=None, squeeze=True, dtype='bool').values

        result = gs.gate_sample(data1_sample, 'Rectangle2')

        np.testing.assert_array_equal(truth, result.get_gate_indices('Rectangle2'))

    @staticmethod
    def test_add_poly1_gate():
        gs = fk.GatingStrategy()

        dim1 = fk.Dimension("FL2-H", compensation_ref="FCS")
        dim2 = fk.Dimension("FL3-H", compensation_ref="FCS")
        dims = [dim1, dim2]

        vertices = [
            fk.Vertex([5, 5]),
            fk.Vertex([500, 5]),
            fk.Vertex([500, 500])
        ]

        poly_gate = fk.gates.PolygonGate("Polygon1", None, dims, vertices, gs)
        gs.add_gate(poly_gate)

        res_path = 'examples/gate_ref/truth/Results_Polygon1.txt'
        truth = pd.read_csv(res_path, header=None, squeeze=True, dtype='bool').values

        result = gs.gate_sample(data1_sample, 'Polygon1')

        np.testing.assert_array_equal(truth, result.get_gate_indices('Polygon1'))

    @staticmethod
    def test_add_poly2_gate():
        gs = fk.GatingStrategy()

        dim1 = fk.Dimension("FL1-H", compensation_ref="FCS")
        dim2 = fk.Dimension("FL4-H", compensation_ref="FCS")
        dims = [dim1, dim2]

        vertices = [
            fk.Vertex([20, 10]),
            fk.Vertex([120, 10]),
            fk.Vertex([120, 160]),
            fk.Vertex([20, 160])
        ]

        poly_gate = fk.gates.PolygonGate("Polygon2", None, dims, vertices, gs)
        gs.add_gate(poly_gate)

        res_path = 'examples/gate_ref/truth/Results_Polygon2.txt'
        truth = pd.read_csv(res_path, header=None, squeeze=True, dtype='bool').values

        result = gs.gate_sample(data1_sample, 'Polygon2')

        np.testing.assert_array_equal(truth, result.get_gate_indices('Polygon2'))

    @staticmethod
    def test_add_poly3_non_solid_gate():
        gs = fk.GatingStrategy()

        dim1 = fk.Dimension("SSC-H", compensation_ref="uncompensated")
        dim2 = fk.Dimension("FL3-H", compensation_ref="FCS")
        dims = [dim1, dim2]

        vertices = [
            fk.Vertex([10, 10]),
            fk.Vertex([500, 10]),
            fk.Vertex([500, 390]),
            fk.Vertex([100, 390]),
            fk.Vertex([100, 180]),
            fk.Vertex([200, 180]),
            fk.Vertex([200, 300]),
            fk.Vertex([10, 300])
        ]

        poly_gate = fk.gates.PolygonGate("Polygon3NS", None, dims, vertices, gs)
        gs.add_gate(poly_gate)

        res_path = 'examples/gate_ref/truth/Results_Polygon3NS.txt'
        truth = pd.read_csv(res_path, header=None, squeeze=True, dtype='bool').values

        result = gs.gate_sample(data1_sample, 'Polygon3NS')

        np.testing.assert_array_equal(truth, result.get_gate_indices('Polygon3NS'))

    @staticmethod
    def test_add_ellipse1_gate():
        gs = fk.GatingStrategy()

        dim1 = fk.Dimension("FL3-H", compensation_ref="uncompensated")
        dim2 = fk.Dimension("FL4-H", compensation_ref="uncompensated")
        dims = [dim1, dim2]

        coords = [12.99701, 16.22941]
        cov_mat = [[62.5, 37.5], [37.5, 62.5]]
        dist_square = 1

        ellipse_gate = fk.gates.EllipsoidGate("Ellipse1", None, dims, coords, cov_mat, dist_square, gs)
        gs.add_gate(ellipse_gate)

        res_path = 'examples/gate_ref/truth/Results_Ellipse1.txt'
        truth = pd.read_csv(res_path, header=None, squeeze=True, dtype='bool').values

        result = gs.gate_sample(data1_sample, 'Ellipse1')

        np.testing.assert_array_equal(truth, result.get_gate_indices('Ellipse1'))

    @staticmethod
    def test_add_ellipsoid_3d_gate():
        gs = fk.GatingStrategy()

        dim1 = fk.Dimension("FL3-H", compensation_ref="FCS")
        dim2 = fk.Dimension("FL4-H", compensation_ref="FCS")
        dim3 = fk.Dimension("FL1-H", compensation_ref="FCS")
        dims = [dim1, dim2, dim3]

        coords = [40.3, 30.6, 20.8]
        cov_mat = [[2.5, 7.5, 17.5], [7.5, 7.0, 13.5], [15.5, 13.5, 4.3]]
        dist_square = 1

        poly_gate = fk.gates.EllipsoidGate("Ellipsoid3D", None, dims, coords, cov_mat, dist_square, gs)
        gs.add_gate(poly_gate)

        res_path = 'examples/gate_ref/truth/Results_Ellipsoid3D.txt'
        truth = pd.read_csv(res_path, header=None, squeeze=True, dtype='bool').values

        result = gs.gate_sample(data1_sample, 'Ellipsoid3D')

        np.testing.assert_array_equal(truth, result.get_gate_indices('Ellipsoid3D'))

    @staticmethod
    def test_add_time_range_gate():
        res_path = 'examples/gate_ref/truth/Results_Range2.txt'

        gs = fk.GatingStrategy()

        dim1 = fk.Dimension("Time", compensation_ref="uncompensated", range_min=20, range_max=80)
        dims = [dim1]

        rect_gate = fk.gates.RectangleGate("Range2", None, dims, gs)
        gs.add_gate(rect_gate)

        truth = pd.read_csv(res_path, header=None, squeeze=True, dtype='bool').values

        result = gs.gate_sample(data1_sample, 'Range2')

        np.testing.assert_array_equal(truth, result.get_gate_indices('Range2'))

    @staticmethod
    def test_add_quadrant1_gate():
        res1_path = 'examples/gate_ref/truth/Results_FL2N-FL4N.txt'
        res2_path = 'examples/gate_ref/truth/Results_FL2N-FL4P.txt'
        res3_path = 'examples/gate_ref/truth/Results_FL2P-FL4N.txt'
        res4_path = 'examples/gate_ref/truth/Results_FL2P-FL4P.txt'

        gs = fk.GatingStrategy()

        div1 = fk.QuadrantDivider("FL2", "FL2-H", "FCS", [12.14748])
        div2 = fk.QuadrantDivider("FL4", "FL4-H", "FCS", [14.22417])

        divs = [div1, div2]

        quad_gate = fk.gates.QuadrantGate("Quadrant1", None, divs, quadrants_q1, gs)
        gs.add_gate(quad_gate)

        truth1 = pd.read_csv(res1_path, header=None, squeeze=True, dtype='bool').values
        truth2 = pd.read_csv(res2_path, header=None, squeeze=True, dtype='bool').values
        truth3 = pd.read_csv(res3_path, header=None, squeeze=True, dtype='bool').values
        truth4 = pd.read_csv(res4_path, header=None, squeeze=True, dtype='bool').values

        result = gs.gate_sample(data1_sample)

        np.testing.assert_array_equal(truth1, result.get_gate_indices('FL2N-FL4N'))
        np.testing.assert_array_equal(truth2, result.get_gate_indices('FL2N-FL4P'))
        np.testing.assert_array_equal(truth3, result.get_gate_indices('FL2P-FL4N'))
        np.testing.assert_array_equal(truth4, result.get_gate_indices('FL2P-FL4P'))

    def test_add_quadrant_gate_relative_percent(self):
        gs = fk.GatingStrategy()

        div1 = fk.QuadrantDivider("FL2", "FL2-H", "FCS", [12.14748])
        div2 = fk.QuadrantDivider("FL4", "FL4-H", "FCS", [14.22417])

        divs = [div1, div2]

        quad_gate = fk.gates.QuadrantGate("Quadrant1", None, divs, quadrants_q1, gs)
        gs.add_gate(quad_gate)

        result = gs.gate_sample(data1_sample)

        total_percent = result.get_gate_relative_percent('FL2N-FL4N') + \
            result.get_gate_relative_percent('FL2N-FL4P') + \
            result.get_gate_relative_percent('FL2P-FL4N') + \
            result.get_gate_relative_percent('FL2P-FL4P')

        self.assertEqual(100.0, total_percent)

    @staticmethod
    def test_add_quadrant2_gate():
        res1_path = 'examples/gate_ref/truth/Results_FSCN-SSCN.txt'
        res2_path = 'examples/gate_ref/truth/Results_FSCD-SSCN-FL1N.txt'
        res3_path = 'examples/gate_ref/truth/Results_FSCP-SSCN-FL1N.txt'
        res4_path = 'examples/gate_ref/truth/Results_FSCD-FL1P.txt'
        res5_path = 'examples/gate_ref/truth/Results_FSCN-SSCP-FL1P.txt'

        truth1 = pd.read_csv(res1_path, header=None, squeeze=True, dtype='bool').values
        truth2 = pd.read_csv(res2_path, header=None, squeeze=True, dtype='bool').values
        truth3 = pd.read_csv(res3_path, header=None, squeeze=True, dtype='bool').values
        truth4 = pd.read_csv(res4_path, header=None, squeeze=True, dtype='bool').values
        truth5 = pd.read_csv(res5_path, header=None, squeeze=True, dtype='bool').values

        gs = fk.GatingStrategy()

        div1 = fk.QuadrantDivider("FSC", "FSC-H", "uncompensated", [28.0654, 70.02725])
        div2 = fk.QuadrantDivider("SSC", "SSC-H", "uncompensated", [17.75])
        div3 = fk.QuadrantDivider("FL1", "FL1-H", "uncompensated", [6.43567])

        divs = [div1, div2, div3]

        quad_gate = fk.gates.QuadrantGate("Quadrant2", None, divs, quadrants_q2, gs)
        gs.add_gate(quad_gate)

        result = gs.gate_sample(data1_sample)

        np.testing.assert_array_equal(truth1, result.get_gate_indices('FSCN-SSCN'))
        np.testing.assert_array_equal(truth2, result.get_gate_indices('FSCD-SSCN-FL1N'))
        np.testing.assert_array_equal(truth3, result.get_gate_indices('FSCP-SSCN-FL1N'))
        np.testing.assert_array_equal(truth4, result.get_gate_indices('FSCD-FL1P'))
        np.testing.assert_array_equal(truth5, result.get_gate_indices('FSCN-SSCP-FL1P'))

    @staticmethod
    def test_add_ratio_range1_gate():
        gs = fk.GatingStrategy()

        rat_xform = fk.transforms.RatioTransform(
            "FL2Rat1",
            ["FL2-H", "FL2-A"],
            param_a=1,
            param_b=0,
            param_c=-1
        )
        gs.add_transform(rat_xform)

        dim_rat1 = fk.RatioDimension(
            "FL2Rat1",
            compensation_ref="uncompensated",
            range_min=3,
            range_max=16.4
        )
        dims = [dim_rat1]

        rect_gate = fk.gates.RectangleGate("RatRange1", None, dims, gs)
        gs.add_gate(rect_gate)

        res_path = 'examples/gate_ref/truth/Results_RatRange1.txt'
        truth = pd.read_csv(res_path, header=None, squeeze=True, dtype='bool').values

        result = gs.gate_sample(data1_sample, 'RatRange1')

        np.testing.assert_array_equal(truth, result.get_gate_indices('RatRange1'))

    @staticmethod
    def test_add_ratio_range2_gate():
        gs = fk.GatingStrategy()

        rat_xform = fk.transforms.RatioTransform(
            "FL2Rat2",
            ["FL2-H", "FL2-A"],
            param_a=2.7,
            param_b=-100,
            param_c=-300
        )
        gs.add_transform(rat_xform)

        dim_rat2 = fk.RatioDimension(
            "FL2Rat2",
            compensation_ref="uncompensated",
            range_min=0.95,
            range_max=1.05
        )
        dims = [dim_rat2]

        rect_gate = fk.gates.RectangleGate("RatRange2", None, dims, gs)
        gs.add_gate(rect_gate)

        res_path = 'examples/gate_ref/truth/Results_RatRange2.txt'
        truth = pd.read_csv(res_path, header=None, squeeze=True, dtype='bool').values

        result = gs.gate_sample(data1_sample, 'RatRange2')

        np.testing.assert_array_equal(truth, result.get_gate_indices('RatRange2'))

    @staticmethod
    def test_add_log_ratio_range1_gate():
        gs = fk.GatingStrategy()

        rat_xform = fk.transforms.RatioTransform(
            "FL2Rat1",
            ["FL2-H", "FL2-A"],
            param_a=1,
            param_b=0,
            param_c=-1
        )
        gs.add_transform(rat_xform)

        log_rat_xform = fk.transforms.LogTransform("MyRatLog", param_t=100, param_m=2)
        gs.add_transform(log_rat_xform)

        dim_rat1 = fk.RatioDimension(
            "FL2Rat1",
            compensation_ref="uncompensated",
            transformation_ref="MyRatLog",
            range_min=0.40625,
            range_max=0.6601562
        )
        dims = [dim_rat1]

        rect_gate = fk.gates.RectangleGate("RatRange1a", None, dims, gs)
        gs.add_gate(rect_gate)

        res_path = 'examples/gate_ref/truth/Results_RatRange1a.txt'
        truth = pd.read_csv(res_path, header=None, squeeze=True, dtype='bool').values

        result = gs.gate_sample(data1_sample, 'RatRange1a')

        np.testing.assert_array_equal(truth, result.get_gate_indices('RatRange1a'))

    @staticmethod
    def test_add_boolean_and1_gate():
        gs = fk.GatingStrategy()

        dim1 = fk.Dimension("FL2-H", compensation_ref="FCS")
        dim2 = fk.Dimension("FL3-H", compensation_ref="FCS")
        dims = [dim1, dim2]

        vertices = [
            fk.Vertex([5, 5]),
            fk.Vertex([500, 5]),
            fk.Vertex([500, 500])
        ]

        poly_gate = fk.gates.PolygonGate("Polygon1", None, dims, vertices, gs)
        gs.add_gate(poly_gate)

        dim3 = fk.Dimension("Time", compensation_ref="uncompensated", range_min=20, range_max=80)
        dims2 = [dim3]

        rect_gate = fk.gates.RectangleGate("Range2", None, dims2, gs)
        gs.add_gate(rect_gate)

        gate_refs = [
            {
                'ref': 'Polygon1',
                'complement': False
            },
            {
                'ref': 'Range2',
                'complement': False
            }
        ]

        bool_gate = fk.gates.BooleanGate("And1", None, "and", gate_refs, gs)
        gs.add_gate(bool_gate)

        res_path = 'examples/gate_ref/truth/Results_And1.txt'
        truth = pd.read_csv(res_path, header=None, squeeze=True, dtype='bool').values

        result = gs.gate_sample(data1_sample, 'And1')

        np.testing.assert_array_equal(truth, result.get_gate_indices('And1'))

    @staticmethod
    def test_add_boolean_and2_gate():
        gs = fk.GatingStrategy()

        dim1 = fk.Dimension("FSC-H", compensation_ref="uncompensated", range_min=100)
        rect_dims = [dim1]

        rect_gate = fk.gates.RectangleGate("Range1", None, rect_dims, gs)
        gs.add_gate(rect_gate)

        dim2 = fk.Dimension("FL2-H", compensation_ref="FCS")
        dim3 = fk.Dimension("FL3-H", compensation_ref="FCS")
        poly_dims = [dim2, dim3]

        vertices = [
            fk.Vertex([5, 5]),
            fk.Vertex([500, 5]),
            fk.Vertex([500, 500])
        ]

        poly_gate = fk.gates.PolygonGate("Polygon1", None, poly_dims, vertices, gs)
        gs.add_gate(poly_gate)

        dim4 = fk.Dimension("FL3-H", compensation_ref="uncompensated")
        dim5 = fk.Dimension("FL4-H", compensation_ref="uncompensated")
        ellipse_dims = [dim4, dim5]

        coords = [12.99701, 16.22941]
        cov_mat = [[62.5, 37.5], [37.5, 62.5]]
        dist_square = 1

        ellipse_gate = fk.gates.EllipsoidGate("Ellipse1", None, ellipse_dims, coords, cov_mat, dist_square, gs)
        gs.add_gate(ellipse_gate)

        gate_refs = [
            {
                'ref': 'Range1',
                'complement': False
            },
            {
                'ref': 'Ellipse1',
                'complement': False
            },
            {
                'ref': 'Polygon1',
                'complement': False
            }
        ]

        bool_gate = fk.gates.BooleanGate("And2", None, "and", gate_refs, gs)
        gs.add_gate(bool_gate)

        res_path = 'examples/gate_ref/truth/Results_And2.txt'
        truth = pd.read_csv(res_path, header=None, squeeze=True, dtype='bool').values

        result = gs.gate_sample(data1_sample, 'And2')

        np.testing.assert_array_equal(truth, result.get_gate_indices('And2'))

    @staticmethod
    def test_add_boolean_or1_gate():
        gs = fk.GatingStrategy()

        dim1 = fk.Dimension("FSC-H", compensation_ref="uncompensated", range_min=100)
        rect_dims = [dim1]

        rect_gate = fk.gates.RectangleGate("Range1", None, rect_dims, gs)
        gs.add_gate(rect_gate)

        dim2 = fk.Dimension("FL2-H", compensation_ref="FCS")
        dim3 = fk.Dimension("FL3-H", compensation_ref="FCS")
        poly_dims = [dim2, dim3]

        vertices = [
            fk.Vertex([5, 5]),
            fk.Vertex([500, 5]),
            fk.Vertex([500, 500])
        ]

        poly_gate = fk.gates.PolygonGate("Polygon1", None, poly_dims, vertices, gs)
        gs.add_gate(poly_gate)

        dim4 = fk.Dimension("FL3-H", compensation_ref="uncompensated")
        dim5 = fk.Dimension("FL4-H", compensation_ref="uncompensated")
        ellipse_dims = [dim4, dim5]

        coords = [12.99701, 16.22941]
        cov_mat = [[62.5, 37.5], [37.5, 62.5]]
        dist_square = 1

        ellipse_gate = fk.gates.EllipsoidGate("Ellipse1", None, ellipse_dims, coords, cov_mat, dist_square, gs)
        gs.add_gate(ellipse_gate)

        gate_refs = [
            {
                'ref': 'Range1',
                'complement': False
            },
            {
                'ref': 'Ellipse1',
                'complement': False
            },
            {
                'ref': 'Polygon1',
                'complement': False
            }
        ]

        bool_gate = fk.gates.BooleanGate("Or1", None, "or", gate_refs, gs)
        gs.add_gate(bool_gate)

        res_path = 'examples/gate_ref/truth/Results_Or1.txt'
        truth = pd.read_csv(res_path, header=None, squeeze=True, dtype='bool').values

        result = gs.gate_sample(data1_sample, 'Or1')

        np.testing.assert_array_equal(truth, result.get_gate_indices('Or1'))

    @staticmethod
    def test_add_boolean_and3_complement_gate():
        gs = fk.GatingStrategy()

        dim1 = fk.Dimension("FSC-H", compensation_ref="uncompensated", range_min=100)
        rect_dims = [dim1]

        rect_gate = fk.gates.RectangleGate("Range1", None, rect_dims, gs)
        gs.add_gate(rect_gate)

        dim2 = fk.Dimension("FL2-H", compensation_ref="FCS")
        dim3 = fk.Dimension("FL3-H", compensation_ref="FCS")
        poly_dims = [dim2, dim3]

        vertices = [
            fk.Vertex([5, 5]),
            fk.Vertex([500, 5]),
            fk.Vertex([500, 500])
        ]

        poly_gate = fk.gates.PolygonGate("Polygon1", None, poly_dims, vertices, gs)
        gs.add_gate(poly_gate)

        dim4 = fk.Dimension("FL3-H", compensation_ref="uncompensated")
        dim5 = fk.Dimension("FL4-H", compensation_ref="uncompensated")
        ellipse_dims = [dim4, dim5]

        coords = [12.99701, 16.22941]
        cov_mat = [[62.5, 37.5], [37.5, 62.5]]
        dist_square = 1

        ellipse_gate = fk.gates.EllipsoidGate("Ellipse1", None, ellipse_dims, coords, cov_mat, dist_square, gs)
        gs.add_gate(ellipse_gate)

        gate_refs = [
            {
                'ref': 'Range1',
                'complement': False
            },
            {
                'ref': 'Ellipse1',
                'complement': True
            },
            {
                'ref': 'Polygon1',
                'complement': False
            }
        ]

        bool_gate = fk.gates.BooleanGate("And3", None, "and", gate_refs, gs)
        gs.add_gate(bool_gate)

        res_path = 'examples/gate_ref/truth/Results_And3.txt'
        truth = pd.read_csv(res_path, header=None, squeeze=True, dtype='bool').values

        result = gs.gate_sample(data1_sample, 'And3')

        np.testing.assert_array_equal(truth, result.get_gate_indices('And3'))

    @staticmethod
    def test_add_boolean_not1_gate():
        gs = fk.GatingStrategy()

        dim1 = fk.Dimension("FL3-H", compensation_ref="uncompensated")
        dim2 = fk.Dimension("FL4-H", compensation_ref="uncompensated")
        ellipse_dims = [dim1, dim2]

        coords = [12.99701, 16.22941]
        cov_mat = [[62.5, 37.5], [37.5, 62.5]]
        dist_square = 1

        ellipse_gate = fk.gates.EllipsoidGate("Ellipse1", None, ellipse_dims, coords, cov_mat, dist_square, gs)
        gs.add_gate(ellipse_gate)

        gate_refs = [
            {
                'ref': 'Ellipse1',
                'complement': False
            }
        ]

        bool_gate = fk.gates.BooleanGate("Not1", None, "not", gate_refs, gs)
        gs.add_gate(bool_gate)

        res_path = 'examples/gate_ref/truth/Results_Not1.txt'
        truth = pd.read_csv(res_path, header=None, squeeze=True, dtype='bool').values

        result = gs.gate_sample(data1_sample, 'Not1')

        np.testing.assert_array_equal(truth, result.get_gate_indices('Not1'))

    @staticmethod
    def test_add_boolean_and4_not_gate():
        gs = fk.GatingStrategy()

        dim1 = fk.Dimension("FSC-H", compensation_ref="uncompensated", range_min=100)
        rect_dims = [dim1]

        rect_gate = fk.gates.RectangleGate("Range1", None, rect_dims, gs)
        gs.add_gate(rect_gate)

        dim2 = fk.Dimension("FL2-H", compensation_ref="FCS")
        dim3 = fk.Dimension("FL3-H", compensation_ref="FCS")
        poly_dims = [dim2, dim3]

        vertices = [
            fk.Vertex([5, 5]),
            fk.Vertex([500, 5]),
            fk.Vertex([500, 500])
        ]

        poly_gate = fk.gates.PolygonGate("Polygon1", None, poly_dims, vertices, gs)
        gs.add_gate(poly_gate)

        dim4 = fk.Dimension("FL3-H", compensation_ref="uncompensated")
        dim5 = fk.Dimension("FL4-H", compensation_ref="uncompensated")
        ellipse_dims = [dim4, dim5]

        coords = [12.99701, 16.22941]
        cov_mat = [[62.5, 37.5], [37.5, 62.5]]
        dist_square = 1

        ellipse_gate = fk.gates.EllipsoidGate("Ellipse1", None, ellipse_dims, coords, cov_mat, dist_square, gs)
        gs.add_gate(ellipse_gate)

        gate1_refs = [
            {
                'ref': 'Ellipse1',
                'complement': False
            }
        ]

        bool1_gate = fk.gates.BooleanGate("Not1", None, "not", gate1_refs, gs)
        gs.add_gate(bool1_gate)

        gate2_refs = [
            {
                'ref': 'Range1',
                'complement': False
            },
            {
                'ref': 'Not1',
                'complement': False
            },
            {
                'ref': 'Polygon1',
                'complement': False
            }
        ]

        bool2_gate = fk.gates.BooleanGate("And4", None, "and", gate2_refs, gs)
        gs.add_gate(bool2_gate)

        res_path = 'examples/gate_ref/truth/Results_And4.txt'
        truth = pd.read_csv(res_path, header=None, squeeze=True, dtype='bool').values

        result = gs.gate_sample(data1_sample, 'And4')

        np.testing.assert_array_equal(truth, result.get_gate_indices('And4'))

    @staticmethod
    def test_add_boolean_or2_complement_gate():
        gs = fk.GatingStrategy()

        dim1 = fk.Dimension("SSC-H", compensation_ref="FCS", range_min=20, range_max=80)
        dim2 = fk.Dimension("FL1-H", compensation_ref="FCS", range_min=70, range_max=200)
        rect_dims = [dim1, dim2]

        rect_gate = fk.gates.RectangleGate("Rectangle2", None, rect_dims, gs)
        gs.add_gate(rect_gate)

        div1 = fk.QuadrantDivider("FL2", "FL2-H", "FCS", [12.14748])
        div2 = fk.QuadrantDivider("FL4", "FL4-H", "FCS", [14.22417])

        divs = [div1, div2]

        quad_gate = fk.gates.QuadrantGate("Quadrant1", None, divs, quadrants_q1, gs)
        gs.add_gate(quad_gate)

        gate1_refs = [
            {
                'ref': 'Rectangle2',
                'complement': False
            },
            {
                'ref': 'FL2N-FL4N',
                'complement': True
            }
        ]

        bool1_gate = fk.gates.BooleanGate("Or2", None, "or", gate1_refs, gs)
        gs.add_gate(bool1_gate)

        res_path = 'examples/gate_ref/truth/Results_Or2.txt'
        truth = pd.read_csv(res_path, header=None, squeeze=True, dtype='bool').values

        result = gs.gate_sample(data1_sample, 'Or2')

        np.testing.assert_array_equal(truth, result.get_gate_indices('Or2'))

    @staticmethod
    def test_add_matrix_poly4_gate():
        gs = fk.GatingStrategy()

        fluoros = ['FITC', 'PE', 'PerCP']
        detectors = ['FL1-H', 'FL2-H', 'FL3-H']

        spill_data = np.array(
            [
                [1, 0.02, 0.06],
                [0.11, 1, 0.07],
                [0.09, 0.01, 1]
            ]
        )

        comp_matrix = fk.Matrix('MySpill', fluoros, detectors, spill_data)
        gs.add_comp_matrix(comp_matrix)

        dim1 = fk.Dimension("PE", compensation_ref="MySpill")
        dim2 = fk.Dimension("PerCP", compensation_ref="MySpill")
        dims = [dim1, dim2]

        vertices = [
            fk.Vertex([5, 5]),
            fk.Vertex([500, 5]),
            fk.Vertex([500, 500])
        ]

        poly_gate = fk.gates.PolygonGate("Polygon4", None, dims, vertices, gs)
        gs.add_gate(poly_gate)

        res_path = 'examples/gate_ref/truth/Results_Polygon4.txt'
        truth = pd.read_csv(res_path, header=None, squeeze=True, dtype='bool').values

        result = gs.gate_sample(data1_sample, 'Polygon4')

        np.testing.assert_array_equal(truth, result.get_gate_indices('Polygon4'))

    @staticmethod
    def test_add_matrix_rect3_gate():
        gs = fk.GatingStrategy()

        fluoros = ['FITC', 'PE', 'PerCP']
        detectors = ['FL1-H', 'FL2-H', 'FL3-H']

        spill_data = np.array(
            [
                [1, 0.02, 0.06],
                [0.11, 1, 0.07],
                [0.09, 0.01, 1]
            ]
        )

        comp_matrix = fk.Matrix('MySpill', fluoros, detectors, spill_data)
        gs.add_comp_matrix(comp_matrix)

        dim1 = fk.Dimension("FITC", compensation_ref="MySpill", range_min=5, range_max=70)
        dim2 = fk.Dimension("PE", compensation_ref="MySpill", range_min=9, range_max=208)
        dims = [dim1, dim2]

        rect_gate = fk.gates.RectangleGate("Rectangle3", None, dims, gs)
        gs.add_gate(rect_gate)

        res_path = 'examples/gate_ref/truth/Results_Rectangle3.txt'
        truth = pd.read_csv(res_path, header=None, squeeze=True, dtype='bool').values

        result = gs.gate_sample(data1_sample, 'Rectangle3')

        np.testing.assert_array_equal(truth, result.get_gate_indices('Rectangle3'))

    @staticmethod
    def test_add_matrix_rect4_gate():
        gs = fk.GatingStrategy()

        fluoros = ['FITC', 'PE', 'PerCP']
        detectors = ['FL1-H', 'FL2-H', 'FL3-H']

        spill_data = np.array(
            [
                [1, 0.02, 0.06],
                [0.11, 1, 0.07],
                [0.09, 0.01, 1]
            ]
        )

        comp_matrix = fk.Matrix('MySpill', fluoros, detectors, spill_data)
        gs.add_comp_matrix(comp_matrix)

        dim1 = fk.Dimension("PerCP", compensation_ref="MySpill", range_min=7, range_max=90)
        dim2 = fk.Dimension("FSC-H", compensation_ref="uncompensated", range_min=10, range_max=133)
        dims = [dim1, dim2]

        rect_gate = fk.gates.RectangleGate("Rectangle4", None, dims, gs)
        gs.add_gate(rect_gate)

        res_path = 'examples/gate_ref/truth/Results_Rectangle4.txt'
        truth = pd.read_csv(res_path, header=None, squeeze=True, dtype='bool').values

        result = gs.gate_sample(data1_sample, 'Rectangle4')

        np.testing.assert_array_equal(truth, result.get_gate_indices('Rectangle4'))

    @staticmethod
    def test_add_matrix_rect5_gate():
        gs = fk.GatingStrategy()

        fluoros = ['FITC', 'PE', 'PerCP']
        detectors = ['FL1-H', 'FL2-H', 'FL3-H']

        spill_data = np.array(
            [
                [1, 0.02, 0.06],
                [0.11, 1, 0.07],
                [0.09, 0.01, 1]
            ]
        )

        comp_matrix = fk.Matrix('MySpill', fluoros, detectors, spill_data)
        gs.add_comp_matrix(comp_matrix)

        dim1 = fk.Dimension("PerCP", compensation_ref="MySpill", range_min=7, range_max=90)
        dim2 = fk.Dimension("FSC-H", compensation_ref="uncompensated", range_min=10)
        dims = [dim1, dim2]

        rect_gate = fk.gates.RectangleGate("Rectangle5", None, dims, gs)
        gs.add_gate(rect_gate)

        res_path = 'examples/gate_ref/truth/Results_Rectangle5.txt'
        truth = pd.read_csv(res_path, header=None, squeeze=True, dtype='bool').values

        result = gs.gate_sample(data1_sample, 'Rectangle5')

        np.testing.assert_array_equal(truth, result.get_gate_indices('Rectangle5'))

    @staticmethod
    def test_add_transform_asinh_range1_gate():
        gs = fk.GatingStrategy()

        asinh_xform = fk.transforms.AsinhTransform(
            "AsinH_10000_4_1",
            param_t=10000,
            param_m=4,
            param_a=1
        )
        gs.add_transform(asinh_xform)

        dim1 = fk.Dimension('FL1-H', 'uncompensated', 'AsinH_10000_4_1', range_min=0.37, range_max=0.63)
        dims = [dim1]

        rect_gate = fk.gates.RectangleGate("ScaleRange1", None, dims, gs)
        gs.add_gate(rect_gate)

        res_path = 'examples/gate_ref/truth/Results_ScaleRange1.txt'
        truth = pd.read_csv(res_path, header=None, squeeze=True, dtype='bool').values

        result = gs.gate_sample(data1_sample, 'ScaleRange1')

        np.testing.assert_array_equal(truth, result.get_gate_indices('ScaleRange1'))

    @staticmethod
    def test_add_transform_hyperlog_range2_gate():
        gs = fk.GatingStrategy()

        xform = fk.transforms.HyperlogTransform(
            "Hyperlog_10000_1_4.5_0",
            param_t=10000,
            param_w=1,
            param_m=4.5,
            param_a=0
        )
        gs.add_transform(xform)

        dim1 = fk.Dimension('FL1-H', 'uncompensated', 'Hyperlog_10000_1_4.5_0', range_min=0.37, range_max=0.63)
        dims = [dim1]

        rect_gate = fk.gates.RectangleGate("ScaleRange2", None, dims, gs)
        gs.add_gate(rect_gate)

        res_path = 'examples/gate_ref/truth/Results_ScaleRange2.txt'
        truth = pd.read_csv(res_path, header=None, squeeze=True, dtype='bool').values

        result = gs.gate_sample(data1_sample, 'ScaleRange2')

        np.testing.assert_array_equal(truth, result.get_gate_indices('ScaleRange2'))

    @staticmethod
    def test_add_transform_linear_range3_gate():
        gs = fk.GatingStrategy()

        xform = fk.transforms.LinearTransform(
            "Linear_10000_500",
            param_t=10000,
            param_a=500
        )
        gs.add_transform(xform)

        dim1 = fk.Dimension('FL1-H', 'uncompensated', 'Linear_10000_500', range_min=0.049, range_max=0.055)
        dims = [dim1]

        rect_gate = fk.gates.RectangleGate("ScaleRange3", None, dims, gs)
        gs.add_gate(rect_gate)

        res_path = 'examples/gate_ref/truth/Results_ScaleRange3.txt'
        truth = pd.read_csv(res_path, header=None, squeeze=True, dtype='bool').values

        result = gs.gate_sample(data1_sample, 'ScaleRange3')

        np.testing.assert_array_equal(truth, result.get_gate_indices('ScaleRange3'))

    @staticmethod
    def test_add_transform_logicle_range4_gate():
        gs = fk.GatingStrategy()

        xform = fk.transforms.LogicleTransform(
            "Logicle_10000_1_4.5_0",
            param_t=10000,
            param_w=0.5,
            param_m=4.5,
            param_a=0
        )
        gs.add_transform(xform)

        dim1 = fk.Dimension('FL1-H', 'uncompensated', 'Logicle_10000_1_4.5_0', range_min=0.37, range_max=0.63)
        dims = [dim1]

        rect_gate = fk.gates.RectangleGate("ScaleRange4", None, dims, gs)
        gs.add_gate(rect_gate)

        res_path = 'examples/gate_ref/truth/Results_ScaleRange4.txt'
        truth = pd.read_csv(res_path, header=None, squeeze=True, dtype='bool').values

        result = gs.gate_sample(data1_sample, 'ScaleRange4')

        np.testing.assert_array_equal(truth, result.get_gate_indices('ScaleRange4'))

    @staticmethod
    def test_add_transform_logicle_range5_gate():
        gs = fk.GatingStrategy()

        xform = fk.transforms.LogicleTransform(
            "Logicle_10000_1_4_0.5",
            param_t=10000,
            param_w=1,
            param_m=4,
            param_a=0.5
        )
        gs.add_transform(xform)

        dim1 = fk.Dimension('FL1-H', 'uncompensated', 'Logicle_10000_1_4_0.5', range_min=0.37, range_max=0.63)
        dims = [dim1]

        rect_gate = fk.gates.RectangleGate("ScaleRange5", None, dims, gs)
        gs.add_gate(rect_gate)

        res_path = 'examples/gate_ref/truth/Results_ScaleRange5.txt'
        truth = pd.read_csv(res_path, header=None, squeeze=True, dtype='bool').values

        result = gs.gate_sample(data1_sample, 'ScaleRange5')

        np.testing.assert_array_equal(truth, result.get_gate_indices('ScaleRange5'))

    @staticmethod
    def test_add_transform_log_range6_gate():
        gs = fk.GatingStrategy()

        xform = fk.transforms.LogTransform(
            "Logarithmic_10000_5",
            param_t=10000,
            param_m=5
        )
        gs.add_transform(xform)

        dim1 = fk.Dimension('FL1-H', 'uncompensated', 'Logarithmic_10000_5', range_min=0.37, range_max=0.63)
        dims = [dim1]

        rect_gate = fk.gates.RectangleGate("ScaleRange6", None, dims, gs)
        gs.add_gate(rect_gate)

        res_path = 'examples/gate_ref/truth/Results_ScaleRange6.txt'
        truth = pd.read_csv(res_path, header=None, squeeze=True, dtype='bool').values

        result = gs.gate_sample(data1_sample, 'ScaleRange6')

        np.testing.assert_array_equal(truth, result.get_gate_indices('ScaleRange6'))