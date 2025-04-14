"""
Unit tests for the Concert Itinerary Builder.

This file contains unit tests for the ItineraryBuilder class in main.py.
Participants will implement tests based on the system specifications.
"""

import unittest
from main import Concert, ItineraryBuilder
from concerts_data import get_all_concerts


class ItineraryBuilderTest(unittest.TestCase):
    """Test cases for the ItineraryBuilder class."""

    def setUp(self):
        """Set up for the tests."""
        self.builder = ItineraryBuilder()

        self.all_concerts = get_all_concerts()

    # ----- Manual Test Cases -----
    # Participants will implement their manual test cases here.

    def test_manual_1(self):
        """Some artists may have no concerts on the list. In that case, that should be indicated in the itinerary."""

        concerts = [Concert("Coldplay", "2025-06-05", "Stockholm", 59.3293, 18.0686),
                    Concert("Adele", "2025-06-15", "Oslo", 59.9139, 10.7522),
                    Concert("Beyoncé", "2025-06-20", "Copenhagen", 55.6761, 12.5683)]

        itinerary = self.builder.build_itinerary(concerts)

        artist_lst = [concert.artist for concert in itinerary]
        tot_artist_lst = [concert.artist for concert in self.all_concerts]
        unique_tot_artist_lst = list(dict.fromkeys(tot_artist_lst))
        actually_not_booked = []
        for artist in unique_tot_artist_lst:
            if artist not in artist_lst:
                actually_not_booked.append(artist)

        self.assertEqual(len(self.builder.get_non_booked_artists(self.all_concerts)),
                         len(actually_not_booked))

        self.assertEqual(self.builder.get_non_booked_artists(self.all_concerts),
                         actually_not_booked)

    def test_manual_2(self):
        """The itinerary should return a list of concerts sorted in chronological order (by date from earliest to latest)."""
        itinerary = self.builder.build_itinerary(self.all_concerts)

        date_lst = [concert.date for concert in itinerary]

        self.assertEqual(date_lst, sorted(date_lst))

    def test_manual_3(self):
        """An artist has at most one concert in the itinerary. If an artist has more than one concert in the list, the itinerary should only include the one with the earliest start date."""

        concert_1 = Concert("Taylor Swift", "2025-06-10",
                            "Stockholm", 59.3293, 18.0686)

        concert_2 = Concert("Taylor Swift", "2025-06-11",
                            "Stockholm", 59.3293, 18.0686)

        concert_3 = Concert("Taylor Swift", "2025-05-11",
                            "Stockholm", 59.3293, 18.0686)

        concert_4 = Concert("Taylor Swift", "2025-06-12",
                            "Stockholm", 59.3293, 18.0686)

        itinerary_1 = self.builder.build_itinerary(
            [concert_1, concert_2, concert_3, concert_4])

        self.assertEqual(len(itinerary_1), 1)

        self.assertEqual(itinerary_1, [concert_3])

        itinerary_2 = self.builder.build_itinerary(
            [concert_3, concert_1, concert_4, concert_1])

        self.assertEqual(itinerary_2, [concert_3])

    # ----- AI-Assisted Test Cases -----
    # Participants will implement their AI-assisted test cases here.
    # Please name your test in a way which indicates that these are AI-assisted test cases.
        # ----- AI-Assisted Test Cases -----

    def test_ai_assisted_same_day_conflict(self):
        """If two concerts occur on the same day, the one closer to the last added concert should be included."""

        # Two concerts on same date
        concert_1 = Concert("Artist A", "2025-06-10", "Berlin", 52.52, 13.405)
        concert_2 = Concert("Artist B", "2025-06-10",
                            "Munich", 48.1351, 11.582)

        # A previous concert to determine proximity
        concert_prev = Concert("Artist C", "2025-06-09",
                               "Leipzig", 51.3397, 12.3731)

        # Concert A is closer to Leipzig than Concert B
        concerts = [concert_prev, concert_1, concert_2]

        itinerary = self.builder.build_itinerary(concerts)

        self.assertIn(concert_prev, itinerary)
        self.assertIn(concert_1, itinerary)
        self.assertNotIn(concert_2, itinerary)
        self.assertEqual(len(itinerary), 2)

    def test_ai_assisted_itinerary_contents(self):
        """Itinerary should contain concerts with artist, date, and location populated."""

        concerts = [
            Concert("Artist X", "2025-07-01", "Amsterdam", 52.3676, 4.9041),
            Concert("Artist Y", "2025-07-05", "Vienna", 48.2082, 16.3738)
        ]

        itinerary = self.builder.build_itinerary(concerts)

        for concert in itinerary:
            self.assertIsInstance(concert.artist, str)
            self.assertRegex(concert.date, r"\d{4}-\d{2}-\d{2}")
            self.assertIsInstance(concert.location, str)

    def test_ai_assisted_prioritize_single_concert_artists(self):
        """Artists with only one concert should be prioritized over artists with multiple concerts."""

        single_concert_artist = Concert(
            "OneTimeArtist", "2025-06-15", "Oslo", 59.9139, 10.7522)

        multi_concerts = [
            Concert("MultiArtist", "2025-06-10", "Paris", 48.8566, 2.3522),
            Concert("MultiArtist", "2025-06-12", "Lyon", 45.764, 4.8357)
        ]

        concerts = [single_concert_artist] + multi_concerts

        itinerary = self.builder.build_itinerary(concerts)

        artist_names = [c.artist for c in itinerary]

        self.assertIn("OneTimeArtist", artist_names)
        self.assertIn("MultiArtist", artist_names)
        self.assertEqual(artist_names.count("OneTimeArtist"), 1)
        self.assertEqual(artist_names.count("MultiArtist"), 1)

        self.assertIn("OneTimeArtist", artist_names)


if __name__ == "__main__":
    unittest.main()
