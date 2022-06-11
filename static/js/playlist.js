var trackDurations = $(".track_duration");
trackDurations.each((index, item) => { item.innerText = formatSongs(item.innerText); })
console.log(playlist);

function formatSongs(song) {

    minutes = Math.floor(song / 60);
    seconds = song % 60;
    if (seconds < 10) seconds = "0" + seconds;
    return minutes + ":" + seconds;

}

playlistFavoriteButton = ".playlist_add_favorite";
$(playlistFavoriteButton).click(function(event) {

    ($(this).hasClass("liked")) ? unlikePlaylist($(this), false): likePlaylist($(this), false);

})

$(favoritePlaylists).each((index, favoritePlaylist) => {

    if (favoritePlaylist == playlist["title"]) likePlaylist($(playlistFavoriteButton), "true");

})

trackFavoriteButton = ".track_add_favorite";
$(trackFavoriteButton).click(function(event) {

    ($(this).hasClass("liked")) ? unlikeSong($(this), false): likeSong($(this), false);

})

function unlikeSong(song, k) {

    song.removeClass("liked");
    songName = $(song.prev()).prop("innerText");
    console.log(songName);
    artistName = $(song.prev().prev()).prop("innerText");
    $(playlist["tracklist"]).each((index, track) => {

        if (track["title"] == songName && track["artist_name"] == artistName && !k) ajaxRequest("DELETE", {"user":user, "track":track});

    })

}

function likeSong(song, k) {

    song.addClass("liked");
    songName = $(song.prev()).prop("innerText");
    console.log(songName);
    artistName = $(song.prev().prev()).prop("innerText");
    $(playlist["tracklist"]).each((index, track) => {

        if (track["title"] == songName && !k) { ajaxRequest("POST", {"user":user, "track":track}); }

    })

}

function unlikePlaylist(playlistElement, k) {

    console.log($(playlistElement.prev()).prop("innerText"));
    playlistElement.removeClass("liked");
    ajaxRequestPlaylist("DELETE", playlist)


}

function likePlaylist(playlistElement, k) {

    //console.log(playlist);
    playlistElement.addClass("liked");
    if (!k) ajaxRequestPlaylist("POST", playlist)

}

function ajaxRequest(reqMethod, reqData) {

    $.ajax({
    type: reqMethod,
    url: `${window.location.href.split("playlists")[0]}api/users/${user}/tracks`,
    contentType: "application/json",
    data: JSON.stringify(reqData),
    dataType: "json"
  });

}

function ajaxRequestPlaylist(reqMethod, reqData) {

    $.ajax({
    type: reqMethod,
    url: `${window.location.href.split("playlists")[0]}api/users/${user}/playlists`,
    contentType: "application/json",
    data: JSON.stringify(reqData),
    dataType: "json"
  });

}