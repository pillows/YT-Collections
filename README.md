# YT Collections

## Subscription Manager and Minimal alternative to Youtube
- Provide a simple view of a user's subscriptions 
- Group user subcscriptions into collections to allow for a filtered video feed
- Automatically creates basic collections for users by grouping subscriptions by channel topics
- Create video playlists on the fly with temporary playlists that are deleted when session is ended

# 

## Backend
- Flask
- MongoDB to store user information
- Redis to cache network requests made to YouTube API

## Frontend
- React
- Webpack to bundle files
- Redux to cache initial states that require network requests to set


## TODO
- NavBar
    - [ ] Finish Account View/Settings

- Subscriptions
    - [ ] Subscriptions Component
    - [ ] Show channel name, views, subscribers count, and date of subscribe

- Channel
    - [ ] Show recent videos
    - [ ] Search videos
    - [ ] Unsubscribe

- Collections
    - [ ] Collections Component
    - [ ] Create new collection
    - [ ] Copy existing collection
    - [ ] Add channel to collection
    - [ ] Default collections are non editable
    - [ ] Videos view of collections 

- Playlists
    - [ ] Temp playlists (saved locally)
    - [ ] Import user playlists?
    - [ ] Add Video to playlist

- Errors
    - [ ] 5XX Error page
    - [ ] Handle error if Youtube API request fail ( from being down or rate limit reached )

- Optimizations
    - [ ] Add rq to server ?? (Later on, only need in collections build and subscriptions build)
    - [ ] User will temporarilly not be able to access most features as subscriptions and collections are need to be finished in the background
    - [ ] In the meantime use threading to work on subscriptions and collections