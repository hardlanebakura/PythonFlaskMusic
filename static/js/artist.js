console.log(artist_dict);
songDurations = $(".artist_popular_duration");
songDurations.each(function(index, item) {

    item.innerText = formatSongs(parseInt(item.innerText));

})

//if user has liked tracks previously, add visual indicator to them
function likeTracks() {

    var topTracksInArtist = $(".artist_popular_title");
    $(topTracksInArtist).each((index, topTrack) => {

        $(favoriteTracks).each((index, favoriteTrack) => {

            if (favoriteTrack.title == $(topTrack).prop("innerText")) likeSong($(topTrack).next());

        })

    })

}

if (typeof(favoriteTracks) != 'undefined') likeTracks();


function formatSongs(song) {

    minutes = Math.floor(song / 60);
    seconds = song % 60;
    if (seconds < 10) seconds = "0" + seconds;
    return minutes + ":" + seconds;

}

favoriteButtons = $(".artist_popular_add_favorite");
favoriteButtons.click(function(event) {

    ($(this).hasClass("liked")) ? unlikeSong($(this)): likeSong($(this));

})

displayAllAlbumsButton = $("#artist_album_all");
displayAllPlaylistsButton = $("#artist_playlist_all");
hideAllAlbumsButton = $("#artist_album_hide_all");
hideAllPlaylistsButton = $("#artist_playlist_hide_all");

displayAllAlbumsButton.click((event) => displayAll(event.target, "albums"));
displayAllPlaylistsButton.click((event) => displayAll(event.target, "playlists"));
hideAllAlbumsButton.click((event) => hideAll(event.target, "albums"));
hideAllPlaylistsButton.click((event) => hideAll(event.target, "playlists"));

function unlikeSong(song) {

    song.removeClass("liked");
    songName = song.prev().prop("innerText");
    console.log(songName);
    $(artist_dict["tracks_top"]).each((index, trackTop) => {

        trackTop = "{" + trackTop.substr(19, trackTop.length - 1);
        trackTop = trackTop.replaceAll("'", '"');
        trackTop = JSON.parse(trackTop);
        console.log(trackTop["title"]);
        console.log(songName);
        if (trackTop["title"] == songName) ajaxRequest("DELETE", {"user":user, "track":trackTop});

    })

}

function likeSong(song) {

    song.addClass("liked");
    songName = song.prev().prop("innerText");
    console.log(songName);
    $(artist_dict["tracks_top"]).each((index, trackTop) => {

        trackTop = "{" + trackTop.substr(19, trackTop.length - 1);
        trackTop = trackTop.replaceAll("'", '"');
        trackTop = JSON.parse(trackTop);
        if (trackTop["title"] == songName) { console.log(songName); trackTop["artist_name"] = artist_dict["name"]; ajaxRequest("POST", {"user":user, "track":trackTop}); }


    })

}

function displayAll(element, displayType) {

    var elementRow = $(element).parent().parent().next();
    (displayType == "albums") ? displayAllAlbums() : displayAllPlaylists();

    function displayAllAlbums() {

        var elementsToPut = artist_dict["albums"].length - 6;
        var rowsToPut = Math.ceil(elementsToPut / 6);
        for (let i = 0; i < rowsToPut; i++) $(elementRow).after(`<div class = 'artist_albums_row'></div>`);

        albumsRows = $(".artist_albums_row");
        $(albumsRows).each((index, albumRow) => {

            if (index > 0) {

                albumRow.innerHTML += `${function() {

                    var albumElements = "";

                    for (let j = 0; j < 6; j++) {

                        if (artist_dict["albums"][index*6 + j] != undefined) {

                            album = formatStringsAlbums(artist_dict["albums"][index*6 + j]);
                            albumLink = `/albums/${formatStringsAlbums(artist_dict["albums"][index*6 + j])["id"]}?artist=${artist_dict["id"]}`;
                            albumElements += `<a href = ${albumLink}><div class = "album_wrapper"><div class = "artist_album">${(function() {

                                return `<img class = "artist_album_img" src = ${album["cover"]}><div class = "artist_album_name">${album["title"]}</div><div class = "artist_album_year">${album["release_date"].split("-")[0]}</div>`;

                            } ())}</div></div>`;

                        }

                    }

                    return albumElements;

                } ()} </a>`;

            }

        })

    $(element).css("display", "none");
    $(element).next().css("display", "block");

    }

    function displayAllPlaylists() {

        var elementsToPut = artist_dict["playlists"].length - 6;
        var rowsToPut = Math.ceil(elementsToPut / 6);

        for (let i = 0; i < rowsToPut; i++) $(elementRow).after(`<div class = 'artist_playlist_row'></div>`);

        playlistRows = $(".artist_playlist_row");
        $(playlistRows).each((index, playlistRow) => {

            if (index > 0) {

                playlistRow.innerHTML += `${function() {

                    var playlistElements = "";

                    for (let j = 0; j < 6; j++) {

                        if (artist_dict["playlists"][index*6 + j] != undefined) {

                            playlist = formatStringsPlaylist(artist_dict["playlists"][index*6 + j]);
                            playlistLink = `/playlists/${playlist["id"]}`;
                            playlistElements += `<a href = ${playlistLink}><div class = "album_wrapper"><div class = "artist_playlist">${(function() {

                                return `<img class = "artist_album_img" src = ${playlist["cover"]}><div class = "artist_album_name">${playlist["title"]}</div>`;

                            } ())}</div></div></a>`;
                            console.log(playlist);
                            console.log(playlistLink);

                        }

                    }

                    return playlistElements;

                } ()} `;

            }

        });

    $(element).css("display", "none");
    $(element).next().css("display", "block");

    }

}

function hideAll(element, displayType) {

    var elementRow = $(element).parent().parent().next();
    console.log(elementRow);
    (displayType == "albums") ? hideAllAlbums() : hideAllPlaylists();

    function hideAllAlbums() {

        albumsRows = $(".artist_albums_row");
        $(albumsRows).each((index, albumRow) => {

            if (index > 0) $(albumRow).remove();

        });

        $(element).css("display", "none");
        $(element).prev().css("display", "block");

    }

    function hideAllPlaylists() {

        playlistRows = $(".artist_playlist_row");
        $(playlistRows).each((index, playlistRow) => {

            if (index > 0) $(playlistRow).remove();

        });

        $(element).css("display", "none");
        $(element).prev().css("display", "block");

    }

}

function formatStringsAlbums(string) {

    s1 = (string.substr(0, string.indexOf("tracklist") - 3) + "}").replaceAll("'", '"');
    s1 = s1.substr(0, s1.indexOf('title') + 9) + (s1.substr(s1.indexOf('title') + 9, s1.indexOf('cover') - 32)).replaceAll('"', "") + s1.substr(s1.indexOf('cover') - 6, s1.length - 1);
    return JSON.parse(s1);

}

function formatStringsPlaylist(string) {

    s1 = ("{" + string.substr(string.indexOf("'id'"), string.indexOf("tracklist") - 25) + "}").replaceAll("'", '"')
    s1 = s1.substr(0, s1.indexOf('"title"') + 10) + s1.substr(s1.indexOf('"title"') + 10, s1.indexOf('"cover"') - 32).replaceAll('"', "") + s1.substr(s1.indexOf('"cover"') -3);
    return JSON.parse(s1);

}

function ajaxRequest(reqMethod, reqData) {

    $.ajax({
    type: reqMethod,
    url: `../api/users/${user}/tracks`,
    contentType: "application/json",
    data: JSON.stringify(reqData),
    dataType: "json"
  });

}

