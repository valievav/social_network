### Project:
REST API for social network & automated bot to make calls to the API

---
### REST API for social network

### Models:
- User
- Post (requires authentication)

### Features:
- user signup -> **/api/user/register/**
- user login -> **/api/user/token/**
- post creation -> **/api/posts/**
- post like -> **/api/posts/<int:pk>/like/** with POST
- post unlike -> **/api/posts/<int:pk>/like/** with DELETE
- analytics about how many likes was made (analytics aggregated by day). -> **/api/likes-analytics/** for all dates or **/api/likes-analytics/?date_from=2020-09-02&date_to=2020-09-15**
- user activity an endpoint which shows when user logged in last time and when was made last
request to the service -> **/api/users/activity/**
- JWT token authentication (**/api/user/token/** & **/api/user/token/refresh/**)

---
### Automated bot to call social network's API

### Config fields:
- number_of_users
- max_posts_per_user
- max_likes_per_user

### Bot workflow:
1. Read setup field from config file
2. Run next activities:
- signs up users (according to number_of_users)
- each user creates random number of posts with any content (up to max_posts_per_user)
- posts are liked randomly, one post can be liked my multiple users, one user can like one post.
