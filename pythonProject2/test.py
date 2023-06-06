import unittest
from io import StringIO
from unittest.mock import patch

from main import create_graph, display_adjacency_list


class TestGraph(unittest.TestCase):
    def test_create_graph(self):
        input_data = "10 15\nA B 5\nA C 3\nB D 2\nB E 7\nC F 4\nC G 6\nD H 1\nD I 9\nE J 8\nF J 5\nG J 6\nH J 4\nI J 3\nA J 7\nB J 2"
        expected_graph = [
            [(1, 5), (2, 3), (9, 7)],
            [(3, 2), (4, 7), (9, 2)],
            [(5, 4), (6, 6)],
            [(7, 1), (8, 9)],
            [(9, 8)],
            [(9, 5)],
            [(9, 6)],
            [(9, 4)],
            [(9, 3)],
            []
        ]

        with patch('builtins.open', return_value=StringIO(input_data)):
            result = create_graph("location.txt")

        self.assertEqual(result, expected_graph)

    def test_display_adjacency_list(self):
        graph = [
            [(1, 5), (2, 3), (9, 7)],
            [(3, 2), (4, 7), (9, 2)],
            [(5, 4), (6, 6)],
            [(7, 1), (8, 9)],
            [(9, 8)],
            [(9, 5)],
            [(9, 6)],
            [(9, 4)],
            [(9, 3)],
            []
        ]
        expected_output = "Vertex A: B(5) C(3) J(7) \nVertex B: D(2) E(7) J(2) \nVertex C: F(4) G(6) \nVertex D: H(1) " \
                          "I(9) \nVertex E: J(8) \nVertex F: J(5) \nVertex G: J(6) \nVertex H: J(4) \nVertex I: J(3) " \
                          "\nVertex J: \n"

        with patch('sys.stdout', new=StringIO()) as fake_out:
            display_adjacency_list(graph)
            self.assertEqual(fake_out.getvalue(), expected_output)


if __name__ == '__main__':
    unittest.main()
