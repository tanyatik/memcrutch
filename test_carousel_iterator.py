import unittest
from carousel_iterator import CarouselIterator


class TestCarouselIterator(unittest.TestCase):
    def test_carousel_preivous_next(self):
        carousel = CarouselIterator(iter([1, 2, 3]))
        self.assertEqual(carousel.current(), 1)

        self.assertEqual(carousel.next(), 2)
        self.assertEqual(carousel.previous(), 1)
        self.assertEqual(carousel.next(), 2)
        self.assertEqual(carousel.next(), 3)
        with self.assertRaises(StopIteration):
            carousel.next()
        self.assertEqual(carousel.current(), 3)

        self.assertEqual(carousel.previous(), 2)
        self.assertEqual(carousel.previous(), 1)
        with self.assertRaises(StopIteration):
            carousel.previous()

        self.assertEqual(carousel.current(), 1)
        self.assertEqual(carousel.next(), 2)
        self.assertEqual(carousel.current(), 2)


if __name__ == "__main__":
    unittest.main()