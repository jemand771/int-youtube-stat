let inputForm = document.getElementsByTagName("form")[0];
inputForm.addEventListener('submit', (event) => {
    event.preventDefault();
    fetch("/video_data/"+document.getElementById("lk").value)
    .then(res => res.json())
    .then((out) => {
        console.log('Output: ', out);
        createVideoObjects(out);
        updateStatistics();
    }).catch(err => {
    console.error(err);
    alert(":( Video oder Playlist nicht gefunden.");
    });
    });

    function updateStats() {
        let videos = document.getElementsByClassName("single-video-container");
        let ids;
        for (let i = 0; i < videos.length; i++) {
            ids[i] = videos[i].getAttribute("id");
        }
        console.log(ids);
    }