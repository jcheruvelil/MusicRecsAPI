# Example Flows

Bob wants to get a song recommendation based on another song he really likes. He first searches for the song that he already knows by calling GET /search/ and inputting a song, which gets a song id of 3030. 
He then calls GET /recommendation/{song_id} and gets songs that are similar. He decides he likes some but also dislikes some of the recommendations. 
He wants to rate these songs so he calls POST /{song_id}/rate for all of the songs and inputs his rating. 


Julie wants to get recommended more songs from a genre she recently got into, Rock. She calls POST /recommendations with her UID, as well as specifying “Rock” as the genre she desires to 
filter the recommendations by to get a recommendation in the genre. The system then will generate a list of songs that are recommended to Julie in the Rock genre that hopefully Julie finds pleasant. 
Julie then can add this song to her playlist if she desires.

Tommy wants to add some new songs to their playlist. He acquires the details of his playlist by using GET /playlist/{playlist_id}. 
He then discovers new songs to input and calls PUT /playlist/{playlist_id}/add with the ID of the new song. 
After the song has been added, he calls GET /playlist/{playlist_id} again to verify the addition.
