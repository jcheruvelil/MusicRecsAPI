# Concurrency

## Outline

Since our project involves many tables and transactions which all interact with one another, we try to implement concurrency control mechanisms which are outlined and will have sequence diagrams.

## Concurrency Control Mechanisms

We use:

1. **Locking** locks are used to prevent multiple transactions from modifying a single row at once.
2. **Time Stamp Protocol** utilized to ensure stability in our transactions, using time stamps to determine a transactions order compared to another
3. **Atomicity** by ensuring that each transaction is atomic, it allows for every operation in a transaction either occuring and working correctly, or completely none to prevent half updates.

## Potential Phenomena without Concurrency Control

Without proper concurrency control, the following phenomena could occur:

### 1. **Dirty Read**

- **Phenomenon**: A transaction reads uncommitted changes made by another transaction.
- **Scenario**: User A updates a track's popularity, and User B reads the updated popularity before User A's transaction is committed.

### 2. **Non-repeatable Read**

- **Phenomenon**: A transaction reads the same row twice and gets different values because another transaction modified and committed the row in between the reads.
- **Scenario**: User A reads the rating of a track, User B updates the rating, and User A reads the rating again, seeing different values.

### 3. **Phantom Read**

- **Phenomenon**: A transaction reads a set of rows that satisfy a condition, another transaction inserts or deletes rows that satisfy the condition, and the first transaction reads again, seeing a different set of rows.
- **Scenario**: User A queries all tracks in a playlist, User B adds a new track to the playlist, and User A queries the playlist again, seeing the new track.

## Respective Sequence Diagrams

### 1. Dirty Read

    sequenceDiagram
    participant UserA as User A
    participant UserB as User B
    participant DB as Database

    UserA->>DB: BEGIN TRANSACTION
    UserA->>DB: UPDATE tracks SET popularity = 90 WHERE track_id = 1
    UserB->>DB: SELECT popularity FROM tracks WHERE track_id = 1
    DB-->>UserB: popularity = 90 (uncommitted)
    UserA->>DB: COMMIT

![image](https://github.com/jcheruvelil/MusicRecsAPI/assets/54489933/9f724daf-dba4-401d-be29-efcada5158eb)


### 2. Non-repeatable Read

    sequenceDiagram
    participant UserA as User A
    participant UserB as User B
    participant DB as Database

    UserA->>DB: BEGIN TRANSACTION
    UserA->>DB: SELECT rating FROM ratings WHERE track_id = 1
    DB-->>UserA: rating = 5
    UserB->>DB: UPDATE ratings SET rating = 4 WHERE track_id = 1
    UserB->>DB: COMMIT
    UserA->>DB: SELECT rating FROM ratings WHERE track_id = 1
    DB-->>UserA: rating = 4
    UserA->>DB: COMMIT

![image](https://github.com/jcheruvelil/MusicRecsAPI/assets/54489933/7ec27a3d-bcec-40d9-a1aa-2fa0e8d1fa90)


### 3. Phantom Read

    sequenceDiagram
    participant UserA as User A
    participant UserB as User B
    participant DB as Database

    UserA->>DB: BEGIN TRANSACTION
    UserA->>DB: SELECT * FROM playlist_tracks WHERE playlist_id = 1
    DB-->>UserA: track_ids = [1, 2, 3]
    UserB->>DB: INSERT INTO playlist_tracks (playlist_id, track_id) VALUES (1, 4)
    UserB->>DB: COMMIT
    UserA->>DB: SELECT * FROM playlist_tracks WHERE playlist_id = 1
    DB-->>UserA: track_ids = [1, 2, 3, 4]
    UserA->>DB: COMMIT

![image](https://github.com/jcheruvelil/MusicRecsAPI/assets/54489933/5b291014-92cf-4b73-bc77-53aa79e119f3)

