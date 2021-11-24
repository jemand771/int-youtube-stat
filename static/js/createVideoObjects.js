    function createVideoObjects(data) {
        if (data.length != 0) {
            for (let i = 0; i < data.length; i++) {
//                console.log(data[i]);
                createSingleVideoContainer(data[i].id, data[i].title, data[i].thumbnail_url, data[i].view_count, data[i].like_count, data[i].duration, data[i].channel_name, data[i].channel_id);
            }
        } else {
            alert("Viedeo/Playlist ist privat oder wurde gelöscht.")
        }
    }
