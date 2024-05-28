# Concurrency

## Outline

Since our project involves many tables and transactions which all interact with one another, we try to implement concurrency control mechanisms which are outlined and will have sequence diagrams.

## Concurrency Control Mechanisms

We use:

1. **Locking** locks are used to prevent multiple transactions from modifying a single row at once.
2. **Time Stamp Protocol** utilized to ensure stability in our transactions, using time stamps to determine a transactions order compared to another
3.

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
