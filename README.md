# 4111Database-Project1-Music streaming website

## Overview

In this project, we implemented a music streaming application with basic functionalities where users can query songs, artists, albums, playlists, etc. Apart from this, the users can also create private and public playlists after logging in. Users can also follow artists of their interest and subscribe playlists that they enjoy listening to. We provide users with some recommendations on artists to follow and songs to listen on the home page. 
We use web scraping to get data from a music streaming website and load it to our database. We have 556 songs from 29 artists in our database.<br>

## Description

The tables in our database are:
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

## Web pages with interesting operations

* Search page: A query is made to a number of different tables to find songs, artists, albums and playlist that match a given search term. This required using pattern matching and case-insensitive querying. And we provide users with some random suggestions on artists to follow and songs to listen on the home page, in order to get new users started.
* Artist page with follow/unfollow option: This page displays an artist and all the albums released by the artist. Additionally, you can follow the artist and find your following artists on profile page if you are not following the artist, or unfollow the artist if you have already followed. 
* Playlist page with subscribe/unsubscribe option: This page displays a playlist and all the songs in it. You can subcribe the playlist if you are not subscribing, or unsubscribe it if you are. Besides, users can set their playlists as public or private. Other users won't be able to visit your private playlists.

## Screenshots of our website
* **Home page**
![image](https://user-images.githubusercontent.com/93358121/162550292-4210cddc-3558-4618-b46b-93ad30bf6361.png)
* **Create account**
![image](https://user-images.githubusercontent.com/93358121/162550515-110aafcb-ee8d-4cfc-95c6-6d1ae88e4772.png)
* **Create playlist**
![image](https://user-images.githubusercontent.com/93358121/162550505-77a4d3ec-cf55-4e15-be60-eb2109bb4f82.png)
* **Search result**
![image](https://user-images.githubusercontent.com/93358121/162550559-1334613b-5960-4aa8-a089-009c5b18cf37.png)
* **Artist page**
![image](https://user-images.githubusercontent.com/93358121/162550480-c0f304e6-4ebd-435b-958b-cc96c1e80a2d.png)
* **Playlist page**
![image](https://user-images.githubusercontent.com/93358121/162550488-300c32f0-1059-47a2-81e4-d0091c5042b4.png)
