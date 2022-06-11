songDurations = $(".track_duration");
songDurations.each(function(index, item) {

    item.innerText = formatSongs(parseInt(item.innerText));

})

function formatSongs(song) {

    minutes = Math.floor(song / 60);
    seconds = song % 60;
    if (seconds < 10) seconds = "0" + seconds;
    return minutes + ":" + seconds;

}

function formatSongNames() {

    songNames = $(".album_track_name");

    $(album["tracklist"]).each((index, track) => {

        (track.slice(-5, -1) == "None") ? track = "{" + track.substr(19, track.length - 35) + "}" : track = "{" + track.substr(19, track.length - 1);
        (track.indexOf("title") == 18) ? i = 31 : i = 33;
        trackTitle = '"' + track.substr(track.indexOf("title") + 9, track.indexOf("duration") -i) + '"';
        trackTitle = trackTitle.replaceAll("'", "");
        track = track.substr(0, track.indexOf("title") + 8) + trackTitle + track.substr(track.indexOf("duration") - 3, track.length - 1);
        track = track.replaceAll("'", '"');
        track = JSON.parse(track);
        album["tracklist"][index] = track;
        songNames[index].innerText = track["title"];

    })

}

formatSongNames();
album["artist_name"] = artist_dict["name"]

favoriteButtons = $(".album_track_add_favorite");
favoriteButtons.click(function(event) {

    ($(this).hasClass("liked")) ? unlikeSong($(this), false): likeSong($(this), false);

})

favoriteAlbums = $(".album_add_favorite");
favoriteAlbums.click(function(event) {

    ($(this).hasClass("liked")) ? unlikeAlbum($(this), false): likeAlbum($(this), false);

})

//if user has liked tracks previously, add visual indicator to them
function likeTracks() {

    var tracks = $(".album_track_name");
    var favoriteTracksListTitles = $.map(favoriteTracks, function(favTrack) { return favTrack["title"] });
    console.log(favoriteTracksListTitles);

    $(tracks).each((index, track) => {

        if (favoriteTracksListTitles.includes($(track).prop("innerText"))) {

            console.log($(track).prop("innerText"));
            console.log($(track).parent().next());
            likeSong($(track).parent().next(), true);

        }

    })

}

if (typeof(favoriteTracks) != 'undefined') likeTracks();

function unlikeSong(song, k) {

    song.removeClass("liked");
    songName = $(song.prev().children()[0]).prop("innerText");
    console.log(songName);
    $(album["tracklist"]).each((index, track) => {

        if (track["title"] == songName) ajaxRequest("DELETE", {"user":user, "track":track});

    })

}

function likeSong(song, k) {

    song.addClass("liked");
    songName = $(song.prev().children()[0]).prop("innerText");
    console.log(songName);
    $(album["tracklist"]).each((index, track) => {

        if (track["title"] == songName && !k) { console.log(track); console.log(album); track["cover"] = album["cover"]; track["artist_name"] = artist_dict["name"]; ajaxRequest("POST", {"user":user, "track":track}); }

    })

}

function unlikeAlbum(albumElement, k) {

    albumElement.removeClass("liked");
    console.log(albumElement);

}

function likeAlbum(albumElement, k) {

    albumElement.addClass("liked");
    console.log(albumElement);
    console.log(album);
    console.log(artist_dict);

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

function ajaxRequestAlbums(reqMethod, reqData) {

    $.ajax({
    type: reqMethod,
    url: `../api/users/${user}/albums`,
    contentType: "application/json",
    data: JSON.stringify(reqData),
    dataType: "json"
  });

}