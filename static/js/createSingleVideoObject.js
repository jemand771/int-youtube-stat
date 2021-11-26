function createSingleVideoContainer(id, title, thumbnail, views, likes, duration, channelName, channelID) {
    let videoContainer = document.getElementsByClassName("scroll-box")[0];
    // create a container for a single video
    let singleVideoContainer = document.createElement("section");
    singleVideoContainer.setAttribute("class", "single-video-container");
    singleVideoContainer.setAttribute("id", id);
    singleVideoContainer.setAttribute("likes", likes);
    singleVideoContainer.setAttribute("views", views);
    videoContainer.appendChild(singleVideoContainer);
    // append Thumbnail to the container
    let singleVideoThumbnail = document.createElement("img");
    singleVideoThumbnail.setAttribute("class", "single-video-thumbnail");
    singleVideoThumbnail.setAttribute("id", id);
    singleVideoThumbnail.setAttribute("src", thumbnail);
    singleVideoContainer.appendChild(singleVideoThumbnail);
    // append Stats for the video
    let singleVideoStats = document.createElement("div");
    singleVideoStats.setAttribute("class", "single-video-stats");
    singleVideoStats.setAttribute("id", id);
    // title as clickable URL
    let videoTitleContainer = document.createElement("h3");
    singleVideoStats.appendChild(videoTitleContainer);
    let singleVideoTitleUrl = document.createElement("a");
    singleVideoTitleUrl.setAttribute("href", ('https://www.youtube.com/watch?v='+id));
    singleVideoTitleUrl.setAttribute("target", "_blank");
    singleVideoTitleUrl.setAttribute("rel", "noopener noreferrer");
    singleVideoTitleUrl.innerHTML = title;
    videoTitleContainer.appendChild(singleVideoTitleUrl);
    // channel name as clickable URL
    let singleVideoChannelContainer = document.createElement("h5");
    singleVideoStats.appendChild(singleVideoChannelContainer);
    let singleVideoChannelUrl = document.createElement("a");
    singleVideoChannelUrl.setAttribute("href", ("https://www.youtube.com/channel/" + channelID));
    singleVideoChannelUrl.setAttribute("target", "_blank");
    singleVideoChannelUrl.setAttribute("rel", "noopener noreferrer");
    singleVideoChannelUrl.innerHTML = channelName;
    singleVideoChannelContainer.appendChild(singleVideoChannelUrl);
    // Likes
    let videoLikes = document.createElement("p");
    videoLikes.innerHTML = "<i class=\"material-icons i-small\">thumb_up</i> Likes: " + likes;
    singleVideoStats.appendChild(videoLikes);
    // Views
    let videoViews = document.createElement("p");
    videoViews.innerHTML = "<i class=\"material-icons i-small\">people_alt</i> Views: " + views;
    singleVideoStats.appendChild(videoViews);
    // Duration
    let videoDuration = document.createElement("p");
    videoDuration.innerHTML = "<i class=\"material-icons i-small\">schedule</i> Länge: " + duration;
    singleVideoStats.appendChild(videoDuration);
    singleVideoContainer.appendChild(singleVideoStats);
    // append delete button for the Container
    let delBut = document.createElement("button");
    delBut.setAttribute("class", "btn-delete-element");
    delBut.setAttribute("onClick", "removeChildElement(this)");
    let deleteIcon = document.createElement("span");
    deleteIcon.setAttribute("class", "material-icons");
    deleteIcon.innerHTML = "delete";
    delBut.appendChild(deleteIcon);
    singleVideoContainer.appendChild(delBut);

}
