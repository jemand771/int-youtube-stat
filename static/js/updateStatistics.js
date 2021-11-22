    function updateStatistics() {
        let videos = document.getElementsByClassName("single-video-container");
        console.log(videos);
        let ids = new Array();
        for (let i = 0; i < videos.length; i++) {
            ids[i] = videos[i].getAttribute("id");
        }
        console.log(ids);
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
            console.log("hello")
            console.log(out);
            document.getElementById("label-video-count").innerHTML = videos.length;
            document.getElementById("label-combined-duration").innerHTML = out.total_duration;
            document.getElementById("label-average-duration").innerHTML = (out.total_duration/videos.length).toFixed(0);
            //TODO temporäre client side berechnung
            let single_videos = document.getElementsByClassName("single-video-container");
            let total_likes = 0;
            let total_views = 0;
            for (let i = 0; i < videos.length; i++) {
                total_likes += parseInt(single_videos[i].getAttribute("likes"), 10);
                total_views += parseInt(single_videos[i].getAttribute("views"), 10);
            }
            console.log(total_views + " <- views     likes -> " + total_likes)
            document.getElementById("label-average-likes").innerHTML = (total_likes/videos.length).toFixed(0);
            document.getElementById("label-average-views").innerHTML = (total_views/videos.length).toFixed(0);
            // bis hier her kann dann weg lol
//            document.getElementById("label-average-likes").innerHTML = out.average_likes;
//            document.getElementById("label-average-views").innerHTML = out.average_views;
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