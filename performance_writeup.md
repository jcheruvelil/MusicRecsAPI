# Performance Testing Results

## Fake Data Modeling

Users: 305 rows
Search History: 138,791 rows
Rec History: 173,341 rows
Ratings: 2,707 rows
Playlists: 5,904 rows
Playlist Tracks: 711,025 rows

Our populate_fake_data.py script can be found in the src directory of the project. 
We modeled our script to add a number of users per run based on a parameter to the 
populate_fake_data function. 

Output of an example run of the program is shown below:
*Parameters: num_users=100*

Here are the distributions of targeted endpoints per user:
max num_playlists: 39
min num_playlists: 5
avg num_playlists: 20.68

max num rating: 337
min num rating: 0
avg num rating: 14.68

max num search: 6946
min num search: 2
avg num search: 791.03

max num rec: 4932
min num rec: 1
avg num rec: 871.93

Here are the results of rows added to the database due to requests to the endpoints:
Users: 305 rows
Search History: 84,190 rows
Rec History: 91,233 rows
Ratings: 1,876 rows
Playlists: 2,293 rows
Playlist Tracks: 269,456 rows


These distributions are roughly estimated assuming that users will be using search and rec 
estimates multiple times a day. As the application scales through months and beyond a year, 
we will reach a million rows with around 200-300 active users.

user_id=416
## Performance results of hitting endpoints

### 1. User

#### 1.1 Create User `/user` (POST)

**Request #1 Timing: 192 ms**:

#### 1.2 Login `/user/login/` (GET)

**Request #1 Timing: 78.2 ms**:
**Average: **:

#### 1.3 Get user library `/user/{user_id}/library` (GET)

**For User with most playlists: 35.2 ms**:
**For User with no playlists: 30.3 ms**:
**Average: 32.75 ms**:

### 2. Searching

#### 2.1. Search Music System Library - `/search` (GET)

**Timing of Request with no parameters (must return every track): 358 ms**:
**Timing of Request with artist parameter: 155 ms**:
**Timing of Request with song parameter: 225 ms**:
**Timing of Request with album parameter: 248 ms**:
**Average: 246.5 ms**:

### 3. Playlists 

#### 3.1 Create playlist - `/playlist/{user_id}/` (POST)

**Request Timing: 51.8 ms**:

#### 3.2 Add track to playlist - `/playlist/{playlist_id}/add/{track_id}` (POST)

**Request Timing: 179 ms**:

#### 3.3 Remove track from playlist - `/playlist/{playlist_id}/remove/{track_id}` (DELETE)

**Request Timing: 222 ms**:

#### 3.4 Get Playlist - `/playlist/{playlist_id}` (GET)

**For Playlist with most songs (1458): 260 ms**:
**For Playlist with no songs: 166 ms**:
**Average: 213 ms**:

### 4. Recommendations

#### 4.1 Get Song Recommendation from Another Song - `/recs/track/{track_id}` - (GET)

**Request Timing: 399 ms ms**:


#### 4.2 Get Song Recommendations from User Ratings - `/recs/ratings/{user_id}` - (GET)

**Request Timing: 103 ms**:

#### 4.3 Get Song Recommendations from Playlist - `/recs/{playlist_id}` - (GET)

**Request Timing: 383 ms**:

### 5. Ratings

#### 5.1 Update Rating - `/rating/{user_id}/{track_id}` (POST)

**TODO**
**Request Timing for creating new rating:  ms**:
**Request Timing for updating existing rating:  ms**:
**Average: **:

### 6. History

#### 6.1 Get Search History - `/history/search` (GET)

**Request Timing for user with most search history (6948): 410 ms**:
**Request Timing for user with no search history: 146 ms**:
**Average: 278 ms**:

#### 6.2 Get Recommendation History - `/history/recommendation` (GET)

**Request Timing for user with most search history (5930): 160 ms**:
**Request Timing for user with no search history: 117 ms**:
**Average: 138.5 ms**:

#### 6.3 Clear Search History - `/history/search/clear` (DELETE)

**TODO**

### 6.4 Clear Recommendation History - `/history/recommendation/clear` (DELETE)

**TODO**

## Performance tuning

### 1. Search 

Search is slow and can be improved by indexing. However, we need to use a 
FULLTEXT index, becuase we are using the LIKE operator when looking at track name,
album name, and artist name. In Postgres, we can achieve this by using tsvectors.

Let's look at the query plan first:

```sql
EXPLAIN ANALYZE SELECT * FROM tracks 
WHERE track_name LIKE '%bennie%'
```

