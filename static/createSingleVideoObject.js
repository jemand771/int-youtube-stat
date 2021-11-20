function createSingleVideoContainer(id, title, thumbnail, views, likes, duration) {
    let videoContainer = document.getElementsByClassName("scroll-box")[0];
    // create a container for a single video
    let singleVideoContainer = document.createElement("section");
    singleVideoContainer.setAttribute("class", "single-video-container");
    singleVideoContainer.setAttribute("id", id);
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
    let videoTitleUrl = document.createElement("a");
    videoTitleUrl.setAttribute("href", ('https://www.youtube.com/watch?v='+id));
    videoTitleUrl.setAttribute("target", "_blank");
    videoTitleUrl.setAttribute("rel", "noopener noreferrer");
    videoTitleUrl.innerHTML = title;
    videoTitleContainer.appendChild(videoTitleUrl);
    // Likes
    let videoLikes = document.createElement("p");
    videoLikes.innerHTML = "Likes: " + likes;
    singleVideoStats.appendChild(videoLikes);
    // Views
    let videoViews = document.createElement("p");
    videoViews.innerHTML = "Views: " + views;
    singleVideoStats.appendChild(videoViews);
    // Duration
    let videoDuration = document.createElement("p");
    videoDuration.innerHTML = "Länge: " + duration;
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
//TODO add delete all elements button
function removeChildElement(childElement) {
    childElement.parentElement.remove();
}
