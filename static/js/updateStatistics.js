    function updateStatistics() {
        let videos = document.getElementsByClassName("single-video-container");
        console.log(videos);
        let ids = new Array();
        for (let i = 0; i < videos.length; i++) {
            ids[i] = videos[i].getAttribute("id");
        }
        console.log(ids);
        // TODO fetch-request with ids-array
    }

    function resetStatistics() {
        document.getElementById("label-combined-duration").innerHTML = "0";
        document.getElementById("label-average-duration").innerHTML = "0";
        document.getElementById("label-average-likes").innerHTML = "0";
        document.getElementById("label-average-views").innerHTML = "0";
    }