# A Music streaming website based on database

A music streaming website based on a relational database on PostgreSQL on Google Cloud Platform. The database is consisted of 7 entities and their relationships, and the schema has 13 tables. I also developed an application with Python Flask and SQL queries which allowed users to query songs, create and subscribe to playlists, and follow artists on a web page built in HTML.

Data is collected from a music streaming website by web scraping. There are 556 songs from 29 artists in the database.

## Features
Users can:
- Query songs, albums, users, artists, playlists
- Create private and public playlists after logging in
- Follow/unfollow artists
- Subscribe to playlists
- Get recommendations on artists to follow and songs to listen on home page 

## Technolgies
- Relational database
- Python Flask
- SQL
- PostgreSQL
- HTML

## Database

The tables in the database are:
* artist: refers to an artist (individual artist or a band)
* album: refers to an album
* song: refers to a song
* users: refers to a user
* playlist_createdby: refers to a playlist and its creator
* genre: refers to a genre
* record: refers to a record company
* artist_of: an artist is artist_of an album, the relationship between artist and album
* owned_by: an album is owned_by a record company, the relationship between album and record
* part_of: a song is part_of an album, the relationship between song and album
* belongs_to: a song belongs_to a genre, the relationship between song and genre
* is_in: a song is_in a playlist, the relationship between song and playlist_createdby
* starred_by: a playlist is starred_by a user, the relationship between user and playlist_createdby
* followed_by: an artist is followed_by a user, the relationship between user and artist

Entity Relationship diagram:
<p>
  <img src="https://user-images.githubusercontent.com/93358121/198050529-f85f904f-1ef7-48d0-934f-41781264f037.jpg" />
<p/>


## Screenshots of website

![image](https://user-images.githubusercontent.com/93358121/162550292-4210cddc-3558-4618-b46b-93ad30bf6361.png)

![image](https://user-images.githubusercontent.com/93358121/162550515-110aafcb-ee8d-4cfc-95c6-6d1ae88e4772.png)

![image](https://user-images.githubusercontent.com/93358121/162550505-77a4d3ec-cf55-4e15-be60-eb2109bb4f82.png)

![image](https://user-images.githubusercontent.com/93358121/162550559-1334613b-5960-4aa8-a089-009c5b18cf37.png)

![image](https://user-images.githubusercontent.com/93358121/162550480-c0f304e6-4ebd-435b-958b-cc96c1e80a2d.png)

![image](https://user-images.githubusercontent.com/93358121/162550488-300c32f0-1059-47a2-81e4-d0091c5042b4.png)
