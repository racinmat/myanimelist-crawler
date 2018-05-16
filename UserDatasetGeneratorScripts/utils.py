from collections import namedtuple

# using named tuple instead of dict lowers size on disk and memory usage, but takes 2 times more to load.
# Still worth it, though.
# comparison for 34 881 123 records of anime list entries
# dicts:
# time to load:  64.91 seconds
# Current memory usage: 22.41 GB
# time to save:  230.74 seconds
# size on disk: 4.9 GB
# named tuples:
# time to load:  125.22 seconds
# Current memory usage: 18.69 GB
# time to save:  274.04 seconds
# size on disk: 3.6 GB

# compared named tuple to dicts:
# time to load:  192% of time
# Current memory usage: 83% of memory
# time to save:  118% of time
# size on disk: 73% of file size

# loading is during stats printing, but not during scraping, so it is still worth

anime_record_keys = [
    'series_animedb_id',
    'my_watched_episodes',
    'my_start_date',
    'my_finish_date',
    'my_score',
    'my_status',
    'my_rewatching',
    'my_rewatching_ep',
    'my_last_updated',
    'my_tags',
]
AnimeRecord = namedtuple('AnimeRecord', anime_record_keys)
