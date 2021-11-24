    function updateStatistics() {
        let videos = document.getElementsByClassName("single-video-container");
        // console.log(videos);
        let ids = new Array();
        for (let i = 0; i < videos.length; i++) {
            ids[i] = videos[i].getAttribute("id");
        }
        // console.log(ids);
        fetch("/stats", {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
//        json: ids,
        body: JSON.stringify(ids),
        })
        .then(res => res.json())
        .then((out) => {
            document.getElementById("label-video-count").innerHTML = videos.length;
            document.getElementById("label-combined-duration").innerHTML = out.total_duration;
            document.getElementById("label-average-duration").innerHTML = out.avg_duration;
            document.getElementById("label-average-likes").innerHTML = out.avg_likes;
            document.getElementById("label-average-views").innerHTML = out.avg_views;
        }).catch(err => {
        console.error(err);
        });
        }


    function resetStatistics() {
        document.getElementById("label-video-count").innerHTML = "0";
        document.getElementById("label-combined-duration").innerHTML = "0";
        document.getElementById("label-average-duration").innerHTML = "0";
        document.getElementById("label-average-likes").innerHTML = "0";
        document.getElementById("label-average-views").innerHTML = "0";
    }