| QUERY PLAN                                                                                              |
| ------------------------------------------------------------------------------------------------------- |
| Seq Scan on tracks  (cost=0.00..5212.21 rows=9 width=249) (actual time=284.506..284.507 rows=0 loops=1) |
|   Filter: (track_name ~~ '%bennie%'::text)                                                              |
|   Rows Removed by Filter: 89377                                                                         |
| Planning Time: 2.820 ms                                                                                 |
| Execution Time: 284.796 ms                                                                              |

We want to eliminate the Sequential scan by using an index. First, we need to create 
a tsvector column which combines track name, album name, and artist name, since we 
want to allow searches with any number of these parameters. To do this, we will 
execute the following SQL:
```sql
ALTER TABLE tracks
    ADD COLUMN textsearchable_index_col tsvector
        GENERATED ALWAYS AS (to_tsvector('english', coalesce(track_name, '') || ' ' || coalesce(artists, '') || ' ' || coalesce(album_name, ''))) STORED;
```

Now, we can create an index on the tsvector column:
```sql
CREATE INDEX tracks_textsearch_idx ON tracks USING GIN (textsearchable_index_col);
DROP INDEX tracks_textsearch_idx;
```

Our searches will now have much better performance. We just have to use the tsvector
column for searches. Let's analyze the query planner once more:

```sql
EXPLAIN ANALYZE
SELECT *
FROM tracks
WHERE textsearchable_index_col @@ to_tsquery('eilish')
LIMIT 10;
```

| QUERY PLAN                                                                                                                             |
| -------------------------------------------------------------------------------------------------------------------------------------- |
| Limit  (cost=19.71..51.12 rows=10 width=249) (actual time=0.969..1.069 rows=10 loops=1)                                                |
|   ->  Bitmap Heap Scan on tracks  (cost=19.71..1423.75 rows=447 width=249) (actual time=0.968..1.067 rows=10 loops=1)                  |
|         Recheck Cond: (textsearchable_index_col @@ to_tsquery('eilish'::text))                                                         |
|         Heap Blocks: exact=2                                                                                                           |
|         ->  Bitmap Index Scan on tracks_textsearch_idx  (cost=0.00..19.60 rows=447 width=0) (actual time=0.874..0.874 rows=56 loops=1) |
|               Index Cond: (textsearchable_index_col @@ to_tsquery('eilish'::text))                                                     |
| Planning Time: 12.248 ms                                                                                                               |
| Execution Time: 1.191 ms                                                                                                               |

Success! Our planning time has increased slightly, but we've improved our execution performance 250x.

### 2. Create User
The create user (/user) endpoint is unecessarily slow. Partly, this is due to 
the check to ensure that there are no existing users with the username that was 
passed in. We have unique usernames in our system. Let's speed up this endpoint.

First, let's take a look at the query planner. 

| QUERY PLAN                                                                                     |
| ---------------------------------------------------------------------------------------------- |
| Seq Scan on users  (cost=0.00..7.71 rows=1 width=26) (actual time=1.480..1.480 rows=0 loops=1) |
|   Filter: (username = 'bobby'::text)                                                           |
|   Rows Removed by Filter: 419                                                                  |
| Planning Time: 2.459 ms                                                                        |
| Execution Time: 1.609 ms                                                                       |


As we can see, we are doing a sequential scan, which is causing the slow performance.

Let's add an index on username with:
```sql
CREATE INDEX username_idx ON users (username);
```

Now, let's double check the query plan.

| QUERY PLAN                                                                                     |
| ---------------------------------------------------------------------------------------------- |
| Seq Scan on users  (cost=0.00..8.24 rows=1 width=26) (actual time=0.139..0.143 rows=1 loops=1) |
|   Filter: (username = 'debug'::text)                                                           |
|   Rows Removed by Filter: 418                                                                  |
| Planning Time: 1.004 ms                                                                        |
| Execution Time: 0.206 ms                                                                       |

Wait! What's going on? Why is it still doing a sequence sqan? Did the index not work?
No, the index worked. What's happening is that our users table has very little data in
it compared to the other tables. There are only a few hundred users. The entire user 
table fits inside one page (8kB) therefore causing the sequential scan despite the 
available index. However, as our system scales, this index can be helpful in speeding up
the endpoints. This index may slow down our insertions, so we may want to hold off on 
its creation until our userbase grows. 

Eventually, with more growth, the username index will also speed up our login endpoint, 
where we also search users by username.


