//TODO invoke function for each element in list
function createSingleVideoContainer(id, title, thumbnail, views, likes, length) {
    let videoContainer = document.getElementsByClassName("scroll-box")[0];
    let singleVideoContainer = document.createElement("section");
    singleVideoContainer.setAttribute("class", "single-video-container");
    singleVideoContainer.setAttribute("id", id);
    videoContainer.appendChild(singleVideoContainer);

    let singleVideoThumbnail = document.createElement("div");
    singleVideoThumbnail.setAttribute("class", "single-video-thumbnail");
    singleVideoThumbnail.setAttribute("id", id);
    let thumbnailCanvas = function () {
        let canvas = document.createElement("canvas");
        canvas.setAttribute("id", id);
        canvas.setAttribute("width", "200");
        canvas.setAttribute("height", "100");
        //TODO put thumbnail here, this is just some beautiful drawing i made :^)
        let ctx = canvas.getContext("2d");
        ctx.moveTo(0, 0);
        ctx.lineTo(200, 100);
        ctx.moveTo(200, 0);
        ctx.lineTo(0, 100)
        ctx.stroke();
        ctx.arc(100, 50, 50, 0, 2 * Math.PI);
        ctx.stroke();
        return canvas;
    };
    singleVideoThumbnail.appendChild(thumbnailCanvas());
    singleVideoContainer.appendChild(singleVideoThumbnail);

    let singleVideoStats = document.createElement("div");
    singleVideoStats.setAttribute("class", "single-video-stats");
    singleVideoStats.setAttribute("id", id);
    let videoTitle = document.createElement("h3");
    videoTitle.innerHTML = title;
    singleVideoStats.appendChild(videoTitle);
    let videoLikes = document.createElement("p");
    videoLikes.innerHTML = "Bewertung: " + likes;
    singleVideoStats.appendChild(videoLikes);
    let videoViews = document.createElement("p");
    videoViews.innerHTML = "Views: " + views;
    singleVideoStats.appendChild(videoViews);
    let videoLength = document.createElement("p");
    videoLength.innerHTML = "Länge: " + length;
    singleVideoStats.appendChild(videoLength);
    singleVideoContainer.appendChild(singleVideoStats);
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