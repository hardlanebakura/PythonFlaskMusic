trackDurations = $(".track_duration");
$(trackDurations).each((index, trackDuration) => {

    trackDuration.innerText = formatSongs(trackDuration.innerText);
    likeSong($($(trackDuration).parent().children()[5]), true);

})

console.log(liked_songs);

function formatSongs(song) {

    minutes = Math.floor(song / 60);
    seconds = song % 60;
    if (seconds < 10) seconds = "0" + seconds;
    return minutes + ":" + seconds;

}

favoriteButtons = $(".track_add_favorite");
favoriteButtons.click(function(event) {

    if ($(this).hasClass("liked")) unlikeSong($(this), false);

})

function unlikeSong(song, k) {

    song.removeClass("liked");
    songName = $($($(song.parent()).children()[2]).children()[0]).prop("innerText");
    console.log(songName);
    $(liked_songs).each((index, track) => {

        console.log(user);
        song.parent().css("display", "none");
        if (track["title"] == songName) ajaxRequest("DELETE", {"user":user, "track":track});
        console.log(track);

    })

    songNumber = $(".liked_songs_user_name").prop("innerText");
    $(".liked_songs_user_name").text(songNumber.split(" ")[0] + " " + (parseInt(songNumber.split(" ")[1]) - 1).toString() + " " + songNumber.split(" ")[2]);

}

function likeSong(song, k) {

    song.addClass("liked");

}

function ajaxRequest(reqMethod, reqData) {

    $.ajax({
    type: reqMethod,
    url: `${window.location.href.split("users")[0]}api/users/${user}/tracks`,
    contentType: "application/json",
    data: JSON.stringify(reqData),
    dataType: "json"
  });

}
