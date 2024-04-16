User Stories

As a listener, I want to be able to get song recommendations based on a song input so that I can quickly find new songs.
As a listener, I want to be able to get song recommendations based on a selected genre so that I can get recommendations that are within a specific range I know.
As a listener, I want to be able to get song recommendations based on a selected artist so that I can find songs similar to groups I like.
As a listener, I want to be able to get a recommendation based on a mood so that I can find songs that align with how I feel.
As a listener, I want to be able to like songs so that I get recommendations that are similar to the one I liked.
As a listener, I want to be able to dislike songs so that I get less recommendations that are similar to the ones I disliked.
As a listener, I want to be able to save songs that have been recommended to me into lists so that I can request songs similar to ones that I’ve liked in the past.
As a Spotify user, I want to be able to login to spotify so that I can feed my listening history and playlists into the algorithm to get song recommendations.
As a listener, I want to get recommended songs that are more up to date with what I’ve been listening to.
As a listener, I want to see a history of songs that I’ve been recommended so I can return to liked songs.
As a listener, I want to be able to get new recommended songs if I don’t enjoy the ones recommended to me initially.
As a listener, I want to be able to rate songs and albums to keep track of what I have been liking and disliking. 


Exceptions

Input song/artist can’t be found. 
	If the input song or artist can’t be found when prompting a recommendation based on a song, prompt the user that that song cannot be found or isn’t available and ask for another song or artist they like.
 
Spotify account login failed.
  Inform the user the account login failed. Ask them if their username/password is correct.

No recommendations available.
	If there is insufficient user data and/or input data, there are no recommendations available and the system will inform the user and prompt them to change their inputs and provide more data.
 
Preferences not saved.
	If  a user attempts to save ratings or preferences but encounters an error (session timeout, server/internet issues) the system will notify the user and suggest refreshing or trying again. 
 
Ratings not available.
	If there are no ratings available for a particular song or album, the system will display a message indicating this. 
 
Songs not available in their region.
  If the song is not available to listen to in their country, the system will display a message indicating that the song is not available in their country.

Limited song catalog.
  If there are not any songs like the one the user is listening to, possibly one in a new genre, only returning a few results, a message displaying that our song catalog is still growing will occur.

Incompatible device.
  If the device the user is using is not compatible with our software, the system will display a message telling our user of supported devices.

No internet connection
  If the user does not have adequate access to the internet, the system will show the user an indicator showing that there is no connection to the system.

Server overload.
  If the system is under stress or is overloaded, and the user tries accessing it, the system will display a message indicating that the system is currently overloaded, and to try again another time.

Song/album already liked/disliked. 
  If the user likes/dislikes a song or album already, the system will display a message when they try to do it again.

Insufficient permissions for Spotify integration.
	If the necessary permissions for Spotify integration are not enabled by the user, the system will display an error and request the user to allow these permissions. 


