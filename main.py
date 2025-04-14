"""
Concert Itinerary Builder

This module provides functionality to build an itinerary of upcoming concerts.
"""

import math


class Concert:
    """
    Represents a concert event.

    Attributes:
        artist (str): The name of the artist performing.
        date (str): The date of the concert in 'YYYY-MM-DD' format.
        location (str): The location where the concert will take place.
        latitude (float): Latitude coordinate of the concert location.
        longitude (float): Longitude coordinate of the concert location.
    """

    def __init__(self, artist, date, location, latitude, longitude):
        self.artist = artist
        self.date = date
        self.location = location
        self.latitude = latitude
        self.longitude = longitude


class ItineraryBuilder:
    """
    A class to build concert itineraries. 
    """

    def __init__(self):
        self.concerts = []

    def _calculate_distance(self, lat1, lon1, lat2, lon2):
        """Calculate the Haversine distance between two lat/lon points."""
        R = 6371  # Radius of the Earth in km
        dlat = math.radians(lat2 - lat1)
        dlon = math.radians(lon2 - lon1)
        a = (math.sin(dlat / 2) ** 2 +
             math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) *
             math.sin(dlon / 2) ** 2)
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        return R * c

    def build_itinerary(self, concerts):
        artist_earliest = {}
        artist_counts = {}

        # Step 1: Get the earliest concert per artist
        for con in concerts:
            artist_counts[con.artist] = artist_counts.get(con.artist, 0) + 1
            if con.artist not in artist_earliest:
                artist_earliest[con.artist] = con
            elif con.date < artist_earliest[con.artist].date:
                artist_earliest[con.artist] = con

        # Step 2: Prepare lists
        single_concerts = [con for artist, con in artist_earliest.items()
                           if artist_counts[artist] == 1]
        multi_concerts = [con for artist, con in artist_earliest.items()
                          if artist_counts[artist] > 1]

        # Sort both lists by date individually
        single_concerts.sort(key=lambda c: c.date)
        multi_concerts.sort(key=lambda c: c.date)

        # Combine: single-concert artists come first regardless of date
        all_candidates = single_concerts + multi_concerts

        selected = []
        used_dates = set()

        for i, con in enumerate(all_candidates):
            if con.date not in used_dates:
                selected.append(con)
                used_dates.add(con.date)
            else:
                # Conflict: find existing concert on that day
                existing = [c for c in selected if c.date == con.date][0]
                idx = selected.index(existing)
                prev = selected[idx - 1] if idx > 0 else existing

                dist_existing = self._calculate_distance(
                    prev.latitude, prev.longitude,
                    existing.latitude, existing.longitude)

                dist_new = self._calculate_distance(
                    prev.latitude, prev.longitude,
                    con.latitude, con.longitude)

                if dist_new < dist_existing:
                    selected[idx] = con

        # Don't sort again — preserve the priority order
        self.concerts = sorted(
            selected,
            key=lambda x: (x.date, artist_counts.get(x.artist, float("inf")))
        )
        return self.concerts

    def get_non_booked_artists(self, all_concerts):
        artist_lst = [concert.artist for concert in self.concerts]
        tot_artist_lst = [concert.artist for concert in all_concerts]
        unique_tot_artist_lst = list(dict.fromkeys(tot_artist_lst))

        non_booked = []

        for artist in unique_tot_artist_lst:
            if artist not in artist_lst:
                non_booked.append(artist)

        return non_booked


if __name__ == "__main__":
    from concerts_data import get_all_concerts

    all_concerts = get_all_concerts()
